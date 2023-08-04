import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.cluster import KMeans

# Step 2: Dataset preparation and feature engineering
df = pd.read_csv('D:/fastApiProject1/trainnew.csv', encoding='latin1', nrows=100)

# Define a dictionary to map the major positions
major_positions = {
    0: 'Applied Sciences',
    1: 'Civil Engineering',
    2: 'Electrical Engineering',
    3: 'Medicine',
    4: 'Sports Science & Recreation',
    5: 'Architecture, Planning & Surveying',
    6: 'Computer & Mathematical Sciences',
    7: 'Health Sciences',
    8: 'Pharmacy',
    9: 'Chemical Engineering',
    10: 'Dentistry',
    11: 'Mechanical Engineering',
    12: 'Plantation & Agrotechnology',
    13: 'Administrative Science & Policy Studies',
    14: 'Education',
    15: 'Music',
    16: 'Art & Design',
    17: 'Film, Theater & Animation',
    18: 'Communication & Media Studies',
    19: 'Law',
    20: 'Accountancy',
    21: 'Information Management',
    22: 'Business & Management',
    23: 'Hotel & Tourism Management'
}

# Split the major data into separate columns based on position
for pos, major_name in major_positions.items():
    df[major_name] = df['major'].apply(lambda x: major_name in x)

# Drop the original 'major' column
df.drop('major', axis=1, inplace=True)

# Convert the studylevel lists to strings
df['studylevel'] = df['studylevel'].apply(lambda x: ','.join(x))

# Encode categorical variables using OneHotEncoder
enc = OneHotEncoder(sparse=False, handle_unknown='ignore')

studylevel_encoded = enc.fit_transform(df['studylevel'].values.reshape(-1, 1))
familyincome_encoded = enc.fit_transform(df['familyincome'].values.reshape(-1, 1))

# Normalize numerical variable using Min-Max scaling
scaler = MinMaxScaler()
cgpa_normalized = df['cgpa'].apply(lambda x: [float(val) for val in x.split(',')]).values.tolist()
cgpa_normalized = scaler.fit_transform(cgpa_normalized)



# Combine encoded features with CGPA into a new DataFrame
features = pd.DataFrame(
    data={
        'studylevel_encoded': studylevel_encoded.tolist(),
        'familyincome_encoded': familyincome_encoded.tolist(),
        'cgpa_normalized': cgpa_normalized.flatten()
    }
)




# Step 3: Apply clustering algorithm (K-means)
kmeans = KMeans(n_clusters=3)  # Specify the desired number of clusters
kmeans.fit(features)

# Step 4: Assign clusters to the data points
cluster_labels = kmeans.predict(features)
df['cluster_label'] = cluster_labels

# Print the cluster labels for each data point
print(df[['finaidname', 'cluster_label']])

# Access the scholarships/financial aid programs within a specific cluster
cluster_id = 0  # Specify the cluster ID of interest
cluster_data = df[df['cluster_label'] == cluster_id]
print(cluster_data)
