import pandas as pd

# Define file paths
file_paths = {
    'before': {
        'blood diamond scandal': 'sentimentResults/output_diamond_before.csv',
        'lemonade album release': 'sentimentResults/output_lemonade_before.csv',
        'renaissance album release': 'sentimentResults/output_renaissance_before.csv',
        'superbowl performance': 'sentimentResults/output_superbowl_before.csv'
    },
    'after': {
        'blood diamond scandal': 'sentimentResults/output_diamond_after.csv',
        'lemonade album release': 'sentimentResults/output_lemonade_after.csv',
        'renaissance album release': 'sentimentResults/output_renaissance_after.csv',
        'superbowl performance': 'sentimentResults/output_superbowl_after.csv'
    }
}

# Calculate percentage of positive and negative sentiment for each file
sentiment_data = {}

for event, paths in file_paths.items():
    for name, path in paths.items():
        df = pd.read_csv(path, header=None, names=['text', 'sentiment'])
        pos_count = (df['sentiment'].str[-3:] == 'Pos').sum()
        neg_count = (df['sentiment'].str[-3:] == 'Neg').sum()
        total_count = len(df)
        pos_pct = pos_count / total_count
        neg_pct = neg_count / total_count
        sentiment_data[f'{name}_{event}'] = {'pos_pct': pos_pct, 'neg_pct': neg_pct}

# Do correlation analysis
correlations = {}

for name1, data1 in sentiment_data.items():
    for name2, data2 in sentiment_data.items():
        if name1 != name2 and name1.split('_')[0] == name2.split('_')[0]:
            event_name = name1.split('_')[0].capitalize()
            before_after1 = name1.split('_')[1].capitalize()
            before_after2 = name2.split('_')[1].capitalize()
            corr_key = f'{before_after1} {event_name} - {before_after2} {event_name}'
            pos_corr_val = round((data1['pos_pct'] - data2['pos_pct']) * 100, 2)
            neg_corr_val = round((data1['neg_pct'] - data2['neg_pct']) * 100, 2)
            correlations[corr_key] = {'Pos Correlation': f'{pos_corr_val}%', 'Neg Correlation': f'{neg_corr_val}%'}

# Print correlation data
print("The correlations here (in the positive scale) are:")
for i, (key, val) in enumerate(correlations.items()):
    if i >= 4:
        break
    pos_corr_val = val['Pos Correlation']
    print("     " + key + ': ' + pos_corr_val)