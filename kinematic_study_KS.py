# from Functions import find_trials, restructure_csv, calc_knee_angles_from_cluster, start_to_stop, plotCyclograms, gaitEvents, cyclogramStats, interpolate, exclude, rename, plot_mean_cyclograms
# from Functions import write_to_csv
import os
import csv
import scipy.io
import matplotlib.pyplot as plt
import glob
import numpy as np
import pandas as pd
import openpyxl
import pickle

# LEAVE the write_to_csv commented, so new files for stats are not generated

# define the folder paths, sheet names (in the demographics .xlsx file), tasks of interest 
demographics_path = r'Z:\Keep Control\Code\Optical Motion Capture\full body analysis stickfigure\Karolina\demographics_kinematicsStudy_v2.xlsx'
base_path = r'Z:\Keep Control\Data\lab dataset'
sheet_name = ['PD', 'healthy_old', 'PD_off']
tasks_of_interest = ['walkFast', 'walkPreferred', 'walkSlow']
# tasks_of_interest = ['walkPreferred', 'walkFast']

# get the list of IDs in each participant group (defined in demographics file) which have events detected
for iSheet in sheet_name:
    if iSheet == 'healthy_old':
        HO_ids_events = find_trials.find_trials(demographics_path, base_path, iSheet)
    elif iSheet == 'PD':
        PD_ids_events = find_trials.find_trials(demographics_path, base_path, iSheet)
    elif iSheet == 'PD_off':
        PD_off_ids_events = find_trials.find_trials(demographics_path, base_path, iSheet)

PD_OFF_ids_events = []    
for ppID in PD_off_ids_events:
    new_ppID = ppID + '_run-off'
    PD_OFF_ids_events.append(new_ppID)

# PD_off_ids_events = rename.rename_PD_off(PD_off_ids_events)

# save the lists in pickle files so I can use them offline (enough to do once)
# Save the lists
# with open('HO_ids_events.pkl', 'wb') as file:
#     pickle.dump(HO_ids_events, file)

# with open('PD_ids_events.pkl', 'wb') as file:
#     pickle.dump(PD_ids_events, file)

# with open('PD_off_ids_events.pkl', 'wb') as file:
#     pickle.dump(PD_off_ids_events, file)


# # # Load the lists
# with open('HO_ids_events.pkl', 'rb') as file:
#     HO_ids_events = pickle.load(file)

# with open('PD_ids_events.pkl', 'rb') as file:
#     PD_ids_events = pickle.load(file)

# with open('PD_off_ids_events.pkl', 'rb') as file:
#     PD_off_ids_events = pickle.load(file)

# PD_ids_events = ['sub-pp008', 'sub-pp022', 'sub-pp038', 'sub-pp046', 'sub-pp075','sub-pp082', 'sub-pp102', 'sub-pp104'] # ids of PD subjects measued both ON and OFF medication

all_ppIDs_events = HO_ids_events + PD_ids_events + PD_OFF_ids_events
# PD_ids_events = ['sub-pp008']
# PD_off_ids_events = ['sub-pp008_run-off']
all_ppIDs_events = ['sub-pp008'] # debuug single subjects
# all_ppIDs_events = PD_ids_events + PD_off_ids_events

# subjects for exclusion - pp028 (for walkPref, missing r_psis), pp091 (missing l_asis), pp053 (missing r_asis), pp154 (only walkFast, missing l_asis)

# restructure data for all participants (saved in 'restructured' folder)

## ENOUGH TO DO ONCE (for off conditions do wihout calling the rename function!)
# restructure_csv.restructure_csv(base_path, all_ppIDs_events)


## calculate knee angles for all participants, all tasks (between start and stop markers) and save in 'knee angles' in .csv format

all_data_dict, incomplete_trials = calc_knee_angles_from_cluster.calc_knee_angles(base_path, all_ppIDs_events, HO_ids_events, PD_ids_events, PD_off_ids_events, tasks_of_interest)



# Specify the file path where you want to save the dictionary
file_path = r'C:\Users\Karolina\Desktop\python\TU Delft\week 4\completeData_dict.pickle'

# file_path_2 = r'C:\Users\Karolina\Desktop\python\TU Delft\week 4\debug_data_dict.pickle'

# Open the file in binary write mode
# with open(file_path, 'wb') as file:
#     # Serialize and save the dictionary
#     pickle.dump(all_data_dict, file)

# Open the file in binary read mode
with open(file_path, 'rb') as file:
    # Load the dictionary from the file (all_data_dict loaded here has already the subjects and cycles excluded)
    all_data_dict = pickle.load(file) # debug data is renamed to all_data_dict to avoid change function calls 


# exclude subjects or trials 
# all_data_dict = exclude.excludeSubjects(all_data_dict)

## exclude subjects or trials 
all_data_dict = exclude.excludeSubjects(all_data_dict)
# debug_data_dict = exclude.excludeSubjects(all_data_dict)

# ## only the 8 PD subjects measured both on and off 
# all_data_dict = {'sub-pp008': all_data_dict['sub-pp008'], 'sub-pp022': all_data_dict['sub-pp022'],'sub-pp038': all_data_dict['sub-pp038'], 'sub-pp046': all_data_dict['sub-pp046'], 'sub-pp075': all_data_dict['sub-pp075'], 
#                  'sub-pp082': all_data_dict['sub-pp082'], 'sub-pp102': all_data_dict['sub-pp102'], 'sub-pp104': all_data_dict['sub-pp104'],
#                  'sub-pp022_run-off': all_data_dict['sub-pp022_run-off'],'sub-pp038_run-off': all_data_dict['sub-pp038_run-off'], 'sub-pp046_run-off': all_data_dict['sub-pp046_run-off'], 
#                  'sub-pp075_run-off': all_data_dict['sub-pp075_run-off'], 'sub-pp082_run-off': all_data_dict['sub-pp082_run-off'], 'sub-pp102_run-off': all_data_dict['sub-pp102_run-off'], 
#                  'sub-pp104_run-off': all_data_dict['sub-pp104_run-off'], 'sub-pp008_run-off': all_data_dict['sub-pp008_run-off']}



## for debugging single subjects from the pickle file 

# all_data_dict = all_data_dict['sub-pp128']
# all_data_dict = {'sub-pp128':all_data_dict}

## make a new dict with values from start to stop

startStop_all_data_dict = start_to_stop.start_to_stop(base_path, all_data_dict, HO_ids_events, PD_ids_events, PD_OFF_ids_events)

gaitEvents_all_data_dict = gaitEvents.gaitEvents(base_path, all_data_dict, HO_ids_events, PD_ids_events, PD_OFF_ids_events, startStop_all_data_dict)

## plot the cyclograms (only start:stop values)

""" returns a dict where key is ppID and value is a dict where key is the task and value is a dict where key is the side 
and value is a list of tuples where the first variable is cycle_data_hip_left and the second is cycle_data_knee_left (which are the mean-centered joint angles)
each tuple is one cycle """
all_ppIDs_cycles1 = plotCyclograms.plotCyclograms(all_data_dict, startStop_all_data_dict, gaitEvents_all_data_dict)
all_ppIDs_cycles = exclude.excludeCycles(all_ppIDs_cycles1) # returns a dict with excluded cycles

# write a plot function for plotting the cyclograms with excluded cycles1!!!!!!!!!!!!!!!!!!!!

""" Lineraly interpolate all cycles so that each cycle has 500 samples """
samples_for_interpol = 500 # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3956041/
all_ppIDs_interpol = interpolate.interpolateCycles(all_ppIDs_cycles, samples_for_interpol)


# CHANGE ppID for _run-off same like in the above codes (all working till here)

####################################################  numerical values of cyclograms ##############################################################
# calculate range of motion 
# all_ppIDs_rom = cyclogramStats.calculateROM(all_ppIDs_interpol)
# write_to_csv.write_rom_to_csv(all_ppIDs_rom, HO_ids_events, PD_ids_events, PD_off_ids_events)

# calculate cyclogram perimeter 
# all_ppIDs_perim = cyclogramStats.calculatePerimeter(all_ppIDs_interpol)

# calculate Angular component of the coefficient of correspondence (ACC) (Field-Fote and Tepavac, 2002)
# acc = cyclogramStats.calculateACC(all_ppIDs_interpol)
## run the below line only once, then comment it out (otherwise the csv file gets rewritten)
# write_to_csv.write_acc_to_csv(acc, HO_ids_events, PD_ids_events, PD_off_ids_events)

# calculate the mean angles per patient per task per side
mean_cyclograms = cyclogramStats.mean_cyclograms(all_ppIDs_interpol)

# calculate mean cyclogram per person, then per group (to check for shape differences between groups) - result is ONE cyclogram PER GROUP and PER SPEED
mean_cyclograms_HO, mean_cyclograms_PD, mean_cyclograms_PD_off, HO_averages, PD_averages, PD_off_averages = cyclogramStats.mean_cyclograms_group_task(mean_cyclograms, HO_ids_events, PD_ids_events, PD_OFF_ids_events)

# calculate mean cyclogram per person (mean of left and right sides) - result is one cyclogram per subject
# mean_cyclograms_perPerson_HO, mean_cyclograms_perPerson_PD, mean_cyclograms_perPerson_PD_off = cyclogramStats.mean_cyclograms_each_subject(mean_cyclograms, HO_ids_events, PD_ids_events, PD_off_ids_events)

# calculate minimums and maximums of cyclograms for each subject
magnitudes_HO, magnitudes_PD, magnitudes_PD_off = cyclogramStats.calc_magnitude_per_person(HO_averages, PD_averages, PD_off_averages)

# calculate ratios between magnitudes of two tasks for all participants (from a defined group), save into csv file 
# input - group magnitudes (e.g., magnitudes_HO), task names (between which the ratio should be calculated), whcih magnitude to take for calculation ('minimum' or 'maximum),
# column name for the csv file, (e.g., 'HC_min_Fast2Pref', csv path (always the same - all data is written to the same file for statistics later))

ratios_csv_path = r'C:\Users\Karolina\Desktop\python\TU Delft\week 4\good stat files\all_subject_ratios.csv'

# change the below to compute new ratios
# task1 is divided by task 2, so task2 should always be 'walkPreferred' to ensure that it stays 1!!!!!!! JA 
magnitudes_for_ratios = magnitudes_PD
task1_for_ratios = 'walkSlow'
task2_for_ratios = 'walkPreferred'
which_magnitude = 'minimum'
column_name_for_ratios = 'PD_off_min_Slow2Pref'

# the function needs fixing - for every ratio calculation it overwrites the existing csv file, so copy and paste the ratio columns in another file 
cyclogramStats.calc_ratios(magnitudes_for_ratios, task1_for_ratios, task2_for_ratios, which_magnitude, column_name_for_ratios, ratios_csv_path)

print('hello')


# plot the average (of all participants) cyclograms - the 3 groups in one plot, 1 plot per speed
# plot_mean_cyclograms.plot_mean_cyclograms_perSpeed(mean_cyclograms_HO, mean_cyclograms_PD, mean_cyclograms_PD_off)

# plot the average cyclograms - the 3 speedsin one plot, 1 plot per group
# the code also calculates the minimum and maximum points of the cyclograms and plots them as circles and stars; as well as where do these points appear in the
# input - variable with mean cyclograms, figure title between '', e.g. - mean_cyclograms_HO for healthy older group, 'Cyclograms of healthy controls'
plot_mean_cyclograms.plot_mean_cyclograms_perGroup(mean_cyclograms_HO, "Cyclograms of control group", samples_for_interpol)

# calculate the mean cyclogram for PD and for HO (all ppIDs) per task 
# mean_cyclogram_group_speed_HO, mean_cyclogram_group_speed_PD = cyclogramStats.meanCyclogramPerGroup(mean_cyclograms, HO_ids_events, PD_ids_events)

# calculate inter-subject variability (Awai & Curt, 2014; https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3956041/)

task_for_variability = 'walkFast'
side_for_variability = 'left'
nbins = 20 # number of bins for SSD (variability) calculation. Awai & Curt (2014) - 20 bins 
# variability_HO, variability_PD, variability_PD_off = cyclogramStats.inter_subject_variability(mean_cyclograms, HO_ids_events, PD_ids_events, PD_off_ids_events, 
                                                                        #   task_for_variability, side_for_variability, nbins) # dependant on the mean_cyclograms function; leave uncommented 


# calculate cyclogram shape difference (SSD)

task_for_ssd = 'walkSlow'
side_for_ssd = 'right'

# within subjects (takes the mean of all ssds per task, adds to a dict where key is ppID and value is mean ssd). task ans side for calculation given in task_for_ssd and side_for_ssd
# ssd_within_subjects_HO, ssd_within_subjects_PD, ssd_within_subjects_PD_off = cyclogramStats.shape_difference_within_subject(all_ppIDs_interpol, HO_ids_events, PD_ids_events, PD_OFF_ids_events, task_for_ssd, side_for_ssd, samples_for_interpol)
## comment the line below once all rows (all tasks, both sides) are filled 
# write_to_csv.write_ssd_to_csv(ssd_within_subjects_HO, ssd_within_subjects_PD, ssd_within_subjects_PD_off, task_for_ssd, side_for_ssd)

print()
# between subjects 
# ssd_between_subjects_HO, ssd_between_subjects_PD, ssd_between_subjects_PD_off = cyclogramStats.shape_difference_between_subjects(mean_cyclograms, HO_ids_events, PD_ids_events, PD_off_ids_events, task_for_ssd, side_for_ssd, samples_for_interpol)

# asymmetry
# asymmetry_HO, asymmetry_PD, asymmetry_PD_off = cyclogramStats.shape_difference_asymmetry_between_subjects(mean_cyclograms, HO_ids_events, PD_ids_events, PD_off_ids_events, task_for_ssd, samples_for_interpol)
# write_to_csv.write_asym_to_csv(asymmetry_HO, asymmetry_PD, asymmetry_PD_off, task_for_ssd)

# mean_cyclograms_HO is a dict where the key is the task name and its value is a tuple where [0] list is average hip angles of all subjects, and [1] is knee angles 
# function returns the shape difference between two groups, so it depends on which groups are inputed 
# task_for_ssd need to be defined as well to identicate which cyclograms (obtained from which speed) are being compared
# input - mean cyclograms of two different groups (e.g., mean_cyclograms_HO, mean_cyclograms_PD), plus task for which this shoudl be calculated
# ssd_between_groups = cyclogramStats.calculate_shape_difference_between_groups(mean_cyclograms_HO, mean_cyclograms_PD, task_for_ssd, samples_for_interpol)

# calculates the differences in cyclograms, obtained from the same group but different speeds
# funtion input - mean angles from two different speeds of the same group, e.g., mean_cyclograms_PD_off['walkPreferred']
# ssd_between_speeds = cyclogramStats.calculate_shape_difference_between_speeds(mean_cyclograms_HO['walkSlow'], mean_cyclograms_PD['walkSlow'], samples_for_interpol)
# print(ssd_between_speeds)

print('hello')

