import os
import pickle as pkl

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm


class NodesDataset(Dataset):
    def __init__(self, config):
        self.config = config
        self.callgraph_path = config["CALLGRAPH_PATH"]
        self.code_path = config["CODE_PATH"]
        self.save_dir = config["SAVE_DIR"]
        self.save_path = os.path.join(self.save_dir, "nodes_dataset.pkl")
        self.cg_file_name = config["CALLGRAPH_FILE_NAME"]
        self.code_file_name = config["CODE_FILE_NAME"]
        self.max_len = 512

    def __len__(self):
        return len(self.data)

    def process(self):
        pass

    def save(self):
        pass

    def load(self):
        pass
