Code for real-time SAXS change detection.

Expects the data to be in the folder `DATA` which contains a folder `inline` that I got from Jens, and a folder `firstdata` that I got from Pooja.

- `compute_change.py`, the initial data analysis script, may be executed in cells, exploratively.
- `visualize_folder_data.py`, tries visualizing all data in all folders 
- `data_navigator`, shows data in an interactive figure, where you use keyboard arrows to change the time. Has to be executed as a Python script. You can use two classes:
  - `DataNavigator`, which shows the mean of 10 images from each `.h5` file, or
  - `SubDataNavigator`, which shows each of 10 images - and is lagging a bit when reading a new image.

