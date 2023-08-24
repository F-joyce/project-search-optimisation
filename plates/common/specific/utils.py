import numpy as np

def reshape_plates_arrays_pop(pop_plate_1d,
                              height_points=10,
                              width_points=50):
    pop_plate_1d = np.array(pop_plate_1d)
    size = pop_plate_1d.shape[0]
    pop_plate_2d = pop_plate_1d.reshape(size,height_points,width_points)
    return pop_plate_2d