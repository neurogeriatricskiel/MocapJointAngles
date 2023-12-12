""" 3D plot the markers and local anatomical coordinate systems (stretch the Z axis (pointing up) to account for plotting markers of a standing human)"""

import matplotlib.pyplot as plt
import numpy as np

def plot_3d(static_data, TAnatShank_right, TAnatThigh_right, TAnatShank_left, TAnatThigh_left, TrefShank_right,
                                                   TrefThigh_right, TrefShank_left, TrefThigh_left, sample_no):    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for variable_name, coordinates_static in static_data.items():
        
        x, y, z = coordinates_static[0, sample_no], coordinates_static[1, sample_no], coordinates_static[2, sample_no] 

    ax.set_box_aspect([1, 0.5, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('All markers')
    
    # rigth side


    # PLOTTING ANATOMICAL COORDINATE SYSTEM FOR THE RIGHT SHANK

    # origin's position expressed in global coordinate system coordinates
    origin_shank_right_anat = np.dot(TrefShank_right, TAnatShank_right[:4, 3])

    x_axis_shank_right_anat = TAnatShank_right[:3, 0]
    y_axis_shank_right_anat = TAnatShank_right[:3, 1]
    z_axis_shank_right_anat = TAnatShank_right[:3, 2]


    scaling_factor = 0.1

    ax.quiver(origin_shank_right_anat[0], origin_shank_right_anat[1], origin_shank_right_anat[2],
            x_axis_shank_right_anat[0] * scaling_factor, x_axis_shank_right_anat[1] * scaling_factor, x_axis_shank_right_anat[2] * scaling_factor,
            color='r', label='U axis', length=1)

    ax.quiver(origin_shank_right_anat[0], origin_shank_right_anat[1], origin_shank_right_anat[2],
            y_axis_shank_right_anat[0] * scaling_factor, y_axis_shank_right_anat[1] * scaling_factor, y_axis_shank_right_anat[2] * scaling_factor,
            color='g', label='V axis', length=1)

    ax.quiver(origin_shank_right_anat[0], origin_shank_right_anat[1], origin_shank_right_anat[2],
            z_axis_shank_right_anat[0] * scaling_factor, z_axis_shank_right_anat[1] * scaling_factor, z_axis_shank_right_anat[2] * scaling_factor,
            color='b', label='W axis', length=1)
    

    # PLOTTING REFERENCE (CLUSTER) COORDINATE SYSTEM FOR THE RIGHT SHANK

    # right side

    x_axis_shank_right_clust = TrefShank_right[:3, 0]
    y_axis_shank_right_clust = TrefShank_right[:3, 1]
    z_axis_shank_right_clust = TrefShank_right[:3, 2]
    origin_shank_right_clust = TrefShank_right[:3, 3] # origin is the 4th column in the transformation matrix


    scaling_factor = 0.1

    ax.quiver(origin_shank_right_clust[0], origin_shank_right_clust[1], origin_shank_right_clust[2],
            x_axis_shank_right_clust[0] * scaling_factor, x_axis_shank_right_clust[1] * scaling_factor, x_axis_shank_right_clust[2] * scaling_factor,
            color='orange', label='U axis', length=1)

    ax.quiver(origin_shank_right_clust[0], origin_shank_right_clust[1], origin_shank_right_clust[2],
            y_axis_shank_right_clust[0] * scaling_factor, y_axis_shank_right_clust[1] * scaling_factor, y_axis_shank_right_clust[2] * scaling_factor,
            color='teal', label='V axis', length=1)

    ax.quiver(origin_shank_right_clust[0], origin_shank_right_clust[1], origin_shank_right_clust[2],
            z_axis_shank_right_clust[0] * scaling_factor, z_axis_shank_right_clust[1] * scaling_factor, z_axis_shank_right_clust[2] * scaling_factor,
            color='purple', label='W axis', length=1)
    


    # PLOTTING ANATOMICAL COORDINATE SYSTEM FOR THE RIGHT THIGH
    """ Plot the anatomical (thigh) coordinate system, computed from the thigh marker cluster, in the global coordinate frame""" # CORRECT THE DESCRIPTION
    origin_thigh_right_anat = np.dot(TrefThigh_right, TAnatThigh_right[:4, 3])
    x_axis_thigh_right_anat = TAnatThigh_right[:3, 0]
    y_axis_thigh_right_anat = TAnatThigh_right[:3, 1]
    z_axis_thigh_right_anat = TAnatThigh_right[:3, 2]


    scaling_factor = 0.1

    ax.quiver(origin_thigh_right_anat[0], origin_thigh_right_anat[1], origin_thigh_right_anat[2],
            x_axis_thigh_right_anat[0] * scaling_factor, x_axis_thigh_right_anat[1] * scaling_factor, x_axis_thigh_right_anat[2] * scaling_factor,
            color='r', length=1)

    ax.quiver(origin_thigh_right_anat[0], origin_thigh_right_anat[1], origin_thigh_right_anat[2],
            y_axis_thigh_right_anat[0] * scaling_factor, y_axis_thigh_right_anat[1] * scaling_factor, y_axis_thigh_right_anat[2] * scaling_factor,
            color='g', length=1)

    ax.quiver(origin_thigh_right_anat[0], origin_thigh_right_anat[1], origin_thigh_right_anat[2],
            z_axis_thigh_right_anat[0] * scaling_factor, z_axis_thigh_right_anat[1] * scaling_factor, z_axis_thigh_right_anat[2] * scaling_factor,
            color='b', length=1)


    # PLOTTING REFERENCE (CLUSTER) COORDINATE SYSTEM FOR THE RIGHT THIGH

    """ Plot the local (thigh) coordinate system, computed from the thigh amrker cluster, in the glocal coordinate frame""" 
    x_axis_thigh_right_clust = TrefThigh_right[:3, 0]
    y_axis_thigh_right_clust = TrefThigh_right[:3, 1]
    z_axis_thigh_right_clust = TrefThigh_right[:3, 2]
    origin_thigh_right_clust = TrefThigh_right[:3, 3] # origin is the 4th column in the transformation matrix

    scaling_factor = 0.1

    ax.quiver(origin_thigh_right_clust[0], origin_thigh_right_clust[1], origin_thigh_right_clust[2],
            x_axis_thigh_right_anat[0] * scaling_factor, x_axis_thigh_right_clust[1] * scaling_factor, x_axis_thigh_right_clust[2] * scaling_factor,
            color='orange', length=1)

    ax.quiver(origin_thigh_right_clust[0], origin_thigh_right_clust[1], origin_thigh_right_clust[2],
            y_axis_thigh_right_clust[0] * scaling_factor, y_axis_thigh_right_clust[1] * scaling_factor, y_axis_thigh_right_clust[2] * scaling_factor,
            color='teal', length=1)

    ax.quiver(origin_thigh_right_clust[0], origin_thigh_right_clust[1], origin_thigh_right_clust[2],
            z_axis_thigh_right_clust[0] * scaling_factor, z_axis_thigh_right_clust[1] * scaling_factor, z_axis_thigh_right_clust[2] * scaling_factor,
            color='purple', length=1)



    # left side


    # PLOTTING ANATOMICAL COORDINATE SYSTEM FOR THE LEFT SHANK
    origin_shank_left_anat = np.dot(TrefShank_left, TAnatShank_left[:4, 3]) # origin is the 4th column in the transformation matrix
    x_axis_shank_left_anat = TAnatShank_left[:3, 0]
    y_axis_shank_left_anat = TAnatShank_left[:3, 1]
    z_axis_shank_left_anat = TAnatShank_left[:3, 2]

    scaling_factor = 0.1

    ax.quiver(origin_shank_left_anat[0], origin_shank_left_anat[1], origin_shank_left_anat[2],
            x_axis_shank_left_anat[0] * scaling_factor, x_axis_shank_left_anat[1] * scaling_factor, x_axis_shank_left_anat[2] * scaling_factor,
            color='r', label='U axis', length=1)

    ax.quiver(origin_shank_left_anat[0], origin_shank_left_anat[1], origin_shank_left_anat[2],
            y_axis_shank_left_anat[0] * scaling_factor, y_axis_shank_left_anat[1] * scaling_factor, y_axis_shank_left_anat[2] * scaling_factor,
            color='g', label='V axis', length=1)

    ax.quiver(origin_shank_left_anat[0], origin_shank_left_anat[1], origin_shank_left_anat[2],
            z_axis_shank_left_anat[0] * scaling_factor, z_axis_shank_left_anat[1] * scaling_factor, z_axis_shank_left_anat[2] * scaling_factor,
            color='b', label='W axis', length=1)

    # PLOTTING REFERENCE (CLUSTER) COORDINATE SYSTEM FOR THE LEFT SHANK

    """ Plot the local (thigh) coordinate system, computed from the thigh amrker cluster, in the glocal coordinate frame""" 
    x_axis_shank_left_clust = TrefShank_left[:3, 0]
    y_axis_shank_left_clust = TrefShank_left[:3, 1]
    z_axis_shank_left_clust = TrefShank_left[:3, 2]
    origin_shank_left_clust = TrefShank_left[:3, 3] # origin is the 4th column in the transformation matrix

    scaling_factor = 0.1

    ax.quiver(origin_shank_left_clust[0], origin_shank_left_clust[1], origin_shank_left_clust[2],
            x_axis_shank_left_clust[0] * scaling_factor, x_axis_shank_left_clust[1] * scaling_factor, x_axis_shank_left_clust[2] * scaling_factor,
            color='orange', length=1)

    ax.quiver(origin_shank_left_clust[0], origin_shank_left_clust[1], origin_shank_left_clust[2],
            y_axis_shank_left_clust[0] * scaling_factor, y_axis_shank_left_clust[1] * scaling_factor, y_axis_shank_left_clust[2] * scaling_factor,
            color='teal', length=1)

    ax.quiver(origin_shank_left_clust[0], origin_shank_left_clust[1], origin_shank_left_clust[2],
            z_axis_shank_left_clust[0] * scaling_factor, z_axis_shank_left_clust[1] * scaling_factor, z_axis_shank_left_clust[2] * scaling_factor,
            color='purple', length=1)
    

    # PLOTTING ANATOMICAL COORDINATE SYSTEM FOR THE LEFT THIGH
    """ Plot the local (thigh) coordinate system, computed from the thigh amrker cluster, in the glocal coordinate frame""" 
    origin_thigh_left_anat = np.dot(TrefThigh_left, TAnatThigh_left[:4, 3]) # origin is the 4th column in the transformation matrix
    x_axis_thigh_left_anat = TAnatThigh_left[:3, 0]
    y_axis_thigh_left_anat = TAnatThigh_left[:3, 1]
    z_axis_thigh_left_anat = TAnatThigh_left[:3, 2]


    scaling_factor = 0.1

    ax.quiver(origin_thigh_left_anat[0], origin_thigh_left_anat[1], origin_thigh_left_anat[2],
            x_axis_thigh_left_anat[0] * scaling_factor, x_axis_thigh_left_anat[1] * scaling_factor, x_axis_thigh_left_anat[2] * scaling_factor,
            color='r', length=1)

    ax.quiver(origin_thigh_left_anat[0], origin_thigh_left_anat[1], origin_thigh_left_anat[2],
            y_axis_thigh_left_anat[0] * scaling_factor, y_axis_thigh_left_anat[1] * scaling_factor, y_axis_thigh_left_anat[2] * scaling_factor,
            color='g', length=1)

    ax.quiver(origin_thigh_left_anat[0], origin_thigh_left_anat[1], origin_thigh_left_anat[2],
            z_axis_thigh_left_anat[0] * scaling_factor, z_axis_thigh_left_anat[1] * scaling_factor, z_axis_thigh_left_anat[2] * scaling_factor,
            color='b', length=1)
    

    # PLOTTING REFERENCE (CLUSTER) COORDINATE SYSTEM FOR THE LEFT THIGH

    """ Plot the local (thigh) coordinate system, computed from the thigh amrker cluster, in the glocal coordinate frame""" 
    x_axis_thigh_left_clust = TrefThigh_left[:3, 0]
    y_axis_thigh_left_clust = TrefThigh_left[:3, 1]
    z_axis_thigh_left_clust = TrefThigh_left[:3, 2]
    origin_thigh_left_clust = TrefThigh_left[:3, 3] # origin is the 4th column in the transformation matrix


    scaling_factor = 0.1

    ax.quiver(origin_thigh_left_clust[0], origin_thigh_left_clust[1], origin_thigh_left_clust[2],
            x_axis_thigh_left_clust[0] * scaling_factor, x_axis_thigh_left_clust[1] * scaling_factor, x_axis_thigh_left_clust[2] * scaling_factor,
            color='orange', length=1)

    ax.quiver(origin_thigh_left_clust[0], origin_thigh_left_clust[1], origin_thigh_left_clust[2],
            y_axis_thigh_left_clust[0] * scaling_factor, y_axis_thigh_left_clust[1] * scaling_factor, y_axis_thigh_left_clust[2] * scaling_factor,
            color='teal', length=1)

    ax.quiver(origin_thigh_left_clust[0], origin_thigh_left_clust[1], origin_thigh_left_clust[2],
            z_axis_thigh_left_clust[0] * scaling_factor, z_axis_thigh_left_clust[1] * scaling_factor, z_axis_thigh_left_clust[2] * scaling_factor,
            color='purple', length=1)


    # # Set labels and legend
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Raw markers with local coordinate systems')
    ax.legend()

    plt.show()
