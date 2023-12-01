import numpy as np

def distance_point_filter(points, boundaries, labels=None):
    min_x = boundaries['min_x']
    max_x = boundaries['max_x']

    min_y = boundaries['min_y']
    max_y = boundaries['max_y']
    
    min_z = boundaries['min_z']
    max_z = boundaries['max_z']

    # Удаление точек, выходящих за рамки x,y,z
    mask = np.where((points[:, 0] >= min_x) & (points[:, 0] <= max_x) & (points[:, 1] >= min_y) & (
                points[:, 1] <= max_y) & (points[:, 2] >= min_z) & (points[:, 2] <= max_z))
    points = points[mask]
    labels = labels[mask]

    points[:, 2] = points[:, 2] + 2
    return points, labels