import numpy as np
import pandas as pd

import os
import json

import matplotlib.pyplot as plt
from matplotlib import colors


class TaskData():

    def __init__(self, json_file):
        self.filename = json_file
        with open(json_file, 'r') as f:
            self.task = json.load(f)
        self.n_train = len(self.task["train"])
        self.n_test = len(self.task["test"])

    def train_pair_generator(self, group="train"):
        for train_inst in self.task[group]:
            yield np.asarray(train_inst["input"]
                             ), np.asarray(train_inst["output"])

    def get_specific_pair(self, index, group="train"):
        train_inst = self.task[group][index]
        return np.asarray(train_inst["input"]
                          ), np.asarray(train_inst["output"])


def plot_task(task):
    """
    Plots the first train and test pairs of a specified task,
    using same color scheme as the ARC app
    """
    cmap = colors.ListedColormap(
        [
            '#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00', '#AAAAAA',
            '#F012BE', '#FF851B', '#7FDBFF', '#870C25'
        ]
    )
    norm = colors.Normalize(vmin=0, vmax=9)
    fig, axs = plt.subplots(1, 4, figsize=(15, 15))
    axs[0].imshow(task['train'][0]['input'], cmap=cmap, norm=norm)
    axs[0].axis('off')
    axs[0].set_title('Train Input')
    axs[1].imshow(task['train'][0]['output'], cmap=cmap, norm=norm)
    axs[1].axis('off')
    axs[1].set_title('Train Output')
    axs[2].imshow(task['test'][0]['input'], cmap=cmap, norm=norm)
    axs[2].axis('off')
    axs[2].set_title('Test Input')
    axs[3].imshow(task['test'][0]['output'], cmap=cmap, norm=norm)
    axs[3].axis('off')
    axs[3].set_title('Test Output')
    plt.tight_layout()
    plt.show()


def read_files(path):
    tasks = []
    for f in os.listdir(path):
        print(f)
        if f[-4:] == "json":
            task_obj = TaskData(os.path.join(path, f))
            tasks.append(task_obj)
    return tasks


if __name__ == "main":
    training_path = "/Users/ninawiedemann/Desktop/Projects/abstract_reasoning/abstraction-and-reasoning-challenge/training"
    tasks = read_files(training_path)
    print(tasks[3].get_specific_pair(1))
    plot_task(tasks[3].task)
