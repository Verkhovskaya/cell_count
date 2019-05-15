import tensorflow as tf
    
def square_distance(array_1, array_2):
    return tf.reduce_sum(tf.square(tf.subtract(array_1, array_2)))

def k_means_2_internal(image_array):
    shape = tf.shape(image_array)
    num_colors = tf.multiply(shape[0], shape[1])
    color_size = shape[2]
    colors = tf.reshape(image_array, [num_colors, color_size])
    color_range = tf.reduce_max(colors)
    color_sums = tf.reduce_sum(colors, axis=1)
    zeros = tf.cast(tf.zeros_like(color_sums),dtype=tf.bool)
    ones = tf.cast(tf.ones_like(color_sums),dtype=tf.bool)
    non_zero_mask = tf.where(color_sums>0,ones,zeros)
    non_zero_colors = tf.boolean_mask(colors, non_zero_mask)
    center_1 = non_zero_colors[0]
    center_2 = non_zero_colors[-1]

    def one_iteration_kmeans(center_1, center_2, _):
        # assign
        distances_1 = tf.reduce_sum(tf.square(tf.subtract(non_zero_colors, center_1)), axis=1)
        distances_2 = tf.reduce_sum(tf.square(tf.subtract(non_zero_colors, center_2)), axis=1)
        zeros = tf.cast(tf.zeros_like(distances_1),dtype=tf.bool)
        ones = tf.cast(tf.ones_like(distances_1),dtype=tf.bool)
        closest_to_1_mask = tf.where(distances_1<distances_2, ones, zeros)
        closest_to_1 = tf.boolean_mask(non_zero_colors, closest_to_1_mask)
        closest_to_2 = tf.boolean_mask(non_zero_colors, tf.logical_not(closest_to_1_mask))
        
        # update
        center_1_new = tf.reduce_mean(closest_to_1, axis=0)
        center_2_new = tf.reduce_mean(closest_to_2, axis=0)#/2 #tf.shape(closest_to_2)[0]
        change = square_distance(center_1_new, center_1) + square_distance(center_2_new, center_2)
        return center_1_new, center_2_new, change
    
    def repeat_condition(_, __, change):
        return tf.less(256/color_range, change)
    
    return tf.while_loop(
        repeat_condition,
        one_iteration_kmeans,
        loop_vars=[non_zero_colors[0], non_zero_colors[-1], 2*256/color_range])[:2]


session = tf.Session()
def k_means_2(image_array):
    global session
    image_array_tensor = tf.convert_to_tensor(image_array)
    return session.run(k_means_2_internal(image_array_tensor))

def test():
    data = [[[0,0,0], [1,1,1],[1,2,1],[5,5,5],[6.0,6,6]]]
    print(k_means_2(data))
# test()