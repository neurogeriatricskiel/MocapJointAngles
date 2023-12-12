import sys
from Functions import Load_markers
from Functions import plot_angles
from Functions import plot_markers_anat_coord_sys_3d
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import os
import glob
from scipy.signal import butter, filtfilt

def calc_knee_angles(static_data_file, dynamic_data_file, all_ppIDs_events, task):
    incomplete_trials = []
    all_ppIDs_tasks_joints = {}
    hip = {}
    knee = {}
    all_ppID_task_angles_knee = {} # dict where the key is ppID and the value is a dict where the key is the task name and its value is a dict where the key is the side and value are angles (np.array)
    i =1

    # Load the marker data as numpy array
    static_data = Load_markers.import_markers(static_data_file)
    dynamic_data = Load_markers.import_markers(dynamic_data_file)

    for ppID in all_ppIDs_events:
            nDynam = len(dynamic_data['l_toe'][0]) # get the lenght of the dynamic trial

            variable_names_static = list(static_data.keys())
            coordinates_static = [static_data[var_name] for var_name in variable_names_static]
            coordinates_static = np.array(coordinates_static)

            # Initiate the matrices in the correct size (dependent on the length of the dynamic data)
            TDynamShank_right = np.zeros((4,4,nDynam))
            TDynamThigh_right = np.zeros((4,4,nDynam))       
            TDynamShank_left = np.zeros((4,4,nDynam))
            TDynamThigh_left = np.zeros((4,4,nDynam))

            TDynamPelvis = np.zeros((4,4,nDynam))

            """ Function for computing the transformation matrix (for the clusters, takes 4 arguments) """
            def MakeLocalFrameHom(marker1,marker2,marker3, marker4):
                # Compute the center of the marker cluster
                t = (marker1+marker2+marker3+marker4)/4
                
                # Compute the local coordinate system 
                x = ((marker1 + marker4)/2)-t
                z_temp = ((marker1+marker2)/2) - t
                y = np.cross(x,z_temp)
                z = np.cross(y,x) # z up, like in raw data 

                # Normalization into unit vectors 
                x_norm = x/np.linalg.norm(x)
                y_norm = y/np.linalg.norm(y)
                z_norm = z/np.linalg.norm(z)

                # Make the transformation matrix
                R = np.transpose(np.array([x_norm,y_norm,z_norm]))
                T = np.array([[R[0,0],R[0,1],R[0,2],t[0]],
                                [R[1,0],R[1,1],R[1,2],t[1]],
                                [R[2,0],R[2,1],R[2,2],t[2]],
                                [0,0,0,1]])
                return T 

            """ Function for computing HIP transformation matrix """
            def MakeHipLocalFrameHom(l_asis, r_asis, l_psis, r_psis):
                # Compute the center of the pelvis
                t = (l_asis + r_asis + l_psis + r_psis)/4

                # Compute the local coordinate system
                x_tmp = l_asis - l_psis
                y = l_asis - r_asis
                z = np.cross(x_tmp,y)
                x = np.cross(y,z)
                
                # Normalization into unit vectors 
                x_norm = x/np.linalg.norm(x)
                y_norm = y/np.linalg.norm(y)
                z_norm = z/np.linalg.norm(z)

                # Make the transformation matrix 
                R = np.transpose(np.array([x_norm,y_norm,z_norm]))
                T = np.array([[R[0,0],R[0,1],R[0,2],t[0]],
                                [R[1,0],R[1,1],R[1,2],t[1]],
                                [R[2,0],R[2,1],R[2,2],t[2]],
                                [0,0,0,1]]) # where the last row is homogeneous coordinates 
                return T 

            
            # Compute the transformation matrix for each segment using the dynamic marker data 
            try:
                for i in range(nDynam):
                    TDynamShank_right[:,:,i] = MakeLocalFrameHom(dynamic_data['r_sk1'][:,i],dynamic_data['r_sk2'][:,i],dynamic_data['r_sk3'][:,i], dynamic_data['r_sk4'][:,i])
                    TDynamThigh_right[:,:,i] = MakeLocalFrameHom(dynamic_data['r_th1'][:,i],dynamic_data['r_th2'][:,i],dynamic_data['r_th3'][:,i], dynamic_data['r_th4'][:,i])

                    TDynamShank_left[:,:,i] = MakeLocalFrameHom(dynamic_data['l_sk1'][:,i],dynamic_data['l_sk2'][:,i],dynamic_data['l_sk3'][:,i], dynamic_data['l_sk4'][:,i])
                    TDynamThigh_left[:,:,i] = MakeLocalFrameHom(dynamic_data['l_th1'][:,i],dynamic_data['l_th2'][:,i],dynamic_data['l_th3'][:,i], dynamic_data['l_th4'][:,i])

                for i in range(nDynam):
                    TDynamPelvis[:,:,i] = MakeHipLocalFrameHom(dynamic_data['l_asis'][:,i],dynamic_data['r_asis'][:,i],dynamic_data['l_psis'][:,i], dynamic_data['r_psis'][:,i])
                    

                # Compute the homogenous tranformation matrix of the thigh and shank clusters from the average static marker positions 

                TStatShank_right = MakeLocalFrameHom(np.mean(static_data['r_sk1'], axis=1),np.mean(static_data['r_sk2'], axis=1),np.mean(static_data['r_sk3'], 
                                                                                                                                         axis=1), np.mean(static_data['r_sk4'], axis=1))
                TStatThigh_right = MakeLocalFrameHom(np.mean(static_data['r_th1'], axis=1),np.mean(static_data['r_th2'], axis=1),np.mean(static_data['r_th3'],
                                                                                                                                          axis=1), np.mean(static_data['r_th4'], axis=1))

                TStatShank_left = MakeLocalFrameHom(np.mean(static_data['l_sk1'], axis=1),np.mean(static_data['l_sk2'], axis=1),np.mean(static_data['l_sk3'], 
                                                                                                                                        axis=1), np.mean(static_data['l_sk4'], axis=1))
                TStatThigh_left = MakeLocalFrameHom(np.mean(static_data['l_th1'], axis=1),np.mean(static_data['l_th2'], axis=1),np.mean(static_data['l_th3'], 
                                                                                                                                        axis=1), np.mean(static_data['l_th4'], axis=1))

                TStatPelvis = MakeHipLocalFrameHom(np.mean(static_data['l_asis'], axis=1),np.mean(static_data['r_asis'], axis=1),np.mean(static_data['l_psis'], 
                                                                                                                                         axis=1), np.mean(static_data['r_psis'], axis=1))

                """ Plot the local coordinate systems and the (mean of) static markers in the global coordinate frame""" 
                plot_markers_anat_coord_sys_3d.plot_3d(static_data, TStatShank_right, TStatThigh_right, TStatShank_left, TStatThigh_left, TStatPelvis)

                # Initiate the transformation matrices of the correct size (dependent on data length)
                T_ref_shank_right = np.zeros((4,4,nDynam))
                T_ref_thigh_right = np.zeros((4,4,nDynam))
                T_Knee_ref_right = np.zeros((4,4,nDynam))
                Knee_Angles_ref_right = np.zeros((3,nDynam))

                T_ref_shank_left = np.zeros((4,4,nDynam))
                T_ref_thigh_left = np.zeros((4,4,nDynam))
                T_Knee_ref_left = np.zeros((4,4,nDynam))
                Knee_Angles_ref_left = np.zeros((3,nDynam))

                T_ref_pelvis = np.zeros((4,4,nDynam))
                T_Hip_ref_right = np.zeros((4,4,nDynam))
                T_Hip_ref_left = np.zeros((4,4,nDynam))
                Hip_Angles_ref_right = np.zeros((3,nDynam))
                Hip_Angles_ref_left = np.zeros((3,nDynam))
                
                # Loop over all samples to determine the transformation matrices of the marker clusters relative to the reference (static) position of the pelvis, thigh and shank
                for i in range(nDynam):
                    T_ref_shank_right[:,:,i] = np.dot(TDynamShank_right[:,:,i],np.linalg.inv(TStatShank_right))
                    T_ref_thigh_right[:,:,i] = np.dot(TDynamThigh_right[:,:,i],np.linalg.inv(TStatThigh_right))
                    T_ref_shank_left[:,:,i] = np.dot(TDynamShank_left[:,:,i],np.linalg.inv(TStatShank_left))
                    T_ref_thigh_left[:,:,i] = np.dot(TDynamThigh_left[:,:,i],np.linalg.inv(TStatThigh_left))
                    T_ref_pelvis[:,:,i] = np.dot(TDynamPelvis[:,:,i], np.linalg.inv(TStatPelvis))

                # Loop pver all samples to determine the transformation matrices for the right and left hip and knee 
                for i in range(nDynam):
                    T_Knee_ref_right[:,:,i]= np.dot(np.linalg.inv(T_ref_thigh_right[:,:,i]),T_ref_shank_right[:,:,i])
                    T_Knee_ref_left[:,:,i]= np.dot(np.linalg.inv(T_ref_thigh_left[:,:,i]),T_ref_shank_left[:,:,i])

                    T_Hip_ref_right[:,:,i]= np.dot(np.linalg.inv(T_ref_pelvis[:,:,i]),T_ref_thigh_right[:,:,i])
                    T_Hip_ref_left[:,:,i]= np.dot(np.linalg.inv(T_ref_pelvis[:,:,i]),T_ref_thigh_left[:,:,i])

                """ Function for decomposing the rotation matrix """
                def rot2eul(R):# Z-X-Y
                    alpha = np.arcsin(R[2,1])*180/np.pi # X
                    beta = np.arctan2(-R[2,0],R[2,2])*180/np.pi # Y
                    gamma = np.arctan2(-R[0,1],R[1,1])*180/np.pi #Z
                    return alpha,beta,gamma

                # Calculate the angles in degrees
                for i in range(nDynam):
                    [Knee_Angles_ref_right[1,i],Knee_Angles_ref_right[0,i],Knee_Angles_ref_right[2,i]] = rot2eul(T_Knee_ref_right[:,:,i])
                    [Knee_Angles_ref_left[1,i],Knee_Angles_ref_left[0,i],Knee_Angles_ref_left[2,i]] = rot2eul(T_Knee_ref_left[:,:,i])
                    [Hip_Angles_ref_right[1,i],Hip_Angles_ref_right[0,i],Hip_Angles_ref_right[2,i]] = rot2eul(T_Hip_ref_right[:,:,i])
                    [Hip_Angles_ref_left[1,i],Hip_Angles_ref_left[0,i],Hip_Angles_ref_left[2,i]] = rot2eul(T_Hip_ref_left[:,:,i])
                
                # Put all the angles in a nested dict where the key is ppID and its value is a dict where the key is task name and its value is a dict where the key is
                # joint name and its value is a dict where the key is the side (left and right) and its value are the angles in degrees for the whole dynamic trial"""

                hip['left'] = np.copy(Hip_Angles_ref_left)
                hip['right'] = np.copy(Hip_Angles_ref_right)

                knee['left'] = np.copy(Knee_Angles_ref_left)
                knee['right'] = np.copy(Knee_Angles_ref_right)

                all_ppID_task_angles_knee.setdefault(ppID, {})[task] = {
                'left': np.copy(Knee_Angles_ref_left),
                'right': np.copy(Knee_Angles_ref_right)
                }

                all_ppIDs_tasks_joints.setdefault(ppID, {}).setdefault(task, {}).setdefault('hip', {}).update({'left':Hip_Angles_ref_left, 'right' : Hip_Angles_ref_right}) 
                all_ppIDs_tasks_joints.setdefault(ppID, {}).setdefault(task, {}).setdefault('knee', {}).update({'left': Knee_Angles_ref_left, 'right' : Knee_Angles_ref_right}) 

            # catch the incomplete trials 
            except:
                print(f'INCOMPLETE is {ppID} {task}')
                incomplete_trials.append((ppID, task))
                continue 
    
    # plot all the angles (output - one figure with six subplots)
    plot_angles.plot_angles(nDynam, Knee_Angles_ref_left, Knee_Angles_ref_right, Hip_Angles_ref_left, Hip_Angles_ref_right, ppID, task)
    return all_ppIDs_tasks_joints, incomplete_trials
