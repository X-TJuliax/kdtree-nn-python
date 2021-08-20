from nearestNeigh.nearest_neigh import NearestNeigh
from nearestNeigh.point import Point
import math

# -----------------------------------------------------------------
# This class is required to be implemented. Kd-tree implementation.
#
# __author__ = 'Prodip Guha Roy'
# __copyright__ = 'Copyright 2021, RMIT University'
# 
# -----------------------------------------------------------------

def deg2rad(deg):
    """
    Convert degrees to radian.
    :return: Radian
    """
    return deg * math.pi / 180.0


def rad2deg(rad):
    """
    Convert radian to degrees.
    :return: Degrees
    """
    return (rad * 180.0) / math.pi
	
class NewPoint:                 
# This class is added to set left, right and parent attributes for each point
    def __init__(self):
        self.id = ""
        self.cat = ""
        self.lat = 0
        self.lon = 0
        self.right = None
        self.left = None
        self.parent = None
        
    def __str__(self):
        #converts the point data to string
        return 'Point{' + 'id=' + self.id + ', cat=' + self.cat.name + ", lat=" + str(self.lat) + ', lon=' + str(
            self.lon) + '}'
			
    def hash_point(self, point) -> int:
        
        hash_value = 7
        hash_value = 53 * hash_value + hash(self.id)
        hash_value = 53 * hash_value + hash(self.cat)
        hash_value = 53 * hash_value + int(self.lat ^ self.lat)
        hash_value = 53 * hash_value + int(self.lon ^ self.lon)
        return hash_value
		
    def dist_to(self, point: Point):        # method to get the distance between NewPoint class objects
        #computes the distance between two points
        theta = self.lon - point.lon
        dist = math.sin(deg2rad(self.lat)) * math.sin(deg2rad(point.lat)) + math.cos(deg2rad(self.lat)) * math.cos(
            deg2rad(point.lat)) * math.cos(deg2rad(theta))
        dist = math.acos(dist)
        dist = rad2deg(dist)
        dist = dist * 60 * 1.1515
        dist = dist * 1.609344
        return dist
		


class KDTreeNN(NearestNeigh):

    def __init__(self):
        
        self.points = None
        self.root_point = None
        self.distances = []
        self.is_point_found = False
        
    def build_index(self, points: [Point]):
        #self.points = points
        self.root_point = NewPoint()            
		# Setting the root node initial values
        self.root_point.id = points[0].id
        self.root_point.cat = points[0].cat
        self.root_point.lat = points[0].lat
        self.root_point.lon = points[0].lon

       
        
        for point_index in range(1,len(points)):
            no_of_iterations = 0                                        
			# Using to get the status of splliting around lat (x) or lon (y).
            parent_node = self.root_point
            while True:
                if (no_of_iterations%2 == 0):                           
				# Dividing around X axis
                    if (points[point_index].lat > parent_node.lat):     # Then gooes to the right of the parent
                        if (parent_node.right == None):
                            new_point = NewPoint()
                            new_point.id = points[point_index].id
                            new_point.cat = points[point_index].cat
                            new_point.lat = points[point_index].lat
                            new_point.lon = points[point_index].lon
                            #print (new_point)
                            parent_node.right = new_point
                            parent_node.right.parent = parent_node
                            #no_of_points += 1
                            break
                        else:
                            parent_node = parent_node.right
                            no_of_iterations += 1
                    else:
                        if (parent_node.left == None):
                            new_point = NewPoint()
                            new_point.id = points[point_index].id
                            new_point.cat = points[point_index].cat
                            new_point.lat = points[point_index].lat
                            new_point.lon = points[point_index].lon
                            parent_node.left = new_point
                            parent_node.left.parent = parent_node
                            break
                        else:
                            parent_node = parent_node.left
                            no_of_iterations += 1
                else:
                    if (points[point_index].lon > parent_node.lon):     
					# Then goes to the left of the parent
                        if (parent_node.right == None):
                            new_point = NewPoint()
                            new_point.id = points[point_index].id
                            new_point.cat = points[point_index].cat
                            new_point.lat = points[point_index].lat
                            new_point.lon = points[point_index].lon
                            parent_node.right = new_point
                            parent_node.right.parent = parent_node
                            break
                        else:
                            parent_node = parent_node.right
                            no_of_iterations += 1
                    else:
                        if (parent_node.left == None):
                            new_point = NewPoint()
                            new_point.id = points[point_index].id
                            new_point.cat = points[point_index].cat
                            new_point.lat = points[point_index].lat
                            new_point.lon = points[point_index].lon
                            parent_node.left = new_point
                            parent_node.left.parent = parent_node
                            break
                        else:
                            parent_node = parent_node.left
                            no_of_iterations += 1
                            
            


    def inorder(self, root, search_term: Point):          # Method to traverse through kd-tree (in-order traversal) and add each point and there distance with respect to search point 
        
        if root==None:              
		#if root is None,return
            return
        
        self.inorder(root.left, search_term)            
		#traverse left subtree
        
                
        
        if (root.cat == search_term.cat):               
		#traverse current node
            self.distances.append({
                'dist': root.dist_to(search_term),
                'point': root
            })
            
        self.inorder(root.right, search_term)           
		#traverse right subtree
        	
    def search(self, search_term: Point, k: int) -> [Point]:
        self.distances = []
        self.inorder(self.root_point, search_term)      
        
        sorted_distances = sorted(self.distances, key=lambda k: k['dist'])

        k_neighbours = [i['point'] for i in sorted_distances[:k]]

        return k_neighbours
		
		


    def add_point(self, point: Point) -> bool:
        # To be implemented.
        pass

    def delete_point(self, point: Point) -> bool:
        result = False
        no_of_iterations = 0
        parent_node = self.root_point           
		# Setting the initial parent as root node of kd-tree
        
        while True:
            if (parent_node == None):
                break
            if (no_of_iterations%2 == 0): 
            # Divide around X axis			
                if (point.lat > parent_node.lat):     
				# Then go to right of the parent
                    if (parent_node.right == None):
                        break
                    else:
                        if (parent_node.right.id == point.id and parent_node.right.cat == point.cat and parent_node.right.lon == point.lon and parent_node.right.lat == point.lat):
                            result = True
                            if (parent_node.right.left == None):
                                parent_node.right = None
                            else:
                                parent_node.right.left.parent = parent_node.parent
                                parent_node.right = parent_node.right.left
                                # If point found Removing the right node assigning it's left child node								
                            break
                        parent_node = parent_node.right
                        no_of_iterations += 1
                else:
                    if (parent_node.left == None):
                        break
                    else:
                        if (parent_node.left.id == point.id and parent_node.left.cat == point.cat and parent_node.left.lon == point.lon and parent_node.left.lat == point.lat):
                            result = True
                            if (parent_node.left.left == None):
                                parent_node.left = None
                            else:
                                parent_node.left.left.parent = parent_node.parent
                                parent_node.left = parent_node.left.left                    
								# If point found Removing the left node assigning it's left child node
                            break
                        parent_node = parent_node.left
                        no_of_iterations += 1
            else:
                if (point.lon > parent_node.lon):     
				# Then go to left of the parent
                    if (parent_node.right == None):
                        break
                    else:
                        if (parent_node.right.id == point.id and parent_node.right.cat == point.cat and parent_node.right.lon == point.lon and parent_node.right.lat == point.lat):
                            result = True
                            if (parent_node.right.left == None):
                                parent_node.right = None
                            else:
                                parent_node.right.left.parent = parent_node.parent
                                parent_node.right = parent_node.right.left                    
								# If point found Removing the right node assigning it's left child node
                            break
                        parent_node = parent_node.right
                        no_of_iterations += 1
                else:
                    if (parent_node.left == None):
                        break
                    else:
                        if (parent_node.left.id == point.id and parent_node.left.cat == point.cat and parent_node.left.lon == point.lon and parent_node.left.lat == point.lat):
                            result = True
                            if (parent_node.left.left == None):
                                parent_node.left = None
                            else:
                                parent_node.left.left.parent = parent_node.parent
                                parent_node.left = parent_node.left.left                    
								# If point found Removing the left node assigning it's left child node
                            break
                        parent_node = parent_node.left
                        no_of_iterations += 1

        return result
        

    def is_point_in(self, point: Point) -> bool:
        
        pass
