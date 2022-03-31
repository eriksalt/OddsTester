import seaborn as sns
import pandas as pd
import random as rand
import numpy as np
from dataclasses import dataclass, field

import cProfile
import marked_odds_opt as opt

sns.set_style("whitegrid")

file_mean_result_by_dice: str = "mean_results_by_dice_pool_size.csv"
file_raw_results_by_dice: str = "raw_results_by_dice.csv"


dice_roll_cache = {x: np.empty(x, dtype=np.int64) for x in range(0, 20)}  # {k:v*2 for (k,v) in dict1.items()}


@dataclass
class OriginalRoll:
    dice_count: int
    rolls: np.ndarray = field(init=False)
    results: np.ndarray = field(init=False)

    def roll_dice(self):
        self.rolls = opt.roll_dice_opt(self.dice_count, dice_roll_cache[self.dice_count])
        return self

    def calculate_results(self):
        self.results = opt.calculate_results(self.rolls)
        return self


def run_raw_results(dice_count: int, run_count: int) -> pd.Series:
    output: np.ndarray = np.empty(run_count * (dice_count - 1), dtype=np.int64)
    for i in range(run_count):
        counter = 0
        results = OriginalRoll(dice_count).roll_dice().calculate_results().results
        base_num: int = i * (dice_count - 1)
        for x in results:
            output[base_num + counter] = x
            counter = counter + 1
    pd_output = pd.Series(output)
    return pd_output


def run_agg_results(dice_count: int, run_count: int, agg_func) -> pd.Series:
    output: np.ndarray = np.empty(run_count, dtype=np.int64)
    for i in range(run_count):
        counter = 0
        results = OriginalRoll(dice_count).roll_dice().calculate_results().results
        output[i] = agg_func(results)
    pd_output = pd.Series(output)
    return pd_output


def exp_result_means_by_dice_pool_size(min_dice_count: int, max_dice_cont: int, run_count: int, filename: str):
    with open(filename, "w") as f:
        for i in range(min_dice_count, max_dice_cont):
            output: pd.Series = run_raw_results(i, run_count)
            f.write(f"{i},{output.mean()}\n")


def exp_raw_results_by_dice_pool_size(min_dice_count: int, max_dice_cont: int, run_count: int, filename: str):
    with open(filename, "w") as f:
        for i in range(min_dice_count, max_dice_cont):
            output: pd.Series = run_raw_results(i, run_count)
            for result in output:
                f.write(f"{i},{result}\n")


run_count = 10000
min_dice = 2
max_dice = 11
exp_raw_results_by_dice_pool_size(min_dice, max_dice, run_count, file_raw_results_by_dice)
# exp_result_means_by_dice_pool_size(2, 11, file_mean_result_by_dice)
