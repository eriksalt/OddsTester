import seaborn as sns
import pandas as pd
import random as rand
import numpy as np
from dataclasses import dataclass, field

sns.set_style('whitegrid')

@dataclass
class OriginalRoll:
    dice_count: int
    rolls : np.ndarray  =   field(init=False)
    results : np.ndarray =   field(init=False)
    
    def roll_dice(self):
        self.rolls = np.empty(self.dice_count, dtype=np.int64)
        max_value : int = -1
        max_index : int = -1
        for i in range(self.dice_count):
            roll= rand.randrange(1,11)
            self.rolls[i] = roll
            if roll > max_value:
                max_value=roll
                max_index=i
        #swap largest value to end
        self.rolls[self.dice_count-1], self.rolls[max_index] = self.rolls[max_index], self.rolls[self.dice_count-1]
        return self

    def calculate_results(self):
        max_roll : int = self.rolls[-1]
        self.results=self.rolls[:-1]+max_roll
        return self

def run_raw_results(dice_count : int, run_count:int)->pd.Series:
    output : np.ndarray = np.empty(run_count * (dice_count-1), dtype=np.int64)
    for i in range(run_count):
        counter=0
        results = OriginalRoll(dice_count).roll_dice().calculate_results().results
        for x in results:
            output[(i*(dice_count-1))+counter]=x
            counter=counter+1
    pd_output = pd.Series(output)
    return pd_output

def run_agg_results(dice_count:int, run_count:int, agg_func)->pd.Series:
    output : np.ndarray = np.empty(run_count , dtype=np.int64)
    for i in range(run_count):
        counter=0
        results = OriginalRoll(dice_count).roll_dice().calculate_results().results
        output[i] = agg_func(results)
    pd_output = pd.Series(output)
    return pd_output


    