import numpy as np
import os
import torch.utils.data as torch_data
import matplotlib.image as mpimg


class SemanticSprayDataset(torch_data.Dataset):
    def __init__(self, root_path, split="train"):
        # ----- parse input parameters -------
        self.root_path = root_path
        assert os.path.isdir(self.root_path)
        assert split in ["train", "test"]
        self.training = True if split == "train" else False

        self.load_low_resolution_lidars = True
        self.load_radar = True
        self.load_camera = True

        # ------- get data splits -------
        split_dir = os.path.join(self.root_path, "ImageSets", self.mode + ".txt")
        assert os.path.isfile(split_dir)
        scenes_list = [x.strip() for x in open(split_dir).readlines()]
        self.sample_id_list = self.get_data_samples(scenes_list)
        print("Mode: %s, loaded samples %d" % (self.mode, len(self.sample_id_list)))
        assert len(self.sample_id_list) > 0

    @property
    def mode(self):
        return "train" if self.training else "test"

    def get_data_samples(self, scenes_list):
        all_samples = []
        for sample_id in scenes_list:
            velo_files = sorted(next(os.walk(os.path.join(self.root_path, sample_id, "velodyne")), (None, None, []))[2])
            for curr_id in velo_files:
                scan_id = curr_id.split(".")[0]
                all_samples.append(os.path.join(self.root_path, sample_id, scan_id))
        return all_samples

    def load_data(self, scene_path, scan_id):
        assert os.path.isdir(scene_path), print(scene_path)
        data = {}

        # ---------- load top mounted LiDAR point cloud and labels ----------
        # load velodyne:
        velo_path = os.path.join(scene_path, "velodyne", scan_id + ".bin")
        points = np.fromfile(velo_path, np.float32).reshape(-1, 5)  # x,y,z,intensity,ring

        # load labels:
        labels_path = os.path.join(scene_path, "labels", scan_id + ".label")
        labels = np.fromfile(labels_path, np.int32).reshape(-1)  # 0: background, 1: foreground (vehicle), 2: noise

        # ego filter
        box_mask = self.ego_box_filter(points)
        points = points[box_mask]
        labels = labels[box_mask]

        # sanity check
        assert points.shape[0] == labels.shape[0]
        data["points"] = points
        data["labels"] = labels

        # ---------- load low resolution LiDARs point cloud ----------
        ibeo_front_path = os.path.join(scene_path, "ibeo_front", scan_id + ".bin")
        ibeo_front = np.fromfile(ibeo_front_path, np.float32).reshape(-1, 4)
        data["ibeo_front"] = ibeo_front

        ibeo_rear_path = os.path.join(scene_path, "ibeo_rear", scan_id + ".bin")
        ibeo_rear = np.fromfile(ibeo_rear_path, np.float32).reshape(-1, 4)
        data["ibeo_rear"] = ibeo_rear

        # ---------- load radar point cloud ----------
        delphi_radar_path = os.path.join(scene_path, "delphi_radar", scan_id + ".bin")
        radar_points = np.fromfile(delphi_radar_path, np.float32).reshape(-1, 4)
        data["radar_points"] = radar_points

        # ---------- load camera image ----------
        camera_path = os.path.join(scene_path, "image_2", scan_id + ".jpg")
        camera_image = mpimg.imread(camera_path)
        data["camera_image"] = camera_image

        # ---------- metadata ----------
        with open(os.path.join(scene_path, "metadata.txt")) as file:
            text_infos = [line.rstrip("\n") for line in file]
        keys = text_infos[0].split(",")
        vals = text_infos[1].split(",")
        assert len(keys) == len(vals)
        metadata = {}
        for k, v in zip(keys, vals):
            metadata[k] = v

        data["infos"] = {"scene_path": scene_path, "scan_id": scan_id, "metadata": metadata}
        return data

    def ego_box_filter(self, points):
        """
        Фильтрует точки вблизи лидара
        :param points:
        :return: Возвращает битовую маску точек. Которые нужно оставить присваивает значение True,
            которые надо удалить False
        """
        SIZE = 2
        ego_mask = (np.abs(points[:, 0]) < SIZE) & (np.absolute(points[:, 1]) < SIZE)
        return ~ego_mask

    def distance_point_filter(self, points, x_max, y_max):
        """
        Фильтрует точки по удаленности от центра
        :param points:
        :param x_max:
        :param y_max:
        :return:
        """
        distance_mask = ~(np.abs(points[:, 0]) < x_max) & (np.absolute(points[:, 1]) < y_max)
        points = points[distance_mask]
        return points

    def __len__(self):
        return len(self.sample_id_list)

    def __getitem__(self, index):
        # --------- get data path ---------
        data_path = os.path.join(self.sample_id_list[index])
        scan_id = data_path.split("/")[-1]
        scene_path = data_path[:-6]

        # --------- load data ---------
        data = self.load_data(scene_path, scan_id)

        return data
