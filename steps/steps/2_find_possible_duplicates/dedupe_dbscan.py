import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df = pd.read_csv(r'C:\Users\austin.tracy\Documents\Deduplication\steps\1_generate_data\data\fake_deduplication_data_v2_small.csv')

# Feature Engineering - Create a similarity matrix
# For simplicity, we're assuming 'name' and 'address' fields
def jaccard_similarity(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    return float(len(a.intersection(b))) / len(a.union(b))

def deduplicate_db_scan_core_personal_elements(df):
    df['core_personal_elements'] = df['Name'] + ' ' + df['Tax ID/SSN'] + ' ' + df["Date Of Birth"]
    similarity_matrix = cosine_similarity(df['core_personal_elements'].apply(lambda x: np.array([jaccard_similarity(x, y) for y in df['core_personal_elements']])).tolist())

    # Normalize the similarity matrix to ensure values are between 0 and 1
    similarity_matrix = np.clip(similarity_matrix, 0, 1)

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(similarity_matrix)

    # Apply DBSCAN
    db = DBSCAN(eps=0.2, min_samples=2, metric='precomputed')
    labels = db.fit_predict(1 - similarity_matrix)  # Use 1 - similarity_matrix for distance-based clustering

    # Add cluster labels to the DataFrame
    df['cluster'] = labels
    pd.unique(df['cluster'])

    list_of_clustered_items = df.loc[df['cluster'] != -1][["cluster"]].reset_index().groupby("cluster").agg(lambda x: [x])
    duplicate_dictionary_for_db_scan = {}
    for _, listing in list_of_clustered_items.iterrows():
        usable_list_type = listing["index"][0].to_list()
        duplicate_dictionary_for_db_scan[usable_list_type[0]] = usable_list_type[1:]
    return duplicate_dictionary_for_db_scan

duplicate_dictionary_for_db_scan = deduplicate_db_scan_core_personal_elements(df)

# # Convert back to DataFrame
# deduplicated_df = pd.DataFrame(deduplicated_records)
# deduplicated_df = pd.concat([df[df['cluster'] == cluster].drop("cluster",axis=1),deduplicated_df])

# # Save deduplicated data
# deduplicated_df.to_csv('deduplicated_data.csv', index=False)