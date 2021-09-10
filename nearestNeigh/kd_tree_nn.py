from nearestNeigh.nearest_neigh import NearestNeigh
from nearestNeigh.point import Point
from nearestNeigh.node import Node
from hashlib import md5
import sys

class KDTreeNN(NearestNeigh):

    def __init__(self):

        self.root = None

    def build_index(self, points: [Point]):

        self.root = self.kdtree(points, 0, None)

    def kdtree(self, points: [Point], axis, parent=None) -> Node:

        # Do nothing
        if len(points) < 1:
            return None

        # Subset size 1, root node with no children OR leaf node.
        elif len(points) == 1:
            split = "lat" if axis % 2 == 0 else "lon"
            return Node(
                Point(points[0].id, points[0].cat,
                      points[0].lat, points[0].lon),
                left=None,
                right=None,
                parent=parent,
                split=split)

        elif len(points) > 1:

            # Even, x-axis (lat). Odd, y-axis (lon)
            if axis % 2 == 0:
                points = sorted(points, key=lambda k: k.lat)
                split = "lat"
            else:
                points = sorted(points, key=lambda k: k.lon)
                split = "lon"

            # Get median point
            idx = len(points) >> 1
            median = points[idx]

            # Give node a reference to its parent for ease of backtracking
            node = Node(
                Point(median.id, median.cat, median.lat, median.lon),
                left=None, right=None, parent=parent, split=split)

            # Slice and partition point subsets as child nodes/subtrees
            node.left = self.kdtree(points[:idx], axis + 1, node)
            node.right = self.kdtree(points[idx + 1:], axis + 1, node)

            return node

    def search(self, search_term: Point, k: int) -> [Point]:

        self.nns, self.moves = [], set()
        self.search_knn(None, self.root, search_term, k, 0, None)
        self.nns = sorted(self.nns, key=lambda k: k['dist'])
        self.nns = [n['point'] for n in self.nns]

        return self.nns

    def search_knn(self, prev, C: Node, T: Point, k, axis,
                   move_hash, backtracking=False):
        """
        P = previous node to C
        C = current node under evaluation
        T = target point
        k = total n-neighbours to save
        axis = dimension C is split on
        st = subtree C is in
        backtracking = if or not this iteration is backtracking
        """

        if C is not None:

            prev_print_val = prev.point.id if prev else None
            dtn = "Traversed to" if not backtracking else "Backtracked to"
            # print(dtn, C.point.id, "from", prev_print_val)

            # Stop backtracking at root
            root = True if C.parent is None else False
            if root and backtracking:
                # print("backtracked back to root")
                return

            # Prevent multiple traversals in any direction
            if move_hash in self.moves:
                # print(prev.point.id, "to", C.point.id, "already traversed")
                return

            # Get relevant per-axis node and distance values
            check_other_subtree = False
            a_dist = C.point.dist_to(T)
            T_dim_val = T.lat if axis % 2 == 0 else T.lon
            C_dim_val = C.point.lat if axis % 2 == 0 else T.lat

            # Forward traverse - follow dim splits to leaf nodes
            if not backtracking:
                if T_dim_val >= C_dim_val:
                    if C.right is not None:
                        new_mh = self.hash_move(C.point, C.right.point, "fwd")
                        self.moves.add(move_hash)
                        self.search_knn(C, C.right, T, k, axis + 1, new_mh)
                    else:
                        backtracking = True
                else:
                    if C.left is not None:
                        new_mh = self.hash_move(C.point, C.left.point, "fwd")
                        self.moves.add(move_hash)
                        self.search_knn(C, C.left, T, k, axis + 1, new_mh)
                    else:
                        backtracking = True

                if not C.left and not C.right:
                    backtracking = True
                    print(C.point.id, "leaf node reached")

            # Reverse - evaluate C
            if backtracking:

                # print("backtracking - evaluating", C.point.id)

                p_dist = self.p_distance(axis, C.point, T)
                if C.point.cat == T.cat:
                    if len(self.nns) < k:
                        self.save_n(a_dist, C.point)
                        check_other_subtree = True
                    elif len(self.nns) == k and self.nns[0]['dist'] > a_dist:
                        self.save_n(a_dist, C.point, replace=True)
                        check_other_subtree = True

                # Fwd-traverse unexplored subtree if required
                if self.nns[0]['dist'] > p_dist or len(self.nns) < k or check_other_subtree:
                # if self.nns[0]['dist'] >= p_dist or check_other_subtree:
                    print("checking", C.point.id, "other subtree")
                    if C.left is not None:
                        new_mh = self.hash_move(C.point, C.left.point, "fwd")
                        self.moves.add(move_hash)
                        self.search_knn(C, C.left, T, k, axis + 1, new_mh)
                    if C.right is not None:
                        new_mh = self.hash_move(C.point, C.right.point, "fwd")
                        self.moves.add(move_hash)
                        self.search_knn(C, C.right, T, k, axis + 1, new_mh)

                # Continue backwards up the tree
                if C.parent is not None:
                    new_mh = self.hash_move(C.point, C.parent.point, "rev")
                    self.moves.add(move_hash)
                    self.search_knn(C, C.parent, T, k, axis - 1, new_mh,
                                    backtracking=True)

    def hash_move(self, a, b, direction):
        """
        Hash point a and b as a record of a movement between nodes
        """

        d_val = 13 if direction == "fwd" else 27
        hash_a = self.hash_point(a)
        hash_b = self.hash_point(b)
        return abs(hash_a + hash_b) * d_val

    def save_n(self, dist, point: Point, replace=False):
        """
        Adds new point & sorts by distance descending
        """

        new_n = {
            'dist': dist, 'point': point,
            'hash': self.hash_point(point),
            'id': point.id}

        if new_n['hash'] not in [n['hash'] for n in self.nns]:
            if replace:
                print("Replaced", self.nns[0]['id'], self.nns[0]['dist'], "with",
                      point.id, dist)
                self.nns[0] = new_n
                self.nns = sorted(self.nns, key=lambda k: k['dist'],
                                  reverse=True)
            else:
                print("saved new neighbour", point.id, dist)
                self.nns.append(new_n)
                self.nns = sorted(self.nns, key=lambda k: k['dist'],
                                  reverse=True)

            print("neighbours:")
            for n in [(n['point'].id, n['dist']) for n in self.nns]:
                print(n)

    def add_point(self, point: Point) -> bool:
        """
        Recursive traverse tree to appropriate location and adds point.
        """

        return self.add_traverse(point, self.root, 0)

    def delete_point(self, point: Point) -> bool:
        # To be implemented.
        pass

    def is_point_in(self, point: Point) -> bool:
        # To be implemented.
        pass

    def p_distance(self, axis, C: Point, T: Point) -> float:
        """
        Returns perpendicular distance between T splitting axis and C
        """

        # Dummy point method
        # T = target
        # D = dummy node perpendicular to target
        # C = splitting line / current node

        if axis % 2 == 0:
            D = Point("", C.cat, C.lat, T.lon)

        else:
            D = Point("", C.cat, T.lat, C.lon)

        return C.dist_to(D)

    def hash_point(self, point) -> int:
        """
        Uses hashlib md5() instead of python standard library.

        Python standard library hash() method does not have consistent hashes
        between runs.
        """

        hash_value = 7
        hash_value = 53 * hash_value + int(md5(str(point.id).encode('utf-8')).hexdigest(), 16)
        hash_value = 53 * hash_value + int(md5(str(point.cat).encode('utf-8')).hexdigest(), 16)
        hash_value = 53 * hash_value + int(point.lat * point.lat)
        hash_value = 53 * hash_value + int(point.lon * point.lon)
        return hash_value

    def print(self, root):
        """
        Prints tree top to bottom, left to right descending. 
        """

        depth = self.depth(root)
        for i in range(1, depth + 1):
            print("\n***", "Level", i, "*********************************")
            self.print_level(root, i)

    def print_level(self, node, depth):
        """
        Helper method for print()
        """

        if not node:
            return

        if depth == 1:
            self.print_count += 1
            print(node.point, self.print_count)

        elif depth > 1:
            self.print_level(node.left, depth - 1)
            self.print_level(node.right, depth - 1)

    def depth(self, node):
        """
        Returns depth of a given node
        """

        if not node:
            return 0
        else:
            l_depth = self.depth(node.left)
            r_depth = self.depth(node.right)

            if l_depth > r_depth:
                return l_depth + 1
            else:
                return r_depth + 1
