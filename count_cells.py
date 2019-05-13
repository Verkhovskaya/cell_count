from file_utils import save_image, load_image, image_add_location_data, get_distance_to, show_image, merge_images, simplify_image, print_image
from k_means import k_means_2
import numpy as np
import sys
from scipy.signal import convolve2d
import os
path = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.setrecursionlimit(100000)


class Cell:
    def __init__(self, array, x, y):
     self.array = array
     self.x = x
     self.y = y

cells_global = []
def split_into_two_major_colors(image_array):
    colors = k_means_2(simplify_image(image_array, 10, 10))
    distances = []
    for i in range(len(colors)):
        distances.append(get_distance_to(image_array, colors[i]))
    overlays = []
    for i in range(len(colors)):
        is_closest = np.zeros(image_array.shape[:2]) + 1
        for j in range(len(colors)):
            is_closest = is_closest * (distances[i] <= distances[j])
        overlays.append(is_closest)
    return overlays


def split_into_individual_cells(cell_overlay, image_array):
    image_copy = np.copy(cell_overlay)
    cells = []
    for x in range(cell_overlay.shape[0]):
        for y in range(cell_overlay.shape[1]):
            found_locations = []
            map_cell(found_locations, image_copy, x, y)
            if len(found_locations) > 0:
              x_start = min([location[0] for location in found_locations])
              y_start = min([location[1] for location in found_locations])
              new_overlay = array_overlay_from_found_locations(found_locations, image_array)
              if np.sum(np.sum(new_overlay))/(new_overlay.shape[0]*new_overlay.shape[1]) > 0.5:
                     cells.append(Cell(new_overlay, x_start, y_start))
    return cells


def array_overlay_from_found_locations(found_locations, image_array):
    min_x = min([point[0] for point in found_locations])
    max_x = max([point[0] for point in found_locations]) + 1
    min_y = min([point[1] for point in found_locations])
    max_y = max([point[1] for point in found_locations]) + 1
    new_array = np.zeros(list(np.concatenate(((max_x-min_x, max_y-min_y), image_array.shape[2:]))))
    for point in found_locations:
        new_array[point[0]-min_x, point[1]-min_y] = image_array[point[0], point[1]]
    return new_array


def map_cell(found_locations, image_array, x, y):
    if x < image_array.shape[0] and y < image_array.shape[1] and x >= 0 and y >= 0:
        if image_array[x,y]:
            found_locations.append((x,y))
            image_array[x,y] = False
            map_cell(found_locations, image_array, x+1, y)
            map_cell(found_locations, image_array, x, y+1)
            map_cell(found_locations, image_array, x-1, y)
            map_cell(found_locations, image_array, x, y-1)


def get_cell_overlay(overlays):
    overlay = overlays[0]
    if (np.sum(overlay[0,:]) + np.sum(overlay[:,0]) + np.sum(overlay[-1,:]) + np.sum(overlay[:,-1]))/(overlay.shape[0] + overlay.shape[1])/2 < 0.5:
        return overlay
    else:
        return overlays[1]


def get_cells(image, min_cell_side=None):
    overlays = split_into_two_major_colors(image)
    cell_overlay = get_cell_overlay(overlays)
    cells = split_into_individual_cells(cell_overlay, image)
    if min_cell_side == None:
        min_cell_side = max(max([cell.array.shape[0] for cell in cells]), max([cell.array.shape[1] for cell in cells])) / 8
    print(min_cell_side)
    print(len(cells))
    cells = list(filter(lambda cell: cell.array.shape[0] > min_cell_side and cell.array.shape[1] > min_cell_side, cells))

    if len(cells) <= 1:
        return cells
    else:
        all_cells = []
        for cell in cells:
            split_cells = get_cells(cell.array, min_cell_side)
            if len(split_cells) > 1:
                for new_cell in split_cells:
                    new_cell.x += cell.x
                    new_cell.y += cell.y
                    all_cells.append(new_cell)
            else:
                all_cells.append(cell)
        return all_cells


def draw_outline(image_array, cells):
    new_image = np.copy(image_array)
    for cell in cells:
        array = cell.array
        x_center = int(cell.x+array.shape[0]/2)
        y_center = int(cell.y+array.shape[1]/2)
        new_image[cell.x:cell.x+array.shape[0],y_center-1: y_center+2] = [np.max(image_array),0,0]
        new_image[x_center-1:x_center+2,cell.y:cell.y+array.shape[1]] = [np.max(image_array),0,0]
    return new_image


def convert_image(in_name, out_name):
    image = load_image(path + in_name)
    cells = get_cells(image)
    save_image(draw_outline(image, cells), name=out_name)
    return len(cells)

def test():
    print(convert_image('test_in.jpg', 'test_out.jpg'))
# test()


def generate_cells_mask(image, cells):
    mask = np.zeros((image.shape[0], image.shape[1]))
    for cell in cells:
       for x in range(cell.array.shape[0]):
          for y in range(cell.array.shape[1]):
              if sum(cell.array[x,y]) > 0:
                  mask[cell.x+x,cell.y+y] = 1
    return mask

def test2():
    print(convert_image('test2.png', 'test2_out.png'))
    image = load_image('test2.png')
    overlays = split_into_two_major_colors(image)
    # cell_overlay = get_cell_overlay(overlays)
    # show_image(cell_overlay)
    cells = get_cells(image)
    show_image(generate_cells_mask(image, cells))
    
# test2()