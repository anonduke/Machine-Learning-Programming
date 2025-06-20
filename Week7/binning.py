# Step 1: Import necessary libraries
import numpy as np
import pandas as pd

# Step 2: Create a sample dataset (simulating house prices)
np.random.seed(42)  # For reproducibility
prices = np.random.normal(300, 100, 1000)  # Mean=300k, SD=100k, 1000 samples
data = pd.DataFrame({'Price': prices})

# Step 3: Define bin edges for fixed-width binning
# Choose boundaries: Low (<200k), Medium (200k-400k), High (>400k)
bin_edges = [0, 200, 400, np.inf]  # Infinite upper bound for high prices
bin_labels = ['Low', 'Medium', 'High']

# Step 4: Apply binning using pd.cut
data['Price_Category'] = pd.cut(data['Price'], bins=bin_edges, labels=bin_labels, include_lowest=True)

# Step 5: Analyze the results
print("Original Data Sample:\n", data['Price'].head())
print("\nBinned Data Sample:\n", data['Price_Category'].head())
print("\nBin Counts:\n", data['Price_Category'].value_counts())

# Optional: Visualize the distribution
import matplotlib.pyplot as plt
data['Price_Category'].value_counts().plot(kind='bar')
plt.title('Distribution of Price Categories')
plt.xlabel('Price Category')
plt.ylabel('Count')
plt.show()