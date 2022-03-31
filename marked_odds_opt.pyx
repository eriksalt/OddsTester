import numpy as np
import random as rand

def roll_dice_opt(dice_count: int, rolls: np.ndarray):
    max_value: int = -1
    max_index: int = -1
    for i in range(dice_count):
        roll = (int(10 * rand.random())) + 1
        rolls[i] = roll
        if roll > max_value:
            max_value = roll
            max_index = i
    # swap largest value to end
    rolls[dice_count - 1], rolls[max_index] = rolls[max_index], rolls[dice_count - 1]
    return rolls

def calculate_results(rolls:np.ndarray)->np.ndarray:
    max_roll: int = rolls[-1]
    return  rolls[:-1] + max_roll
    