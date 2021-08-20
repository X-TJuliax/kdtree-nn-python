from nearestNeigh.point import Point


# -------------------------------------------------
# Base class for nearest neighbour approaches.
#
# __author__ = 'Prodip Guha Roy'
# __copyright__ = 'Copyright 2021, RMIT University'
# 
# -------------------------------------------------
class NearestNeigh:

    def build_index(self, points: [Point]):
        """
        construct the data structure to store nodes
        :param points: nodes to be stored
        """
        pass

    def search(self, search_term: Point, k: int) -> [Point]:
        """
        search for nearby points
        :param search_term: The query point which passes information such as category and location
        :param k: number of points that should be searched
        :return: a list of k point as search result
        """
        pass

    def add_point(self, point: Point) -> bool:
        """
        add a point to the data structure
        :param point: point to be added
        :return: whether succeeded, e.g. return False when point is already in the data structure
        """
        pass

    def delete_point(self, point: Point) -> bool:
        """
        delete a point from data structure. Be aware that even when the object are not in the data stucture,
        the identical point in the data structure should be deleted
        :param point: point to be deleted
        :return: whether succeeded, e.g. return False when point not found
        """
        pass

    def is_point_in(self, point: Point) -> bool:
        """
        Check whether the point is in the data structure
        :param point: point to be checked
        :return: True if point is present
        """
        pass
