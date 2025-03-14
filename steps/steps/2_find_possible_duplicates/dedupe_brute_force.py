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
    3-1 = it's reasonable
    0 = not a close match"""
    # current_name, other_name = row[column_name],compared_row[column_name]
    current_name = current_name.lower().strip()
    other_name = other_name.lower().strip()
    if current_name == other_name:
        return 4
    query_embedding = model.encode(current_name)
    if np.linalg.norm(query_embedding - get_encoding(other_name,temp_memory)) < 1:
        return 3
    
    # Considerations about misentering
    typo_measurement = either_way_typo_measurement(current_name,other_name)
    # assess hearing as a different factor if typos are more than just 1
    # hearing should be more intensive of a consideration, so it is held off
    if typo_measurement > 1:
        typo_measurement = min(typo_measurement,either_way_mishearing_measurement(current_name,other_name))
    if typo_measurement < 4:
        return 4 - typo_measurement
    else:
        return 0

def test_id_similarity(current_id:Any, other_id:Any) -> int:
    """This function unlike the name function expects an exact match or it to be
    something different (that is whereas a name can have parts omitted and still be
    the same name [just presented in part] an email is technically completely different
    if not presented in full...) There may be some similarity between email addresses that can be
    missed in treating it in this manner, but an email is not the same email as another if its
    any different...
    4 = a true match
    3-1 = it's close
    0 = not a close match"""
    current_id = str(current_id)
    other_id = str(other_id)
    if current_id == other_id or current_id is None or other_id is None:
        return 4
    if quick_typo_check(current_id,other_id):
        typo_measurement = either_way_typo_measurement(current_id,other_id)
        # assess hearing as a different factor if typos are more than just 1
        # hearing should be more intensive of a consideration, so it is held off
        if typo_measurement > 1:
            typo_measurement = min(typo_measurement,either_way_mishearing_measurement(current_id,other_id))
        if typo_measurement < 4:
            return 4 - typo_measurement
        else:
            return 0
    else:
        return 0

def test_tax_ssn_similarity(current_id:Any, other_id:Any) -> int:
    """This function unlike the name function expects an exact match or it to be
    something different (that is whereas a name can have parts omitted and still be
    the same name [just presented in part] an email is technically completely different
    if not presented in full...) There may be some similarity between email addresses that can be
    missed in treating it in this manner, but an email is not the same email as another if its
    any different...
    4 = a true match
    3-1 = it's close
    0 = not a close match"""
    same_id_similarity_score = test_id_similarity(current_id,other_id)
    if same_id_similarity_score >= 2:
        return same_id_similarity_score
    else:
        if ((str(current_id[0]) == '9') ^ (str(other_id[0]) == 9)):
            return 2 # Not as good as a single digit difference of an id, but just after that as a potential match with potential identifiers that could be to the same person
        else:
            return same_id_similarity_score

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
    test_one_column_of_row_similarity(row,df,"Tax ID/SSN",test_tax_ssn_similarity)
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
    for metric in tqdm(['Email', 'Phone Number','Tax ID/SSN'], desc="Metric:"):
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


def get_duplicates_from_field_similarity_scores_simple(og_df: pd.core.frame.DataFrame, df: pd.core.frame.DataFrame):
    """The simple version just uses the overall score closer to the original design"""
    identified_duplicates = df.loc[df[11] >= 84] #oversimplified
    identified_duplicates = identified_duplicates[[0,1]].groupby(0).agg(lambda x: x)
    og_df.loc[[0,1582]]

def get_duplicates_from_field_similarity_scores_simple_v2(df: pd.core.frame.DataFrame):
    """
    Warning! This version expects adjustments to the score to weight name, birthdate, and id far above the others that more commonly people might share with related people around them. The address is deweighted as the least helpful item (that is the most likely to be shared by unrelated people).
    The simple version just uses the overall score closer to the original design"""
    # Adjustments
    # df
    
    
    # Not duplicates
    # current_considerations = df.loc[df[11] < 81].sort_values(11)
    # # Maybe duplicates; they have at least 2 of the core items matched
    # df.loc[(df[11] >= 81)&(df[11] < 125)].sort_values(11)
    # # Duplicates
    # df.loc[df[11] >= 125].sort_values(11)
    
    # i1, i2 = current_considerations.sample(n=1).iloc[0,0:2]
    # og_df.loc[[i1,i2]].to_dict()


    # address up to 12
    # email up to 16
    # phone up to 16
    # name up to 48 (36 is okay)
    # id up to 60 (30 might be okay)
    # birth up to 60 (30 is okay 20 is pushing it)
    identified_duplicates = df.loc[df[11] >= 125] #oversimplified
    identified_duplicates = identified_duplicates[[0,1]].groupby(0).agg(lambda x: x)
    return identified_duplicates

if __name__ == "__main__":
    # Super Slow Process...
    deduplication_file_csv_location = r'steps\1_generate_data\data\fake_deduplication_data_v2_small.csv'
    brute_force_dedupe(deduplication_file_csv_location)
    
    # Opening File from that Slower Process
    df = pd.read_csv(r"steps\2_find_possible_duplicates\data_brute\brute_similarity_scores_v2.txt",sep="\t",header=None)
    for i in range(3,6):
        df[i] = df[i] /2
    for i in [2,7,10]:
        df[i] = df[i] * 1.5
    df[11] = df.iloc[:,2:11].apply(lambda row: sum(row),axis=1)
    duplicates_brute = get_duplicates_from_field_similarity_scores_simple_v2(df).to_dict()