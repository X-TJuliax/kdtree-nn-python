import sys
from nearestNeigh.nearest_neigh import NearestNeigh
from nearestNeigh.naive_nn import NaiveNN
from nearestNeigh.kd_tree_nn import KDTreeNN
from nearestNeigh.point import Point, parse_cat, parse_point


# -------------------------------------------------------------------
# This is the entry point to run the program in file-based mode.
# It uses the data file to initialise the set of points.
# It takes a command file as input and output into the output file.
# Refer to usage() for exact format of input expected to the program.
#
# __author__ = 'Prodip Guha Roy'
# __copyright__ = 'Copyright 2021, RMIT University'
#
# -------------------------------------------------------------------

def usage():
    """
    Print help/usage message.
    """
    print('python nearest_neigh_file_based.py', '<approach> [data fileName] [command fileName] [output fileName]')
    print('<approach> = <naive | kdtree>')
    sys.exit(1)


if __name__ == '__main__':
    # Fetch the command line arguments
    args = sys.argv

    if len(args) != 5:
        print('Incorrect number of arguments.')
        usage()

    # initialise search agent
    agent: NearestNeigh = None
    if args[1] == 'naive':
        agent = NaiveNN()
    elif args[1] == 'kdtree':
        agent = KDTreeNN()
    else:
        print('Incorrect argument value.')
        usage()

    # read from data file to populate the initial set of points
    data_filename = args[2]
    points = []
    try:
        data_file = open(data_filename, 'r')
        for line in data_file:
            values = line.split()
            point_id = values[0]
            cat = parse_cat(values[1])
            lat = float(values[2])
            lon = float(values[3])
            point = Point(point_id, cat, lat, lon)
            points.append(point)

        data_file.close()
        agent.build_index(points)
    except FileNotFoundError as e:
        print("Data file doesn't exist.")
        usage()

    command_filename = args[3]
    output_filename = args[4]
    # Parse the commands in command file
    try:
        command_file = open(command_filename, 'r')
        output_file = open(output_filename, 'w')

        for line in command_file:
            command_values = line.split()
            command = command_values[0]
            # search
            if command == 'S':
                cat = parse_cat(command_values[1])
                lat = float(command_values[2])
                lon = float(command_values[3])
                k = int(command_values[4])
                point = Point("searchTerm", cat, lat, lon)
                search_result = agent.search(point, k)
                if search_result:
                    for search_point in search_result:
                        output_file.write(str(search_point) + '\n')

            # add
            elif command == 'A':
                point_id = command_values[1]
                cat = parse_cat(command_values[2])
                lat = float(command_values[3])
                lon = float(command_values[4])
                point = Point(point_id, cat, lat, lon)
                if not agent.add_point(point):
                    output_file.write('Add point failed.\n')

            # delete
            elif command == 'D':
                point_id = command_values[1]
                cat = parse_cat(command_values[2])
                lat = float(command_values[3])
                lon = float(command_values[4])
                point = Point(point_id, cat, lat, lon)
                if not agent.delete_point(point):
                    output_file.write('Delete point failed.\n')

            # check
            elif command == 'C':
                point_id = command_values[1]
                cat = parse_cat(command_values[2])
                lat = float(command_values[3])
                lon = float(command_values[4])
                point = Point(point_id, cat, lat, lon)
                output_file.write(str(agent.is_point_in(point)) + '\n')

            else:
                print('Unknown command.')
                print(line)

        output_file.close()
        command_file.close()
    except FileNotFoundError as e:
        print("Command file doesn't exist.")
        usage()
