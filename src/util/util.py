


def get_lane_points(points_path):
    lane_points = [[0, 0] for i in range(4)]
    points_file = open(points_path, "r")
    for i in range(4):
        lane_points[i] = [int(i) for i in points_file.readline().strip().split(',')]
    return lane_points