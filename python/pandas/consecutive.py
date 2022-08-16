# %%
import numpy as np
import pandas as pd
# %%
# Create data from 1 to 3, where it is highly likely that we have some repeating numbers
np.random.seed(0)
data = np.random.randint(0,3,100) # Also works with repeating strings
df = pd.DataFrame(data, columns=['data'])
# %%
# Number the consequtive numbers:
df['consecutive_cumsum'] = df['data'].ne(df['data'].shift(1)).cumsum() # Count up where the values are not repeating
df['consecutive'] = df.groupby(df['consecutive_cumsum']).cumcount()+1 # Where consecutive it will count which item place it has in the sequence

# Consecutive size:
consecutive_size = df.groupby(df['consecutive_cumsum']).size() # How many items in each consecutive 'group'
df['consecutive_size'] = df['consecutive_cumsum'].apply(lambda x: consecutive_size[x]) # Fill it back into the df
# %%
# Remove all consecutive values but keep the first one
df = df.drop_duplicates(subset=['consecutive_cumsum'], keep='first')
