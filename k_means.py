import numpy as np

def square_distance(array_1, array_2):
    return sum([(array_1[i] - array_2[i])**2 for i in range(len(array_1))])

def k_means_2(image_array):
    print('calculating k_means_2')
    num_colors = image_array.shape[2]
    color_range = np.max(image_array)
    centers = [[0]*num_colors, [color_range]*num_colors]

    for i in range(10):
        # assign
        sums = [[0]*num_colors, [0]*num_colors]
        num_points = [0, 0]
        for x in range(image_array.shape[0]):
            for y in range(image_array.shape[1]):
                point = image_array[x, y]
                if sum(point) != 0:
                    assigned_center = 0 if square_distance(point, centers[0]) < square_distance(point, centers[1]) else 1
                    for k in range(num_colors):
                        sums[assigned_center][k] += point[k]
                    num_points[assigned_center] += 1

        # update
        new_centers = [0, 0]
        for j in [0, 1]:
            if num_points[j] > 0:
                new_centers[j] = [sums[j][k]/num_points[j]
                    for k in range(num_colors)
                ]
            else:
                new_centers[j] = [color_range/2] * num_colors
        # print(new_centers, i)

        if sum([square_distance(new_centers[j], centers[j]) for j in [0, 1]]) < color_range/256.0:
            return new_centers
        else:
            centers = new_centers
    print('Issues converging')
    return centers

def k_means_2_test():
    points = np.array([[[0, 0], [1, 2], [3, 5], [5, 5]]])
    k_means_2(points)

# k_means_2_test()


def none(centers):
    return centers