def recommend_financial_aid(study_level, major_of_study, family_income, cgpa_range):
    recommendations = []  # List to store the recommended options

    # Convert the CGPA range to the lower and upper bounds
    if cgpa_range:
        cgpa_lower, cgpa_upper = map(float, cgpa_range.split(' - '))
    else:
        cgpa_lower, cgpa_upper = 0.0, 0.0

    if study_level == 'foundation' and major_of_study == 'all' and family_income == 'all':
        recommendations.append('Bantuan Kewangan Asasi IPTA')
    if study_level == 'degree' and major_of_study == 'all' and family_income == 'b40' and cgpa_lower >= 3.0:
        recommendations.append('Biasiswa Cagamas Scholarship Programme')
    if study_level == 'degree' and major_of_study == 'all' and family_income == 'b40' and cgpa_lower >= 3.5:
        recommendations.append('Biasiswa Gadang Scholarship')
    if study_level == 'degree' and major_of_study == 'all' and cgpa_lower >= 3.5:
        recommendations.append('Biasiswa Bank Negara Malaysia Scholarship – Undergraduate')
        recommendations.append('Biasiswa Gamuda Scholarship 2023')
        recommendations.append('Biasiswa Great Eastern Scholarship')
    if study_level == 'master' and major_of_study == 'all' and cgpa_lower >= 3.5:
        recommendations.append('Biasiswa Endowment UiTM 2022')
        recommendations.append('Biasiswa Suruhanjaya Perkhidmatan Air Negara (SPAN) Scholarship 2022')

    # If no matching rule found, add a default recommendation
    if len(recommendations) == 0:
        recommendations.append('No financial aid recommendation found.')

    return recommendations


# Example usage
study_level = 'foundation'
major_of_study = 'all'
family_income = 'b40'
cgpa_range = '3.50 - 4.00'

recommendations = recommend_financial_aid(study_level, major_of_study, family_income, cgpa_range)
if len(recommendations) > 0:
    print('Recommended financial aid options:')
    for i, recommendation in enumerate(recommendations):
        print(f'{i + 1}. {recommendation}')
else:
    print('No financial aid recommendation found.')
