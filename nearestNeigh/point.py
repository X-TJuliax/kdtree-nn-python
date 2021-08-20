from nearestNeigh.category import Category
import math

# -------------------------------------------------
# __author__ = 'Prodip Guha Roy'
# __copyright__ = 'Copyright 2021, RMIT University'
# 
# -------------------------------------------------


def deg2rad(deg):
    """
    Convert degrees to radian.
    :param deg: Degrees to convert to radian
    :return: Radian
    """
    return deg * math.pi / 180.0


def rad2deg(rad):
    """
    Convert radian to degrees.
    :param rad: Radian to convert to degrees.
    :return: Degrees
    """
    return (rad * 180.0) / math.pi


def parse_cat(cat_str) -> Category:
    """
    Cast str to Category
    :param cat_str: str of a Category
    :return: Category
    """
    if cat_str.lower() == Category.RESTAURANT.name.lower():
        cat = Category.RESTAURANT
    elif cat_str.lower() == Category.EDUCATION.name.lower():
        cat = Category.EDUCATION
    elif cat_str.lower() == Category.HOSPITAL.name.lower():
        cat = Category.HOSPITAL
    else:
        print("Unknown Category: ", cat_str)

    return cat


# Class representing a point in the assignment
class Point:
    def __init__(self, id, cat: Category, lat, lon):
        self.id = id
        self.cat = cat
        self.lat = lat
        self.lon = lon

    def __str__(self):
        """
        Convert Point data to string
        """
        return 'Point{' + 'id=' + self.id + ', cat=' + self.cat.name + ", lat=" + str(self.lat) + ', lon=' + str(
            self.lon) + '}'

    def __eq__(self, other):
        """
        Equality for a point
        :param other: object of type Point to compare
        :return: True if equal, otherwise False
        """

        if self is other:
            return True

        if other is None:
            return False

        if isinstance(other, self.__class__):
            if self.lat != other.lat:
                return False

            if self.lon != other.lon:
                return False

            if self.id != other.id:
                return False

            if self.cat != other.cat:
                return False
        else:
            return False

        return True

    def __ne__(self, other):
        """
        Inequality for a point
        :param other: object of type Point to compare
        :return: False is equal, otherwise True
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Hashing for point
        :return: hash
        """
        hash_value = 7
        hash_value = 53 * hash_value + hash(self.id)
        hash_value = 53 * hash_value + hash(self.cat)
        hash_value = 53 * hash_value + int(self.lat ^ self.lat)
        hash_value = 53 * hash_value + int(self.lon ^ self.lon)
        return hash_value


    def dist_to(self, point):
        """
        Computes the distance between two Points, for nearest neighbour searches.
        Use this to compare your distances
        :param point: Point to compute distance to, from self point object
        :return: Distance
        """
        theta = self.lon - point.lon
        dist = math.sin(deg2rad(self.lat)) * math.sin(deg2rad(point.lat)) + math.cos(deg2rad(self.lat)) * math.cos(
            deg2rad(point.lat)) * math.cos(deg2rad(theta))
        dist = math.acos(dist)
        dist = rad2deg(dist)
        dist = dist * 60 * 1.1515
        dist = dist * 1.609344
        return dist


def parse_point(string: str) -> Point:
    """
    cast string to Point, assuming format of __str__() of Point class
    :param string: string to cast
    :return: Point object
    """
    info = string[string.index('{')+1:string.index('}')]
    fields = info.split(',')
    field = fields[0]
    point_id = field[field.index('=')+1:]
    field = fields[1]
    cat = parse_cat(field[field.index('=')+1:])
    field = fields[2]
    lat = float(field[field.index('=')+1:])
    field = fields[3]
    lon = float(field[field.index('=')+1:])

    point = Point(point_id, cat, lat, lon)
    print(str(point))
    return point
