import numpy as np

def square_distance(array_1, array_2):
    return sum([(array_1[i] - array_2[i])**2 for i in range(len(array_1))])

def k_means_2(image_array):
    num_colors = image_array.shape[2]
    color_range = np.max(image_array)
    colors = []
    # create a list of all non-zero colours in the image
    for x in range(image_array.shape[0]):
        for y in range(image_array.shape[1]):
            color = image_array[x, y]
            if sum(color) != 0:
                colors.append(color)

    # initial guesses
    centers = [colors[0], colors[-1]]

    # Iterative k-means clustering, maximum 10 cycles
    for i in range(10):
        # assign
        sums = [[0]*num_colors, [0]*num_colors]
        num_points = [0, 0]
        for color in colors:
            assigned_center = 0 if square_distance(color, centers[0]) < square_distance(color, centers[1]) else 1
            for k in range(num_colors):
                sums[assigned_center][k] += color[k]
            num_points[assigned_center] += 1

        # update
        new_centers = [0, 0]
        for j in [0, 1]:
            if num_points[j] > 0:
                new_centers[j] = [sums[j][k]/num_points[j]
                    for k in range(num_colors)
                ]
            else:
                new_centers[j] = centers[j]

        if sum([square_distance(new_centers[j], centers[j]) for j in [0, 1]]) < color_range/256.0:
            # return early
            return new_centers
        else:
            centers = new_centers

    return centers

def k_means_2_test():
    points = np.array([[[0, 0], [1, 2], [3, 5], [5, 5], [4,5]]])
    print(k_means_2(points))

# k_means_2_test()
