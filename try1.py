import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Preprocess the dataset
dataset = pd.read_csv('D:/fastApiProject1/newest.csv', encoding='latin1', nrows=100)

# Split multi-valued columns
dataset['studylevel'] = dataset['studylevel'].str.split(',')
dataset['familyincome'] = dataset['familyincome'].str.split(',')
dataset['major'] = dataset['major'].str.split('-')

# Step 2: Convert categorical variables to numerical representations
one_hot_encoded = pd.get_dummies(dataset['identity']).add_prefix('identity_')
one_hot_encoded = pd.concat([one_hot_encoded, pd.get_dummies(dataset['state']).add_prefix('state_')], axis=1)

for column in ['studylevel', 'familyincome', 'major']:
    categories = set(category for categories_list in dataset[column] for category in categories_list)
    for category in categories:
        one_hot_encoded[column + '_' + category] = dataset[column].apply(lambda x: int(category.strip().lower() in [val.strip().lower() for val in x]))

# Step 3: Define input_aid and get common columns between input vector and dataset vectors
input_aid = {
    'studylevel': ['Bachelor'],
    'familyincome': ['b40'],
    'cgpa': 3.5,
    'major': ['plantation'],
    'identity': ['default'],
    'state': ['default']
}

common_columns = set(one_hot_encoded.columns) & set(pd.get_dummies(pd.DataFrame(input_aid)).columns)

# Step 4: Calculate similarity
def get_similarity(input_vector, dataset_vector):
    input_vector = input_vector.reshape(1, -1)
    dataset_vector = dataset_vector.reshape(1, -1)
    return cosine_similarity(input_vector[:, :dataset_vector.shape[1]], dataset_vector[:, :dataset_vector.shape[1]])[0][0]

input_cgpa = input_aid['cgpa']

# Convert input_cgpa to range format
input_cgpa_range = str(input_cgpa) + ',' + str(input_cgpa)

input_aid['cgpa'] = input_cgpa_range

input_vector = pd.get_dummies(pd.DataFrame(input_aid)).reindex(columns=common_columns, fill_value=0).values.flatten()

# Convert CGPA column in dataset to range format
dataset['cgpa'] = dataset['cgpa'].apply(lambda x: str(x) + ',' + str(x))

dataset_vectors = one_hot_encoded.reindex(columns=common_columns, fill_value=0).values
similarities = [get_similarity(input_vector, dataset_vector) for dataset_vector in dataset_vectors]

# Step 5: Rank the financial aid entries
dataset['similarity'] = similarities
ranked_aid = dataset.sort_values('similarity', ascending=False)

# Step 6: Calculate similarity percentage
ranked_aid['similarity_percentage'] = ranked_aid['similarity'] * 100

# Step 7: Return recommended financial aid options (finaidname) with similarity percentage
recommended_aid = ranked_aid.head(20)[['finaidname', 'similarity_percentage']].values.tolist()

# Print the recommended financial aid options with similarity percentage
for aid in recommended_aid:
    print(f"Financial Aid: {aid[0]}, Similarity: {aid[1]:.2f}%")
