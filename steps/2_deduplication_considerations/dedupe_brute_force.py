"""This deduplication method is to give us some sense of a baseline for deduplication. 
This is a less machine learning centric approach and relies more on careful considerations
of each record. A small batch is of little concern, but with the potentiality of 100,000
customers this might take significant processing time. Specifically, this takes the method
of grouping by the TAX/SSN ID column, the phone number column, and the email column to find
any matching values (more unique and id like columns). For any matches, it compares each pair of matching rows within those groupings by considering every column for the strength of the relationship. These figures are output to a csv with the potential matches.

The results can then be considered according to their connection strength (some number between 16 and 164)"""
import re
from typing import Dict, List, Any

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from data_cleaning import *
from typo_checking import *

##################
# Settings
##################
# Turning this off to speed things up, but if you have a better solution to the warning messages...
pd.options.mode.chained_assignment = None

##################
# Data
##################
# Load the model
model_name = 'Snowflake/snowflake-arctic-embed-l-v2.0'
model = SentenceTransformer(model_name)

##################
# Functions
##################
def get_cluster_exact_match_elements(df: pd.core.frame.DataFrame, column_name: str) -> List:
    grouping = pd.DataFrame(df.groupby(column_name).count().iloc[:,1])
    grouping.columns = ["# Rows Grouped"]
    grouping = grouping.reset_index()
    return grouping.loc[grouping["# Rows Grouped"]>1].iloc[:,0].to_list()

#*#*#*#*#*#*#*#*#
# Similarity Functions
#*#*#*#*#*#*#*#*#
def get_encoding(text: str, temp_memory: Dict[str,List[float]]) -> List[float]:
    saved_encoding = temp_memory.get(text,[])
    if len(saved_encoding) > 0:
        return saved_encoding
    else:
        encoding = model.encode(text)
        temp_memory[text] = encoding
        return encoding

def test_name_similarity(current_name:str, other_name:str, temp_memory = {}) -> int:
    """4 = a true match
    3 = it's reasonable
    0 = not a close match"""
    # current_name, other_name = row[column_name],compared_row[column_name]
    if current_name.lower().strip() == other_name.lower().strip():
        return 4
    elif quick_typo_check(current_name,other_name):
        query_embedding = model.encode(current_name)
        if np.linalg.norm(query_embedding - get_encoding(other_name,temp_memory)) < 1:
            return 3
        else:
            return 0
    else:
        return 0

def test_id_similarity(current_id:Any, other_id:Any) -> int:
    """4 = a true match
    3-1 = it's close
    0 = not a close match"""
    current_id = str(current_id)
    other_id = str(other_id)
    if current_id == other_id or current_id is None or other_id is None:
        return 4
    if quick_typo_check(current_id,other_id):
        query_embedding = model.encode(current_id)
        typo_measurement = either_way_typo_measurement(current_id,other_id)
        if either_way_typo_measurement(current_id,other_id) < 4:
            return 4 - typo_measurement
        else:
            return 0
    else:
        return 0

def test_one_column_of_row_similarity(row: pd.Series, df: pd.core.frame.DataFrame, column_name: str, function_to_apply: callable) -> None:
    """This exists because of a weird unexplained error. It came from the df[column_name].apply(lambda x: test_name_similarity(x,row[column_name])) part, but inexplicably seemed the same as other columns. City was the only one affected...it seemed"""
    similarity_column = column_name.replace(" ","_") + "_Similarity"
    try:
        df.loc[df.index == df.index,similarity_column] = df[column_name].apply(lambda x: function_to_apply(x,row[column_name]))
    except:
        df.loc[df.index == df.index,similarity_column] = None
        for _, compared_row in df.iterrows():
            score = function_to_apply(row[column_name],compared_row[column_name])
            df.loc[df.index == compared_row.name,column_name.replace(" ","_") + "_Similarity"] = score

def test_similarity_to_row(row: pd.Series, df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    test_one_column_of_row_similarity(row,df,"Name",test_name_similarity)
    test_one_column_of_row_similarity(row,df,"Street Address",test_name_similarity)
    test_one_column_of_row_similarity(row,df,"City",test_name_similarity)
    test_one_column_of_row_similarity(row,df,"State",test_name_similarity)
    test_one_column_of_row_similarity(row,df,"Zip",test_id_similarity)
    test_one_column_of_row_similarity(row,df,"Tax ID/SSN",test_id_similarity)
    test_one_column_of_row_similarity(row,df,"Phone Number",test_id_similarity)
    test_one_column_of_row_similarity(row,df,"Email",test_id_similarity)
    test_one_column_of_row_similarity(row,df,"Date Of Birth",test_id_similarity)
    return df

def brute_force_dedupe(deduplication_file_csv_location: str):
    version_match = re.search(r"(?<=\_v)[0-9]+(?=(\.csv)|\_)",deduplication_file_csv_location)
    version_number = version_match.group() if version_match != None else -1 # -1 for a default
    df = pd.read_csv(deduplication_file_csv_location)
    clean_phone_numbers(df,"Phone Number")
    regularize_us_phone_numbers(df,"Phone Number","State")
    for metric in tqdm(['Tax ID/SSN', 'Email', 'Phone Number'], desc="Metric:"):
        for clustering_item in tqdm(get_cluster_exact_match_elements(df,metric),desc="Clustering Items:"):
            clustered_elements = df.loc[df[metric] == clustering_item]
            current_row_to_consider_for_duplicate = clustered_elements.iloc[0]
            remaining_elements = clustered_elements.iloc[1:]
            while len(remaining_elements) > 0:
                test_df = test_similarity_to_row(current_row_to_consider_for_duplicate,remaining_elements)
                for _, row in test_df.iterrows():
                    similarity_scores = (row.iloc[-9:] * np.array([8,1,1,2,1,10,4,4,10])).to_list()
                    # The multiplication is dependent on column ordering
                    similarity_score = sum(similarity_scores)
                    with open(r"steps/2_deduplication_considerations/data_brute/" + f"brute_similarity_scores_v{version_number}.txt","a+") as f:
                        tab = "\t"
                        _ = f.write(f"{current_row_to_consider_for_duplicate.name}{tab}{row.name}{tab}{tab.join([str(x) for x in similarity_scores])}{tab}{similarity_score}\n")
                current_row_to_consider_for_duplicate = remaining_elements.iloc[0]
                remaining_elements = remaining_elements.iloc[1:]

if __name__ == "__main__":
    deduplication_file_csv_location = r'C:\Users\austin.tracy\Documents\Deduplication\steps\1_fake_data\data\fake_deduplication_data_v1_small.csv'
    brute_force_dedupe(deduplication_file_csv_location)
    