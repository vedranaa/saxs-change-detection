#%%
import h5py
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib widget

def read_h5_file(file_name):
    with h5py.File(file_name, 'r') as f:
        data = f['entry/data/data'][:]
        print(data.shape)
    return data

#%%
 
folder_path = 'data/'
 
waxs_rad = ['node_02_200', 'node_04_110']
waxz_az = ['node_06_200_110_az_int', 'node_14_002_004_az_int']
SAXS_rad = ['node_08_SAXS_rad_int', 'node_10_SAXS_mirror_rad_int']
# SAXS_az = ['node_11_SAXS_az_int', 'node_12_SAXS_az_int_mirror']
 
file_waxs_rad_200 = folder_path + waxs_rad[0] + '.h5'
file_waxs_rad_110 = folder_path + waxs_rad[1] + '.h5'
file_waxz_az_200_110 = folder_path + waxz_az[0] + '.h5'
file_waxz_az_002_004 = folder_path + waxz_az[1] + '.h5'
file_SAXS_rad = folder_path + SAXS_rad[0] + '.h5'
file_SAXS_mirror_rad = folder_path + SAXS_rad[1] + '.h5'
# file_SAXS_az = folder_path + SAXS_az[0] + '.h5'
# file_SAXS_mirror_az = folder_path + SAXS_az[1] + '.h5'
 
# def print_structure(name, obj):
#     print(name)
 
def read_h5_file(file_name):
    with h5py.File(file_name, 'r') as f:
        data = f['entry/data/data'][:]
        print(data.shape)
    return data
 
data_waxs_rad_200 = read_h5_file(file_waxs_rad_200)
data_waxs_rad_110 = read_h5_file(file_waxs_rad_110)
data_waxz_az_200_110 = read_h5_file(file_waxz_az_200_110)
data_waxz_az_002_004 = read_h5_file(file_waxz_az_002_004)
data_SAXS_rad = read_h5_file(file_SAXS_rad)
data_SAXS_mirror_rad = read_h5_file(file_SAXS_mirror_rad)


data_combined 

#%%

path = 'data_not_used/node_04_110.h5'
data = read_h5_file(path)


fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(data, aspect='auto')

# %%

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(data)
#%%
print(np.isnan(data).sum()/data.size)


# %%
