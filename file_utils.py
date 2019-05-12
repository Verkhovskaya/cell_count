import numpy as np
import matplotlib.pyplot as plt
import math
import os
path = os.path.dirname(os.path.abspath(__file__))

def load_image(image_path):
    print('Loading image')
    return plt.imread(image_path)

def print_image(image_array):
    simple = simplify_image(image_array, 25, 25)
    if len(image_array.shape) == 2:
        for line in simple:
            print(''.join([str(int(x)) for x in line]))
    else:
        for line in simple:
            print(''.join(['1' if x[0] > 0 else '0' for x in line]))


def simplify_image(image_array, new_x, new_y):
    if image_array.shape[0] <= new_x or image_array.shape[1] <= new_y:
        return image_array
    x_scale = 1.0*image_array.shape[0]/new_x
    y_scale = 1.0*image_array.shape[1]/new_y
    if len(image_array.shape) == 2:
        new_image = np.zeros((new_x, new_y))
    else:
        new_image = np.zeros((new_x, new_y, image_array.shape[2]))
    for x in range(new_x):
        for y in range(new_y):
            image_x = int(x*x_scale)
            image_y = int(y*y_scale)
            new_image[x, y] = image_array[image_x, image_y]
    return new_image

def image_add_location_data(image_array, keep_location=False, cluster_factor=40):
    print('Converting image to points')
    new_array = []
    for x in range(image_array.shape[0]):
        for y in range(image_array.shape[1]):
            if keep_location:
                new_array.append(np.concatenate((image_array[x,y],[x/image_array.shape[0]*cluster_factor,y/image_array.shape[1]*cluster_factor])))
            else:
                new_array.append(image_array[x,y])
    return np.array(new_array)

def get_distance_to(image_array, color_array):
    if len(color_array) != image_array.shape[2]:
        raise Exception("Dimensions don't match")
    new_array = np.zeros((image_array.shape[0], image_array.shape[1]))
    for x in range(image_array.shape[0]):
        for y in range(image_array.shape[1]):
            new_array[x,y] = sum([(color_array[i] - image_array[x,y,i])**2 for i in range(len(color_array))])**0.5
    return np.array(new_array)

def show_image(image_array):
    plt.imshow(image_array)
    plt.show()

def save_image(image_array, name='out.jpg'):
    plt.imsave(path+name, image_array)

def merge_images(image_arrays):
    num_across = int(len(image_arrays)**0.5)
    num_down = math.ceil(1.0*len(image_arrays)/num_across)
    image_rows = [image_arrays[y*num_across:(y+1)*num_across] for y in range(num_down)]
    row_heights = [max([image.shape[1] for image in row]) for row in image_rows]
    total_width = max([sum([image.shape[0]+1 for image in row])+1 for row in image_rows])
    new_image = np.zeros(np.concatenate(([total_width+1, sum(row_heights)+len(row_heights)+1], image_arrays[0].shape[2:])))+0.3
    y_offset = 1
    for row_id in range(len(image_rows)):
        row = image_rows[row_id]
        x_offset = 1
        for image in row:
            new_image[x_offset:x_offset+image.shape[0],y_offset:y_offset + image.shape[1]] = image
            x_offset += image.shape[0] + 1
        y_offset += row_heights[row_id] + 1
    return new_image

def kmeans(points_array, num_colors):
    print('Running kmeans, looking for ' + str(num_colors) + ' clusters')
    kmeans = 0 # KMeans(n_clusters=num_colors, random_state=0).fit(points_array)
    return kmeans.cluster_centers_
