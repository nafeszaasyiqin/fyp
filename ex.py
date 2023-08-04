import pandas as pd

dataset = pd.read_csv('D:/fastApiProject1/test.csv', encoding='latin1', nrows=100)


def recommend_financial_aids(study_level, family_income, cgpa, major):
    recommended_aids = []

    filtered_dataset = dataset[
        (dataset['studylevel'].str.lower().str.contains(study_level.lower())) &
        (dataset['familyincome'].str.lower().str.contains(family_income.lower())) &
        ((dataset['major'].str.lower().str.contains(major.lower())) | (major.lower() == 'all'))
    ]

    if filtered_dataset.empty:
        print("No financial aids found for the given criteria.")
    else:
        for index, row in filtered_dataset.iterrows():
            cgpa_range = row['cgpa'].split(',')
            lower_range = float(cgpa_range[0].strip())
            upper_range = float(cgpa_range[1].strip())

            user_cgpa = float(cgpa)
            if user_cgpa >= lower_range and user_cgpa <= upper_range:
                recommended_aids.append(row)

        if len(recommended_aids) == 0:
            print("No recommendations found for the given criteria.")
        else:
            print("Recommended financial aids:")
            for aid in recommended_aids:
                print(aid['finaidname'], "-", aid['finaidlink'])


study_level = 'Foundation'
family_income = 'B40'
cgpa = '4.00'
major = 'ALL'

recommend_financial_aids(study_level, family_income, cgpa, major)
