from nearestNeigh.nearest_neigh import NearestNeigh
from nearestNeigh.point import Point
from nearestNeigh.node import Node
import sys

sys.setrecursionlimit(0x100000)

class KDTreeNN(NearestNeigh):

    def __init__(self):

        self.root = None
        self.node_count = 0
        self.neighbours = []
        self.is_point_found = False
        self.splitAxis = ""


        # Used for detailed debug print output
        self.print_count = 0

        # Conmtains hashes of points already evaluated
        self.closed_list = []
        self.t_closed_list = []

    def build_index(self, points: [Point]):
        """
        Creates KD tree by partitioning given list of points recursively
        """

        print(len(points))

        # for i in points:
        #     if i.id == "id716" or i.id == "id862" or i.id == "id300":
        #         print(i.id)

        self.root = self.partition(points, 0, None)
        print(self.node_count)
        # self.print(self.root)

    def partition(self, points: list, axis: int, parent=None) -> Node:
        """
        Partitions the given list of points into KD tree nodes
        1.  Sort list of points by lon or lat alternatively
        2.  Return median point as current node with points
            above/below the median as subtrees.
        """

        # Empty point set, do nothing
        if len(points) < 1:
            return None

        # Subset size 1, root node with no children OR leaf node.
        elif len(points) == 1:
            self.node_count += 1

            if points[0].id == "id716" or points[0].id == "id862" or points[0].id == "id300":
                print(points[0].id)

            return Node(
                Point(points[0].id, points[0].cat,
                      points[0].lat, points[0].lon),
                left=None,
                right=None,
                parent=parent)

        # >1 point in subset, sort according to alternating axis
        elif len(points) > 1:

            # Even, x-axis (latitude). Odd, y-axis (longitude)
            if axis % 2 == 0:
                points = sorted(points, key=lambda k: k.lat)
            else:
                points = sorted(points, key=lambda k: k.lon)

            # Get median point
            if len(points) % 2 == 0:
                m_index = int((len(points) / 2) - 1)
            else:
                m_index = int(len(points) // 2)
            median = points[m_index]

            # Give node a reference to parent node for ease of backtracking
            node = Node(
                Point(median.id, median.cat, median.lat, median.lon),
                left=None, right=None, parent=parent)

            self.node_count += 1

            # Slice and partition subsets as child nodes/subtrees
            left = self.partition(points[:m_index], axis + 1, node)
            right = self.partition(points[m_index + 1:], axis + 1, node)
            node.left = left
            node.right = right

            if node.point.id == "id716" or node.point.id == "id862" or node.point.id == "id300":
                print(node.point.id)

            return node

    def search(self, search_term: Point, k: int) -> [Point]:
        """
        Return k nearest neighbours of search_term co-ords and category
        1. Move down tree recursively, considerate of split and co-ord
            at each branch
        2. When leaf node reached, add node to saved closest neighbours.
        3. Backtrack node by node.
        4. If backtracked node closer than saved neighbour, add to saved list.
        5. Check other subtree of split only dist from target to current
            closest point > dist from target to split.
        """

        # Find k nearest neighbours
        self.neighbours = []
        self.forward_traverse(None, self.root, search_term, 0, k)

        # Flatten neighbour list to points-only.
        if self.neighbours:
            self.neighbours = sorted(self.neighbours, key=lambda k: k['dist'])

            for i in self.neighbours:
                print(i['dist'], i['point'])

            self.neighbours = [n['point'] for n in self.neighbours]

        return self.neighbours

    def forward_traverse(self, parent, cur_node, targ: Point, axis: int,
                         k: int, subtree=None):
        """
        Helper method for search()
        """

        backtrack = True

        if cur_node is not None:

            # Not even traversing these nodes, must be not exploring all relevant subtrees
            if cur_node.point.id == "id716" or cur_node.point.id == "id862" or cur_node.point.id == "id300":
                print(cur_node.point.id)
                sys.exit()

            p_hash = self.hash_point(cur_node.point)

            if p_hash not in self.t_closed_list:
                self.t_closed_list.append(p_hash)
            else:
                backtrack = False

            # Traverse child nodes if they exist
            # X-dim split, compare latitude
            if axis % 2 == 0:
                if targ.lat > cur_node.point.lat:
                    if cur_node.right is not None:
                        self.forward_traverse(cur_node, cur_node.right, targ,
                                              axis + 1, k, subtree="right")
                elif cur_node.left is not None:
                    self.forward_traverse(cur_node, cur_node.left,
                                          targ, axis + 1, k, subtree="left")

            # Y-dim split, compare longitude
            else:
                if targ.lon > cur_node.point.lon:
                    if cur_node.right is not None:
                        self.forward_traverse(cur_node, cur_node.right, targ,
                                              axis + 1, k, subtree="right")
                elif cur_node.left is not None:
                    self.forward_traverse(cur_node, cur_node.left,
                                          targ, axis + 1, k, subtree="left")

            # Save neighbour and backtrack when leaf nodes reached
            if cur_node.left:
                if not cur_node.left.left and not cur_node.left.right:
                    l_dist = cur_node.left.point.dist_to(targ)
                    print("leaf node:", l_dist, cur_node.left.point, "parent:", cur_node.left.parent.point.id)
                    self.save_neighbour(l_dist, cur_node.left.point, k, targ)
                    if backtrack:
                        self.backtrack(cur_node.left, targ, axis - 1, k, subtree)

            if cur_node.right:
                if not cur_node.right.left and not cur_node.right.right:
                    r_dist = cur_node.right.point.dist_to(targ)
                    print("leaf node:", r_dist, cur_node.right.point, "parent:", cur_node.right.parent.point.id)
                    self.save_neighbour(r_dist, cur_node.right.point, k, targ)
                    if backtrack:
                        self.backtrack(cur_node.right, targ, axis - 1, k, subtree)

    def backtrack(self, cur_node, targ: Point, axis: int, k: int,
                  subtree=None):
        """
        Helper method for search()
        """

        if cur_node:
            if cur_node.parent:
                print("backtracked to", cur_node.parent.point.id, "previous node was", subtree, "subtree")

                # Check if point should be saved as neighbour
                dist = cur_node.parent.point.dist_to(targ)
                if self.save_neighbour(dist, cur_node.parent.point, k, targ):
                    print("saved new neighbour point", cur_node.parent.point.id)

                # Traverse previously unexplored subtree(s)
                if subtree == "left" and cur_node.parent.right is not None:
                    self.forward_traverse(cur_node.parent, cur_node.parent.right,
                                          targ, axis + 1, k, subtree="right")

                elif subtree == "right" and cur_node.parent.left is not None:
                    self.forward_traverse(cur_node.parent, cur_node.parent.left,
                                          targ, axis + 1, k, subtree="left")

                # Keep backtracking until branches no longer valid
                tree = "right" if subtree == "left" else "left"
                self.backtrack(cur_node.parent.parent, targ, axis - 1, k, tree)

    def save_neighbour(self, dist, point: Point, k: int, targ: Point):
        """
        Helper method for search()
        Save to or overwrite an element of neighbours list with the
        incoming point.
        """

        p_hash = self.hash_point(point)

        if p_hash not in self.closed_list:

            # Save immediately if < k neighbours in list
            if len(self.neighbours) < k and point.cat == targ.cat:
                self.neighbours.append({
                    'dist': dist,
                    'point': point
                })
                self.closed_list.append(p_hash)
                return True

            # If k neighbours and cur_node dist > max(saved), replace max.
            elif len(self.neighbours) == k and point.cat == targ.cat:
                self.neighbours = sorted(self.neighbours,
                                         key=lambda k: k['dist'], reverse=True)
                if self.neighbours[0]['dist'] > dist:
                    del self.neighbours[0]
                    self.neighbours.append({
                        'dist': dist,
                        'point': point
                    })
                    self.closed_list.append(p_hash)
                    return True

        return False

    def add_point(self, point: Point) -> bool:
      
        pass

    def delete_point(self, point: Point) -> bool:
        result = False
        self.is_point_found = False
        prev_root = None
        #Method to traverse the kd-tree and check the point to be deleted
        #if the root is none, return
        def traverse_and_delete(root, point, axis=""):
            if root == None:
                return
        #Traverse left subtree 
            traverse_and_delete(root.left, point)
            #If the node doesn't have a right subtree, and the left tree is not none, swap the left subtree to the right
            if (root.right == None and root.left !=None):
                root.left.parent = root.parent
                root = root.left
                if (root.right !=None):
                    axis = root.splitAxis
                    smallest_x_or_y_coorinate = None
                    remove_node = root
                    root = root.right
                    while True:
                        if (root.left ==None):
                            if (smallest_x_or_y_coorinate !=None):
                                #Assigning new parent to the smallest coordinate
                                smallest_x_or_y_coorinate.parent = remove_node.parent
                                #Assign right node to the smallest coordinates right node
                                smallest_x_or_y_coorinate.right = remove_node.right
                                remove_node = None
                                return
                            else:
                                 if (root.left != None):
                                     root = root.left
                                 elif (root.right != None):
                                     root = root.right
                                 if  (root == None):
                                     if (smallest_x_or_y_coorinate !=None):
                                         #Remove parent node and assign new parent to the smallest coordinate
                                         smallest_x_or_y_coorinate.parent = remove_node.parent
                                         #Assign right node to the smallest coordinates right
                                         smallest_x_or_y_coorinate.right = remove_node.right 
                                         remove_node = None
                                         return
                                     else:
                                         smallest_x_or_y_coorinate = remove_node.right
                                         smallest_x_or_y_coorinate.parent = remove_node.parent
                                         remove_node = None
                                         return
                        else:
                            if (smallest_x_or_y_coorinate !=None):
                                smallest_x_or_y_coorinate.parent = remove_node.parent
                                smallest_x_or_y_coorinate.right = remove_node.right 
                                remove_node = None
                                return
                            else:
                                smallest_x_or_y_coorinate = remove_node.right
                                smallest_x_or_y_coorinate.parent = remove_node.parent
                                remove_node = None
                                return
                else:
                    root = root.left
                    if (root.splitAxis ==axis):
                        smallest_x_or_y_coorinate = root
                    #replace with the node on the right subtree with smallest x- or y- coordinate depending on axis of the node
                    # recursively remove that node            
                    root.right.parent = root.parent
                    root = root.right


            #if it's a leaf node, remove that node
            elif (root.right == None and root.left == None):
                if (root == root.parent.right):
                    root.parent.right = None
                elif (root == root.parent.left):
                    root.parent.left = None
                root=None    
                self.is_point_found = True
                return True


                

                                         
                                            
                                        
                


    def is_point_in(self, point: Point) -> bool:
        no_of_iterations = 0
        result = False

        self.is_point_found = False

        
            
        
        
        return result

    def hash_point(self, point) -> int:
        """
        Hash method provided in Point class kept giving me unsupported operand
        errors for flout ^ float sums. This implementation is the same but uses
        float * float instead instead of exponent.
        """

        hash_value = 7
        hash_value = 53 * hash_value + hash(point.id)
        hash_value = 53 * hash_value + hash(point.cat)
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
        Helper method for print
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