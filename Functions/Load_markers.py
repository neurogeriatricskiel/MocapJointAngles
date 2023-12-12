# Autor: Rafael van Loon (R.M.vanLoon-1@student.tudelft.nl)
# loads csv files and makes them in to marker dicts
def import_markers(path):
    import csv
    import numpy as np
    # from tkinter.filedialog import askopenfilename
    # path = askopenfilename()

    all_data  =[]
    
    with open(path, newline='') as csvfile:
        file = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in file:
            all_data.append(row)
        
        keys = [all_data[0]]
        all_data = np.transpose(all_data)
        values = []
        for i in range(len(row)-1):
            values.append(all_data[i,1:])  
    
    markerpositions = dict(zip(keys[0],values))
    data_size = np.shape(all_data)
    Marker_amount = int(data_size[0]/3)
    final_keys = []
    final_values = []
    final_value = []
    j = 0
    for i in range(Marker_amount):
        final_keys.append(all_data[j,0])
        markertype = {'x':all_data[j+0,1:].astype(float),'y':all_data[j+1,1:].astype(float),'z':all_data[j+2,1:].astype(float)}
        final_value.append(markertype)
        #final_values.append([all_data[j,1:].astype(np.float),all_data[j+1,1:].astype(np.float),all_data[j+2,1:].astype(np.float)]) 
        final_values.append(np.array([all_data[j,1:].astype(float),all_data[j+1,1:].astype(float),all_data[j+2,1:].astype(float)]))
        j = j+3


    markers = dict(zip(final_keys,final_values))    
    return markers