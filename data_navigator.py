'''Opens interactive matplotlib figure. Works well when run as python script 
(not in a cell mode in VS Code).'''

import h5py
import hdf5plugin
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

class DataNavigator:
    def __init__(self, foldername):
        self.files = glob.glob(foldername + '*.h5')
        self.index = 0
        self.vmax = 0.5
        self.image = file2image(self.files[self.index], mean=True)
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self.image, vmin=0, vmax=self.vmax)
        self.ax.set_title(f"Image {self.index + 1}/{len(self.files)}")
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        plt.show()

    def on_key(self, event):
        move = 0
        if event.key == 'right':  
            move = 1
        elif event.key == 'left':  
            move = -1
        elif event.key == 'up':
            move = 100
        elif event.key == 'down':
            move = -100
        self.index = (self.index + move) % len(self.files)
        self.image = file2image(self.files[self.index], mean=True)
        self.im.set_data(self.image)
        self.ax.set_title(f"Image {self.index + 1}/{len(self.files)}")
        self.fig.canvas.draw()


class SubDataNavigator:
    def __init__(self, foldername):
        self.files = glob.glob(foldername + '*.h5')
        self.data = file2image(self.files[0])
        self.image = self.data[0]
        self.channels = self.data.shape[0]
        self.index = 0
        self.vmax = 0.1
        self.file_index = 0
        self.sub_index = 0
        self.length = self.channels * len(self.files)
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self.image, vmin=0, vmax=self.vmax)
        self.ax.set_title(f"Image {self.index + 1}/{self.length}")
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        plt.show()

    def on_key(self, event):
        old_file_index = self.file_index
        move = 0
        if event.key == 'right':  
            move = 1
        elif event.key == 'left':  
            move = -1
        elif event.key == 'up':
            move = 100
        elif event.key == 'down':
            move = -100
        self.index = (self.index + move) % self.length
        self.file_index = self.index // self.channels
        self.sub_index = self.index % self.channels
        if self.file_index != old_file_index:
            self.data = file2image(self.files[self.file_index])
        self.image = self.data[self.sub_index]
        self.im.set_data(self.image)
        self.ax.set_title(f"Image {self.index + 1}/{self.length}")
        self.fig.canvas.draw() 

foldername = 'DATA/inline/bobbin2_2s/'
#foldername = 'DATA/inline/3s_running_yarn_3/'
navigator = DataNavigator(foldername)
#navigator = SubDataNavigator(foldername)
