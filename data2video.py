#%%

import h5py
import hdf5plugin
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

def file2image(file, mean=False):
    with h5py.File(file, 'r') as f:
        data = f['entry/data/data']
        data = np.array(data)
    data[data==2**32-1] = 0
    if mean:
        data = data.sum(axis=0)
    data = np.log(data + 1)
    return data

def image2frame(image, vmax=0.1, i=None, j=None):
    image = np.clip(image/vmax, 0, 1)
    cmap = plt.colormaps['viridis'] 
    frame = (cmap(image)[:, :, :3] * 255).astype(np.uint8)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    if i is not None:
        text = str(i) if j is None else str(i) + ' ' + str(j)
        frame = cv2.putText(frame, 
            text, 
            org=(50, 100), 
            fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale = 1, 
            color = (255, 255, 255),
            thickness=3)
    return frame

def folder2video(foldername, videoname, vmax=0.1, sub=False):    
    frame_per_second = 90 if sub else 15
    files = glob.glob(foldername + '*.h5')
    h, w = file2image(files[0]).shape[-2:]
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(videoname, fourcc, frame_per_second, (w, h))
    print()
    for i in range(len(files)):
        print(f'\r{i}/{len(files)}', end='')
        image = file2image(files[i])
        if sub:
            image = file2image(files[i], mean=False)
            for j in image.shape[0]:
                frame = image2frame[image[j], vmax, i, j]
                writer.write(frame)
        else:
            image = file2image(files[i], mean=True)
            frame = image2frame(image, vmax, i)
            writer.write(frame)
    print()
    writer.release()

foldername = 'DATA/inline/bobbin2_2s/'
videoname = 'bobbin2_2_mean.mp4'
folder2video(foldername, videoname)

 #%%

