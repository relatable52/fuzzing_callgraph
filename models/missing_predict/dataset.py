import os
import pickle as pkl

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm


class NodesDataset(Dataset):
    def __init__(self, config, fold_idx=0, mode="train", n_folds=5):
        self.config = config
        self.fold_idx = fold_idx
        self.mode = mode
        self.n_folds = n_folds

        self.callgraph_path = config["CALLGRAPH_PATH"]
        self.code_path = config["CODE_PATH"]
        self.save_dir = config["SAVE_DIR"]
        os.makedirs(self.save_dir, exist_ok=True)
        self.save_path = os.path.join(
            self.save_dir, f"{self.mode}_fold{self.fold_idx}.pkl"
        )

        self.cg_file_name = config["CALLGRAPH_FILE_NAME"]
        self.code_file_name = config["CODE_FILE_NAME"]
        self.max_len = 512

        if os.path.exists(self.save_path):
            print(f"[INFO] Loading cached dataset from {self.cache_path}")
            self._load()
        else:
            print(
                f"[INFO] Creating dataset from {self.callgraph_path} and {self.code_path}"
            )
            self._process()
            self._save()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        pass

    def _process(self):
        pass

    def _save(self):
        pass

    def _load(self):
        pass
