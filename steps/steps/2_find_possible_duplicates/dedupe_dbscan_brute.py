import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from typing import Dict, List, Set

similarity_weights = np.array([60,60,60,15,15,6,4,3,2])

def jaccard_similarity(str1, str2):
    a = set(str(str1).split())
    b = set(str(str2).split())
    return float(len(a.intersection(b))) / len(a.union(b))

def create_columns(base_columns:List[str],similarity_allowances:List[float],modified_naming_suffix:str=""):
    for column, similarity in tqdm(list(zip(base_columns,similarity_allowances)),"Creating Columns in Relation to " + modified_naming_suffix):
        similarity_matrix = cosine_similarity(df[column].apply(lambda x: np.array([jaccard_similarity(x, y) for y in df[column]])).tolist())

        # Normalize the similarity matrix to ensure values are between 0 and 1
        similarity_matrix = np.clip(similarity_matrix, 0, 1)

        # Standardize features
        # scaler = StandardScaler()
        # X_scaled = scaler.fit_transform(similarity_matrix)

        # Apply DBSCAN
        db = DBSCAN(eps=similarity, min_samples=2, metric='precomputed')
        labels = db.fit_predict(1 - similarity_matrix)  # Use 1 - similarity_matrix for distance-based clustering

        # Add cluster labels to the DataFrame
        df[column + modified_naming_suffix] = labels

def analyze_similarities(focused_df_rows: pd.core.frame.DataFrame, duplicates: Set[str]) -> None:
    while len(focused_df_rows) > 1:
        current_row = focused_df_rows.iloc[0].name
        for row_index in focused_df_rows.index[1:]:
            # Compute similarities
            similarities = focused_df_rows.loc[[current_row,row_index]].nunique().values
            strict_similarities = np.where(similarities[:9] == 1, 1, 0) 
            lax_similarities = np.where(similarities[9:-1] == 1, .5, 0)
            similarities_condensed = np.maximum(strict_similarities,lax_similarities)
            # reassess tax_id similarity for ssn tax id mismatch potential
            if similarities[-1] == 2 and similarities_condensed[0] == 0.0:
                similarities_condensed[0] = .5
            # Assess similarities for duplicates
            if sum(similarities_condensed * similarity_weights) > 120:
                duplicates.add(f"{current_row},{row_index}")
        # Remove the First Row As It Was Analyzed
        focused_df_rows = focused_df_rows.iloc[1:]

def find_similarities_two_column_basis(base_column_1:str,base_column_2:str,
    similarity_df:pd.core.frame.DataFrame,duplicates:Set[str]):
    """Using two columns to find some reasonbly likely candidates for duplicates analyze specific rows for duplicates"""
    for element in tqdm(list(similarity_df.loc[(similarity_df[base_column_1] != -1)&(similarity_df[base_column_2] != -1)].groupby([base_column_1,base_column_2]).count().index),f"Analyzing Pairings of {base_column_1} and {base_column_2}"): 
        focused_df_rows = similarity_df[(similarity_df[base_column_1] == element[0])&(similarity_df[base_column_2] == element[1])] 
        analyze_similarities(focused_df_rows,duplicates)

def find_similarities_three_column_basis(base_column_1:str,base_column_2:str,base_column_3:str,
    similarity_df:pd.core.frame.DataFrame,duplicates:Set[str]):
    """Using three columns to find some reasonbly likely candidates for duplicates analyze specific rows for duplicates; these are expected to be weaker than two columns alone, but with three to be reasonable."""
    for element in tqdm(list(similarity_df.loc[(similarity_df[base_column_1] != -1)&(similarity_df[base_column_2] != -1)&(similarity_df[base_column_3] != -1)].groupby([base_column_1,base_column_2,base_column_3]).count().index),"Analyzing for Duplicates Across Three Columns"): 
        focused_df_rows = similarity_df[(similarity_df[base_column_1] == element[0])&(similarity_df[base_column_2] == element[1])&(similarity_df[base_column_3] == element[2])] 
        analyze_similarities(focused_df_rows,duplicates)

def deduplicate_db_scan_core_personal_elements(df) -> Dict[str,int]:
    duplicates = set()

    # Label Similar Items
    create_columns(['Tax ID/SSN', 'Name', 'Date Of Birth', 'Phone Number', 'Email', 'State', 'City', 'Zip', 'Street Address'],[0.00000001,0.00000001,0.00000001,0.00000001,0.00000001,0.00000001,0.00000001,0.00000001,0.00000001],"_Similarity_Strict")
    create_columns(['Tax ID/SSN', 'Name', 'Date Of Birth', 'Phone Number', 'Email', 'State', 'City', 'Zip', 'Street Address'],[0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2],"_Similarity_Lax")
    
    # To be used as a way to recognize possible matches that aren't as strong but matches
    df["is_ssn?"] = df["Tax ID/SSN"].apply(lambda x: x[0] != 9)

    # Focus Down the DataFrame
    similarity_df = df[['Tax ID/SSN_Similarity_Strict', 'Name_Similarity_Strict',
       'Date Of Birth_Similarity_Strict', 'Phone Number_Similarity_Strict',
       'Email_Similarity_Strict', 'State_Similarity_Strict',
       'City_Similarity_Strict', 'Zip_Similarity_Strict',
       'Street Address_Similarity_Strict', 'Tax ID/SSN_Similarity_Lax',
       'Name_Similarity_Lax', 'Date Of Birth_Similarity_Lax',
       'Phone Number_Similarity_Lax', 'Email_Similarity_Lax',
       'State_Similarity_Lax', 'City_Similarity_Lax', 'Zip_Similarity_Lax',
       'Street Address_Similarity_Lax',"is_ssn?"]]
    
    # Assuming that name, tax id/ssn, and birthdate are the main three elements 
    # that should relate to each other; I'm taking pairings of those strictly
    # to find reasonable connections or all three with at least some lax similarity
    find_similarities_two_column_basis("Tax ID/SSN_Similarity_Strict","Name_Similarity_Strict",similarity_df,duplicates)
    find_similarities_two_column_basis(
        "Date Of Birth_Similarity_Strict","Name_Similarity_Strict",similarity_df,duplicates)
    find_similarities_two_column_basis(
        "Tax ID/SSN_Similarity_Strict","Date Of Birth_Similarity_Strict",similarity_df,duplicates)
    find_similarities_three_column_basis(
        "Tax ID/SSN_Similarity_Lax","Name_Similarity_Lax","Date Of Birth_Similarity_Lax",similarity_df,duplicates)
    duplicates_dictionary = {}
    for duplicate in duplicates:
        i1, i2 = [int(x) for x in duplicate.split(",")]
        if len(duplicates_dictionary.get(i1,[])) == 0:
            duplicates_dictionary[i1] = []    
        duplicates_dictionary[i1].append(i2)
    return duplicates_dictionary
    
        
        
        
    # Similarity Testing for Tweaking Parameters
    # similarity_analysis = "Tax ID/SSN"
    # for similarity_analysis in ['Tax ID/SSN','Name', 'Date Of Birth','Phone Number', 'Email', 'State','City', 'Zip', 'Street Address']:
    #     print(similarity_analysis)
    #     all_values = set(pd.unique(df[similarity_analysis+"_Similarity"])).difference([-1])
    #     for value in all_values:
    #         if df.loc[df[similarity_analysis+"_Similarity"]==value][[similarity_analysis,similarity_analysis+"_Similarity"]].nunique().iloc[0] != 1:
    #             print(df.loc[df[similarity_analysis+"_Similarity"]==value][[similarity_analysis,similarity_analysis+"_Similarity"]])

    # exploration_space = {}
    # fixed_elements = []
    # columns_list = df.columns.tolist()
    # column_len = len(columns_list)

    # main_column = columns_list[0]
    # exploration_space[main_column] = pd.unique(df[main_column]).tolist()
    # focused_df_rows = df.copy()
    # current_column = main_column
    # similarity_weights = np.array([30,30,30,15,15,6,4,3,2])
    # explored = []

    # # tracking row information
    # duplicates = []
    # next_group = False
    # while len(exploration_space[main_column]) > 0:
    #     # Focus the df down to the current elements
    #     current_exploration_value = exploration_space[current_column].pop()
    #     focused_df_rows = focused_df_rows[
    #         focused_df_rows[current_column] == current_exploration_value
    #         ]
    #     # Determine current status of exploration
    #     if len(focused_df_rows) == 2:
    #         similarity = [1 if x == 1 else 0 for x in focused_df_rows.nunique().to_list()]
    #         current_sum = sum(np.array(similarity) * similarity_weights)
    #         next_group = True
    #     else:
    #         fixed_elements.append(current_exploration_value)
    #         current_sum = sum(np.array([1 if x != -1 else 0 for x in fixed_elements]) * similarity_weights[:len(fixed_elements)])
    #     # If duplicate stop going farther
    #     if current_sum >= 90: 
    #         duplicates.append(focused_df_rows.index.to_list())
    #         next_group = True
    #     # If it can't be a duplicate with the remaining items move on 
    #     elif next_group:
    #         pass # just keep going
    #     elif (len(fixed_elements) == 2 and current_sum == 0) or (len(fixed_elements) == 3 and current_sum == 30) or (len(fixed_elements) == 5 and current_sum <= 60):
    #         next_group = True
    #     # If not determined look at the next column if it exists
    #     elif len(fixed_elements) < column_len:
    #         exploration = f"{fixed_elements[0]}-{len(fixed_elements)}"
    #         if not exploration in explored:
    #             current_column = columns_list[len(fixed_elements)]
    #             exploration_space[current_column] = pd.unique(df[current_column]).tolist()
    #             explored.append(exploration)
    #     # Or there's nothing else to consider
    #     else:
    #         next_group = True
    #     if next_group:
    #         if len(fixed_elements) > 0:
    #             fixed_elements.pop()
    #         current_column = columns_list[len(fixed_elements)]
    #         focused_df_rows = df.copy()
    #         for i, element in enumerate(fixed_elements):
    #             focused_df_rows = focused_df_rows[focused_df_rows.iloc[0] == element]
    # duplicate_dictionary = {}
    # for item in duplicates:
    #     if len(duplicate_dictionary.get(item[0],[])) == 0:
    #         duplicate_dictionary[item[0]] = []
    #     for match in item[1:]:
    #         duplicate_dictionary[item[0]].append(match)
    # return duplicate_dictionary

if __name__ == "__main__":
    df = pd.read_csv(r'C:\Users\austin.tracy\Documents\Deduplication\steps\1_generate_data\data\fake_deduplication_data_v2_small.csv')
    db_scan_v2 = deduplicate_db_scan_core_personal_elements(df)
