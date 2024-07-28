# Initial Setup
    python3 -m venv venv
    source venv/bin/activate
    pip install -e .

# Fast Pandas

> DO THIS:
1. Use Vectorized Operations:
```
df['new_column'] = df['existing_column'] * 2  # Vectorized operation
```

2. Leverage Built-in Functions: - apply(), transform(), groupby()

```
df['mean_value'] = df.groupby('group_column')['value_column'].transform('mean')
```

3. Use Efficient Data Types:

```
df['category_column'] = df['category_column'].astype('category')
```

4. Use Single Indexing:

```
df.loc[df['column'] > 0, 'new_column'] = 1
```

5. Use inplace Parameter:

```
df.dropna(inplace=True)
```

6. Batch Processing


> DONT DO THIS:
1. Avoid Loops:
```
for index, row in df.iterrows():
    df.at[index, 'new_column'] = row['existing_column'] * 2
```
2. Avoid Applying Functions Row-wise:

! Don't use apply() with axis=1 for row-wise operations if a vectorized solution is available.

```
df['new_column'] = df.apply(lambda row: row['col1'] + row['col2'], axis=1)
```

3. Avoid Using apply() for Simple Operations:
```
df['new_column'] = df['existing_column'].apply(lambda x: x * 2)
```

Don't use apply() for operations that can be done with vectorized operations.

4. Avoid Unnecessary Copies:

```
# Don't do this
df_copy = df.copy()
df_copy['new_column'] = df_copy['existing_column'] * 2
```


5. Avoid Using loc and iloc Inside Loops: 
```
for i in range(len(df)):
    df.loc[i, 'new_column'] = df.loc[i, 'existing_column'] * 2
```


6. Avoid Using pd.concat in a Loop:
```
for i in range(100):
    df = pd.concat([df, new_row_df])
```

