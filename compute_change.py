'''Initial analysis. This is the first code, and has not been cleaned.'''

#%%
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob


def read_h5_file(file_name):
    with h5py.File(file_name, 'r') as f:
        data = f['entry/data/data'][:]
    return data

def nan_windowed_mean_std(data, half_window, robust=True):
    mean = np.full(shape=data.shape, fill_value=np.nan)
    std = np.full(shape=data.shape, fill_value=np.nan)
    t = data.shape[1]

    for i in range(half_window, t - half_window):
        start = i - half_window
        end = i + half_window + 1
        window = data[:, start : end]
        mean[:, i] = np.nanmean(window, axis=1)
        std[:, i] = np.nanstd(window, axis=1)
    return mean, std

#%%

folder_path = 'DATA/inline/bobbin2_2s_data/'
files = glob.glob(folder_path + '*.h5')

datas = []
for file in files:
    data = read_h5_file(file)
    data = data.reshape((data.shape[0], -1))
    print(file)
    print(data.shape)
    datas.append(data)

data = np.concatenate(datas, axis=1).T
print("Combined data shape:", data.shape)

#%%
#fig, ax = plt.subplots(figsize=(10, 5))
#ax.imshow(data[:,:3000], aspect='auto', interpolation='none')
#ax.set_title(f'Nan ratio {np.isnan(data).sum() / data.size:.2%}')

#%%
# Show raw data

fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(data, aspect='auto', interpolation='none')
ax.set_title(f'Nan ratio {np.isnan(data).sum() / data.size:.2%}')
ax.set_xlabel('Time')
ax.set_ylabel('Fitted values')
plt.savefig('bobbin_1.png')


#%%
# Normalize every data row

data_normalized = data.copy()
missing_data = np.any(np.isnan(data_normalized), axis=0)
remove = np.ones(shape=missing_data.shape)
remove[missing_data] = np.nan
data_normalized *= remove.reshape(1, -1)
mean_rows = np.nanmean(data_normalized, axis=1, keepdims=True)
std_rows = np.nanstd(data_normalized, axis=1, keepdims=True)
data_normalized -= mean_rows
data_normalized /= std_rows

fig, ax = plt.subplots(figsize=(20, 10))
ax.imshow(data_normalized, aspect='auto', vmin=-1.5, vmax=1.5, interpolation='none')
ax.set_title(f'Nan ratio {np.isnan(data_normalized).sum() / data_normalized.size:.2%}')
ax.set_xlabel('Time')
ax.set_ylabel('Fitted values (normalized)')
plt.savefig('bobbin_1_normalized.png')

#%%
# K-means clustering, only on time-points where we have all data

valid_data = data_normalized[:, ~missing_data]
valid_indices = np.arange(data_normalized.shape[1])
valid_indices = valid_indices[~missing_data]
from sklearn.cluster import KMeans

# Number of clusters
n_clusters = 5

# Perform k-means clustering
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
kmeans.fit(valid_data.T)  # Transpose to cluster columns (features)

# Get cluster labels
labels = kmeans.labels_

# Plot the clustered data
fig, ax = plt.subplots(figsize=(10, 5))
scatter = ax.scatter(valid_indices, labels, c=labels, cmap='viridis', s=10)
ax.set_title('K-Means Clustering of Valid Data')
ax.set_xlabel('Time')
ax.set_ylabel('Cluster index')
plt.show()
#%% Investigating some outliers

half_window = 5
mean, std = nan_windowed_mean_std(data_normalized, half_window)

fig, ax = plt.subplots(3, 1, figsize=(10, 10))
ax[0].imshow(mean[:,3920:3930], vmin=-3, vmax=3, aspect='auto', interpolation='none')
ax[0].set_title('Windowed mean')
ax[1].imshow(std[:,3920:3930], vmin=0, vmax=3, aspect='auto', interpolation='none')
ax[1].set_title('Windowed std')
ax[2].imshow(data_normalized[:,3920:3930], vmin=-3, vmax=3, aspect='auto', interpolation='none')
ax[2].set_title('Data')
plt.show()


# %%
# Down from here, the code has not been tested, and I think
# something is wrong

#%%
# Attempt of change detection

dm = mean[:, 2 * half_window:-half_window] - mean[:, half_window:-2 * half_window]
ms = std[:, 2 * half_window:-half_window] + std[:, half_window:-2 * half_window]

change = dm / ms  
abs_change = np.abs(change)


fig, ax = plt.subplots(2, 1, figsize=(10, 10))
ax[0].imshow(change[:,:3000], aspect='auto')
ax[0].set_title('Change')
ax[1].imshow(abs_change[:,:3000], aspect='auto')
ax[1].set_title('Abs change')


sc = abs_change.sum(axis=0) 
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_title('Sum of abs change')
ax.plot(sc)


# %%

# %%
