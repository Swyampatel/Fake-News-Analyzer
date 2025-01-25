import pandas as pd

# Load the datasets
fake = pd.read_csv('Fake.csv')
true = pd.read_csv('True.csv')

# Add a 'label' column to each DataFrame
fake['label'] = 1  # 1 for fake news
true['label'] = 0  # 0 for real news

# Combine the DataFrames
data = pd.concat([fake, true])

# Shuffle the combined DataFrame
data = data.sample(frac=1).reset_index(drop=True)

# Save the combined DataFrame to a new CSV file
data.to_csv('fake_news.csv', index=False)

print("Combined dataset saved as 'fake_news.csv'")
