#%%
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob

def read_h5_file(file_name):
    with h5py.File(file_name, 'r') as f:
        data = f['entry/data/data'][:]
    return data

def normalize_data(data, remove_invalid=True, remove_extreme=True):
    ''' Normalize data to [0, 1]. 
        If remove_invalid, every column containing at least one nan is set to nan.
        If remove extreme, removes points more than 12 std from mean.
    '''
    data_normalized = data.copy()
    if remove_invalid:
        missing_data = np.any(np.isnan(data_normalized), axis=0)
        remove = np.ones(shape=missing_data.shape)
        remove[missing_data] = np.nan
        data_normalized *= remove.reshape(1, -1)
    if remove_extreme:
        mean_rows = np.nanmean(data_normalized, axis=1, keepdims=True)
        std_rows = np.nanstd(data_normalized, axis=1, keepdims=True)
        extreme = np.any(np.abs(data_normalized - mean_rows) > 12 * std_rows, axis=0)
        remove = np.ones(shape=extreme.shape)
        remove[extreme] = np.nan
        data_normalized *= remove.reshape(1, -1)
    mean_rows = np.nanmean(data_normalized, axis=1, keepdims=True)
    std_rows = np.nanstd(data_normalized, axis=1, keepdims=True)
    data_normalized -= mean_rows
    data_normalized /= std_rows
    return data_normalized

def read_folder_data(folder_path):
    if folder_path[-1] != '/':
        folder_path += '/' 
    files = glob.glob(folder_path + '*.h5')
    datas = []
    rownames = []
    for file in files:
        data = read_h5_file(file)
        data = data.reshape((data.shape[0], -1))
        print(file)
        print(data.shape)
        if data.shape[1]<20:
            datas.append(data)
            print('Added')
            t = file.split('/')[-1].strip('.h5')
            rownames.extend([t] * data.shape[1])
    data = np.concatenate(datas, axis=1).T
    print("Combined data shape:", data.shape)
    return data, rownames

#%%
path = '/Users/VAND/Desktop/inline/'  # path to folder containing data

folders = [ 
        'bobbin 1 overwritten data',
        'bobbin1_3s data',
        'bbobbin2',
        'bobbin 2 data 1436',
        'bobbin2_2s live live data',
        ]

for folder in folders:
    data, rownames = read_folder_data(path + folder)
    data_normalized = normalize_data(data)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(data_normalized, vmin=-2, vmax=2, aspect='auto', interpolation='none')
    ax.set_yticks(np.arange(data_normalized.shape[0]), rownames)
    ax.set_title(f'{folder}\nNan ratio {np.isnan(data).sum() / data.size:.2%}')
    plt.show()




# %%
