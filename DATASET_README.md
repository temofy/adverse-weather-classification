---------------------------------------------------
LICENSE
---------------------------------------------------
Creative Commons Attribution 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.


---------------------------------------------------
# Extracting the data:
---------------------------------------------------
The dataset toolkit can be found: https://github.com/aldipiroli/semantic_spray_dataset

To download the dataset:
- Download all of the files (SemanticSprayDataset.zip, SemanticSprayDataset.z01, ...)
- Combine all of the zip files in one single file:
  $ zip -F SemanticSprayDataset.zip --out SemanticSprayDataset_single_file.zip
- Extract the files:
  $ unzip SemanticSprayDataset_single_file.zip

The extracted dataset should have a structure like this:

|--- Crafter_dynamic
|   |--- 0000_2021-09-08-14-36-56_0
|   |   |--- image_2
|   |   |   |--- 000000.jpg
|   |   |   |--- ....
|   |   |--- delphi_radar
|   |   |   |--- 000000.bin
|   |   |   |--- ....
|   |   |--- ibeo_front
|   |   |   |--- 000000.bin
|   |   |   |--- ....
|   |   |--- ibeo_rear
|   |   |   |--- 000000.bin
|   |   |   |--- ....
|   |   |--- labels
|   |   |   |--- 000000.label
|   |   |   |--- ....
|   |   |--- velodyne
|   |   |   |--- 000000.bin
|   |   |   |--- ....
|   |   |--- poses.txt
|   |   |--- metadata.txt
|   |....
|--- Golf_dynamic
|   |--- 0000_2021-09-08-08-27-59_0
|   |   |--- image_2
|   |   |   |--- 000000.jpg
|   |   |   |--- ....
|   |   |--- delphi_radar
|   |   |   |--- 000000.bin
|   |   |   |--- ....
|   |   |--- ibeo_front
|   |   |   |--- 000000.bin
|   |   |   |--- ....
|   |   |--- ibeo_rear
|   |   |   |--- 000000.bin
|   |   |   |--- ....
|   |   |--- labels
|   |   |   |--- 000000.label
|   |   |   |--- ....
|   |   |--- velodyne
|   |   |   |--- 000000.bin
|   |   |   |--- ....
|   |   |--- poses.txt
|   |   |--- metadata.txt
|   |....

---------------------------------------------------
# Exploring the data:
---------------------------------------------------
The sensor setup used for the recordings is the following [1]:
 - 1 Front Camera
 - 1 Velodyne VLP32C LiDAR (top mounted high-resolution LiDAR)
 - 2 Ibeo LUX 2010 LiDAR (front and rear mounted, low-resolution LiDAR)
 - 1 Aptiv ESR 2.5 Radar

For each scene, each sensor data can be found in their respective folders:
- [Camera Image] in the folder "image_2" (e.g., Crafter_dynamic/0000_2021-09-08-14-36-56_0/image_2/000000.jpg)
- [VLP32C LiDAR] in the folder "velodyne" (e.g., Crafter_dynamic/0000_2021-09-08-14-36-56_0/velodyne/000000.bin)
- [VLIbeo LUX 2010 LiDAR front] in the folder "ibeo_front" (e.g., Crafter_dynamic/0000_2021-09-08-14-36-56_0/ibeo_front/000000.bin)
- [VLIbeo LUX 2010 LiDAR rear] in the folder "ibeo_rear" (e.g., Crafter_dynamic/0000_2021-09-08-14-36-56_0/ibeo_rear/000000.bin)
- [Aptiv ESR 2.5 Radar] in the folder "delphi_radar" (e.g., Crafter_dynamic/0000_2021-09-08-14-36-56_0/delphi_radar/000000.bin)
- [Semantic Labels for VLP32C LiDAR] in the folder "labels" (e.g., Crafter_dynamic/0000_2021-09-08-14-36-56_0/labels/000000.label)
- The ego vehicle poses are located in the file "poses.txt". The convention used by the SemanticKITTI dataset [2], [3] is followed.
- Additional information on the scene setup (e.g., ego_velocity) are given in the "metadata.txt" file.

We provide semantic labels for the VLP32C LiDAR scans.
The labeled classes and associated class ID are the following:
    - Background -> 0
    - Leading Vehicle -> 1
    - Spray and other noise artifacts -> 2

---------------------------------------------------
# Loading the data:
---------------------------------------------------
More detailed instructions are provided in: https://github.com/aldipiroli/semantic_spray_dataset
Here is a minimal example for loading both a scan point cloud and associated labels in Python:

import numpy as np

point_cloud_path = "Crafter_dynamic/0000_2021-09-08-14-36-56_0/velodyne/000000.bin"
labels_path = "Crafter_dynamic/0000_2021-09-08-14-36-56_0/labels/000000.label"

labels = np.fromfile(labels_path, np.int32).reshape(-1) # 0: Background, 1: Leading Vehicle, 2: Spray
points = np.fromfile(point_cloud_path, np.float32).reshape(-1, 5)  # x,y,z,intensity,ring

---------------------------------------------------
# Experiments Infos
---------------------------------------------------
Please refer to the original dataset publication for the full raw data, additional scenes and more detailed information on the sensor setup [1].

---------------------------------------------------
# References
---------------------------------------------------
[1] C. Linnhoff, L. Elster, P. Rosenberger, and H. Winner, "Road spray in lidar and radar data for individual moving objects," 2022-04. [Online].
DOI: https://doi.org/10.48328/tudatalib-930
Available: https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/3537
[2] Behley, Jens, et al. "Semantickitti: A dataset for semantic scene understanding of lidar sequences." Proceedings of the IEEE/CVF international conference on computer vision. 2019.
[3] http://www.semantic-kitti.org/dataset.html