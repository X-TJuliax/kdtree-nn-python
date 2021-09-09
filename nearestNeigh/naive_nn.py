from nearestNeigh.nearest_neigh import NearestNeigh
from nearestNeigh.point import Point


class NaiveNN(NearestNeigh):

    def __init__(self):

        self.points = None

    def build_index(self, points: [Point]):
        """
        Stores list of points for future queries.
        """

        # No DS, list used as is.
        self.points = points

    def search(self, search_term: Point, k: int) -> [Point]:
        """
        Return k nearest neighbours of search_term co-ords and category
        """

        # Calculate distance of all points relative to input point
        distances = []
        for point in self.points:

            # Only consider distance if category matches
            if point.cat == search_term.cat:
                distances.append({
                    'dist': point.dist_to(search_term),
                    'point': point
                })

        # Sort by distance
        sorted_distances = sorted(distances, key=lambda k: k['dist'])

        # Slice for k neighbours
        k_neighbours = [i['point'] for i in sorted_distances[:k]]

        for n in sorted_distances:
            print(n['point'].id, "dist:", n['dist'])

        return k_neighbours

    def add_point(self, point: Point) -> bool:

        result = False

        # Check if the point exists
        exists = False
        for index, p in enumerate(self.points):
            if p.id == point.id and p.cat == point.cat and p.lon == point.lon and p.lat == point.lat:
                exists = True

        # Add if it doesnt exist
        if not exists:
            self.points.append(point)
            result = True

        return result

    def delete_point(self, point: Point) -> bool:

        result = False

        # Find the points index
        target = None
        for index, p in enumerate(self.points):
            if p.id == point.id and p.cat == point.cat and p.lon == point.lon and p.lat == point.lat:
                target = index

        # Delete if it exists
        if target is not None:
            del self.points[target]
            result = True

        return result


    def is_point_in(self, point: Point) -> bool:

        result = False

        # Check if the point exists
        for index, p in enumerate(self.points):
            if p.id == point.id and p.cat == point.cat and p.lon == point.lon and p.lat == point.lat:
                result = True

        return result
