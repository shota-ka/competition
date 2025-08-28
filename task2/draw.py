import matplotlib.pyplot as plt
import numpy as np

def draw_map(data, name, mode="predict"):

    arr = np.array(data)

    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(["white", "red", "blue", "green", "yellow"])

    plt.imshow(arr, cmap=cmap)

    plt.grid(color="black", linewidth=1)
    plt.xticks(np.arange(-0.5, arr.shape[1], 1), [])  # 列の区切り
    plt.yticks(np.arange(-0.5, arr.shape[0], 1), [])  # 行の区切り

    plt.savefig(f"{mode}_{name}.png")