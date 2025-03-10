import pandas as pd
import pyautogui

from data_cleaning import *

og_df = pd.read_csv(r"steps\1_generate_data\data\fake_deduplication_data_v1_small.csv")
clean_phone_numbers(og_df,"Phone Number")
regularize_us_phone_numbers(og_df,"Phone Number","State")

df = pd.read_csv(r"steps\2_deduplication_considerations\data_brute\brute_similarity_scores_v1.txt",sep="\t",header=None)
df.sort_values(11)

match_patterns = df.iloc[:,2:11][df.iloc[:,2:11].duplicated(subset=[2,3,4,5,6,7,8,9,10])==False]

for _, pattern in list(match_patterns.iterrows())[4:]:
    pattern_df = df.loc[df.iloc[:,2:11].apply(lambda row: all(row.fillna(0) == pattern.fillna(0)), axis=1)]
    print(pattern.sum())
    print(pattern.to_list())
    for i in range(3):
        random_sample = pattern_df.sample(n=1)
        og_df.loc[random_sample[0]].iloc[0].to_list()
        og_df.loc[random_sample[1]].iloc[0].to_list()
    pyautogui.alert("Another Pattern Has Been Printed...")
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n")


    

