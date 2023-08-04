import pandas as pd
import numpy as np

# Step 1: Preprocess the dataset
dataset = pd.read_csv('D:/fastApiProject1/trainnew.csv', encoding='latin1', nrows=100)

# Split multi-valued columns
dataset['studylevel'] = dataset['studylevel'].str.split(',')
dataset['familyincome'] = dataset['familyincome'].str.split(',')
dataset['major'] = dataset['major'].str.split('-')

# Custom function to calculate Jaccard similarity between two sets
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return (intersection / union) * 100  # Convert to percentage

# Step 4: Calculate similarity
def get_similarity(user_input, dataset_entry):
    similarity_scores = []
    for column_name in ['studylevel', 'familyincome', 'major', 'identity', 'state']:
        user_input_set = set(user_input[column_name])
        dataset_entry_set = set(dataset_entry[column_name])
        similarity = jaccard_similarity(user_input_set, dataset_entry_set)
        similarity_scores.append(similarity)

    return np.mean(similarity_scores)  # Take the mean of individual Jaccard similarities

# Step 6: Filter financial aid options based on user criteria
user_study_level = 'degree'
user_family_income = 'b40'
user_cgpa = 4
user_subcategory = 'medicine'
user_identity = 'all'
user_state = 'all'

filtered_aid = dataset[
    (dataset['studylevel'].apply(lambda x: isinstance(x, list) and user_study_level.lower() in [level.lower() for level in x])) &
    (dataset['familyincome'].apply(lambda x: any(user_family_income.lower() in val.lower() for val in x))) &
    (dataset['major'].apply(lambda x: any(user_subcategory.lower() in val.lower() for val in x))) &
    (dataset['identity'].apply(lambda x: user_identity.lower() in x.lower())) &
    (dataset['state'].apply(lambda x: user_state.lower() in x.lower())) &
    ((dataset['cgpa'].apply(lambda x: float(x.split(',')[0])) <= user_cgpa) &
     (dataset['cgpa'].apply(lambda x: float(x.split(',')[1])) >= user_cgpa))
]

# Step 7: Calculate similarities for all filtered financial aid options
def calculate_similarities(user_input):
    similarities = [get_similarity(user_input, dataset_entry) for dataset_entry in filtered_aid.to_dict(orient='records')]
    return similarities

# Convert user input to a DataFrame
user_input = pd.DataFrame({
    'studylevel': [user_study_level],
    'familyincome': [user_family_income],
    'cgpa': [user_cgpa],
    'major': [user_subcategory],
    'identity': [user_identity],
    'state': [user_state]
})

# Calculate similarities for user input and filtered financial aid options
filtered_aid['similarity'] = calculate_similarities(user_input)

# Step 8: Sort financial aid options by similarity in descending order
filtered_aid_sorted = filtered_aid.sort_values(by='similarity', ascending=False)

# Format similarity scores with two decimal places
filtered_aid_sorted['similarity'] = filtered_aid_sorted['similarity'].apply(lambda x: '{:.2f}'.format(x))

print("Filtered Aid:")
print(filtered_aid_sorted[['finaidname', 'similarity']])
