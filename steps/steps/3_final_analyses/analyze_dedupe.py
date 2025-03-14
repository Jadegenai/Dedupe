import numpy as np
import pandas as pd
import pyautogui
from typing import Dict, Set

from data_cleaning import *

def get_pairings(dictionary: Dict[int,int]) -> Set:
    pairings = set()
    for key in dictionary.keys():
        matches = dictionary[key]
        pairings = pairings.union(set([f"{key},{match}" for match in matches] if type(matches) == list or type(matches) == np.ndarray else [f"{key},{matches}"]))
    return pairings

if __name__ == "__main__":
    og_df = pd.read_csv(r"steps\1_generate_data\data\fake_deduplication_data_v2_small.csv")
    clean_phone_numbers(og_df,"Phone Number")
    regularize_us_phone_numbers(og_df,"Phone Number","State")

    # Run Programs for Finding Possible Duplicates (Step 2)
    # Then you can plug them in here
    dictionary_1 = duplicates_brute[1]
    dictionary_2 = db_scan_v2

    pairings_1 = get_pairings(dictionary_1)
    pairings_2 = get_pairings(dictionary_2)
    differences_1 = pairings_1.difference(pairings_2)
    differences_2 = pairings_2.difference(pairings_1)
    similarities = pairings_1.intersection(pairings_2)
    import random
    len(differences_1)
    len(differences_2)
    i1, i2 = random.choice(list(differences_1)).split(",")
    og_df.loc[[int(i1),int(i2)]]

    i1, i2 = random.choice(list(differences_2)).split(",")
    og_df.loc[[int(i1),int(i2)]]

    len(differences_1)
    len(differences_2)
