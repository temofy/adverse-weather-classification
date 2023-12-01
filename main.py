from dataset.semantic_spray_dataset import SemanticSprayDataset
from visualization import visualization_tools as vis
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from utils import distance_point_filter
import numpy as np
from sklearn.cluster import DBSCAN

def main():
    train_dataset = SemanticSprayDataset("SemanticSprayDataset", "train")
    test_dataset = SemanticSprayDataset("SemanticSprayDataset", "train")

    # train_dataloader = DataLoader(train_dataset, batch_size=1, shuffle=False)
    # for data in train_dataloader:
    #     print("Максимальные значения в x, y, z, intensity, rings:", data["points"].numpy().squeeze().max(0))
    #     print("Точек машин: ", np.count_nonzero(data["labels"].numpy() == 1))
    #     print("Точек шума: ", np.count_nonzero(data["labels"].numpy() == 2))
    #     input("...")

    for data in test_dataset:
        test(data)


def dbscan(data, eps=2, min_samples=5, leaf_size=30):
    clustering = DBSCAN(eps=eps, min_samples=min_samples, leaf_size=leaf_size).fit(data)

    core_samples_mask = np.zeros_like(clustering.labels_, dtype=bool)
    core_samples_mask[clustering.core_sample_indices_] = True
    labels = clustering.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    print('Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)

    unique_labels = set(labels)
    labels_color = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    return labels, labels_color

def points_preprocess(data, distance_crop=False):
    boundaries = {}
    boundaries['min_x'] = -30
    boundaries['max_x'] = 30
    boundaries['min_y'] = -30
    boundaries['max_y'] = 30
    boundaries['min_z'] = -30
    boundaries['max_z'] = 30
    if distance_crop:
        data["points"], data["labels"] = distance_point_filter(data["points"], boundaries, data["labels"])

    return data

def delete_noisy():
    pass
def test(data):
    data["labels"] = np.zeros(len(data["labels"]))
    data = points_preprocess(data, distance_crop=True)
    labels, labels_color = dbscan(data["points"], 2, 20)

    data["labels"] = labels

    vis.visualize_scene(data, plot_type="3D", labels_color=labels_color)


if __name__ == "__main__":
    main()

