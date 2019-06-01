import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import torch
import sys

from sklearn.manifold import TSNE
from model import Autoencoder
import random

from dataset import dataset as dataset
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if "plot_embedding" in sys.argv:
    indices = random.sample(list(range(dataset.size)), 1000)
    voxels = dataset.voxels[indices, :, :, :]
    autoencoder = Autoencoder()
    autoencoder.load()
    print("Generating codes...")
    with torch.no_grad():
        codes = autoencoder.create_latent_code(*autoencoder.encode(voxels), device).cpu().numpy()
    labels = dataset.label_indices[indices].cpu().numpy()

    print("Calculating t-sne embedding...")
    tsne = TSNE(n_components=2)
    embedded = tsne.fit_transform(codes)

    
    print("Plotting...")
    fig, ax = plt.subplots()
    ax.scatter(embedded[:, 0], embedded[:, 1], c=labels, s = 4)
    fig.set_size_inches(40, 40)
    for i in range(len(indices)):
        box = AnnotationBbox(OffsetImage(plt.imread("images/{:d}.png".format(indices[i])), zoom = 0.5), embedded[i, :], frameon=True)
        ax.add_artist(box)
    plt.savefig("t-sne.pdf", dpi=200, bbox_inches='tight')

if "create_images" in sys.argv:
    from voxel.viewer import VoxelViewer
    from tqdm import tqdm
    viewer = VoxelViewer(start_thread=False, background_color = (1.0, 1.0, 1.0, 1.0))
    viewer._initialize_opengl()
    for i in tqdm(range(dataset.size)):
        viewer.set_voxels(dataset.voxels[i, :, :, :].cpu().numpy())
        viewer._render()
        viewer.save_image("images/{:d}.png".format(i))
