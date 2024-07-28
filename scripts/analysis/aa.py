"""
PLAN:
    0. Configuration
        - dictionary for column mapping
        - variable for column names
    1. Load data
    2. Data cleaning
        - prepare columns
        - remove unnecessary stuff
    3. Melt dataframe
    4. Check for outliers
        - adjust outliers to the mean
    5. Pivot dataframe
        - rename columns from dictionary
    6. Data analysis
    7. Output formatting
    8. Main function
    8. <Optional> Profiling
"""

import pandas as pd
import numpy as np
from tabulate import tabulate

# Profiling
import cProfile
import pstats
import time
from datetime import datetime

logs_folder = '/home/miros/DataOps/developer/white/protocol/logs/pstats/'

data_file = '/home/miros/DataOps/developer/white/protocol/data/raw_data.json'
clean_file = '/home/miros/DataOps/developer/white/protocol/data/clean_data.json'

company_columns = ['Company A', 'Company B', 'Company C', 'Company D', 'Company E']

pivot_columns_dict = {
        "AUM Split_Fixed income" : "AUM_FI",
        "AUM Split_Hedge funds":"AUM_HF",
        "AUM Split_Multi-asset"  :"AUM_MA",
        "AUM Split_Other" : "AUM_Other",
        "AUM Split_Private Debt" :"AUM_PD",
        "AUM Split_Private Equity" : "AUM_PE",
        "AUM Split_Public equities" :"AUM_PubEq",
        "Revenue_Total":"Revenue_Millions_GBP",
        "AUM_Total" :"AUM"
}

aum_pe_ratio = 'AUM_PE_Ratio'
aum_hf_ratio = 'AUM_HF_Ratio'
aum_4y_cagr = 'AUM_4Y_CAGR'
revenue_4y_cagr = 'Revenue_4Y_CAGR'
aum_check = 'AUM_Check'
revenue = 'Revenue_Millions_GBP'
category = 'Category'
subcategory = 'Subcategory'
company = 'Company'
year = 'Year'
metric = 'Metric'
period = 'Period'
aum_pe = 'AUM_PE'
aum_hf = 'AUM_HF'
aum_original = 'AUM'
aum_calculated = 'AUM_Millions_GBP'



# ----------------- LOAD DATA ----------------- #
def load_data(data_file):
    with open(data_file, 'r') as f:
        data = f.read().replace("'", '"')
    with open(clean_file, 'w') as f:
        f.write(data)
    df = pd.read_json(clean_file)
    return df


# ----------------- CLEAN DATA ----------------- #
def clean_data(df):
    # Create a mapping from response columns to the first row values
    first_row = df.iloc[0]
    column_mapping = {f'Response {i+1}': first_row[f'Response {i+1}'] for i in range(5)}
    df.rename(columns=column_mapping, inplace=True)
    df.drop(df.index[0], inplace=True)

    # Add year and period description columns
    df[year] = pd.to_datetime(df['Question level 2'].str.extract('(\d{4})')[0], format='%Y').dt.year
    df[period] = df['Question level 2'].str.extract('([A-Za-z\s]+)')[0].str.strip().fillna('EoY').str.upper()

    # Reset the index and drop unnecessary columns
    df = df[df['Question level 2'] != 'EoY 2024'].reset_index(drop=True)
    df.drop(columns=['Project', 'Question level 2'], inplace=True)
    df.rename(columns={'Question level 1': 'Category', 'Question level 3': 'Subcategory'}, inplace=True)

    # Replace category values
    replacements = {
        'What was your AuM split over the last 5 years?': 'AUM Split',
        'What was your revenue in the last 5 years?': 'Revenue',
        'What was your total AuM in the last 5 years?': 'AUM'
    }
    df[category] = df[category].replace(replacements)
    df[company_columns] = df[company_columns].apply(pd.to_numeric, errors='coerce')
    df[metric] = df[category] + "_" + df[subcategory]
    df.drop(columns=['Category', 'Subcategory', 'Period'], inplace=True)
    return df


#------------------- MELT THE DATAFRAME -------------------#
def melt_dataframe(df):
    df_melted = pd.melt(df, id_vars=['Metric', 'Year'], var_name='Company', value_name='Value')

    return df_melted

#---------------------------- OUTLIERS -------------------#
def find_outliers(df, threshold=1.75):
    def z_score(x):
        return (x - x.mean()) / x.std()

    df = df.dropna(subset=['Value']).reset_index(drop=True)
    df['Z-Score'] = df.groupby(['Company', 'Metric'])['Value'].transform(z_score)
    df['Outlier'] = df['Z-Score'].abs() > threshold
    non_outlier_means = df.groupby(['Company', 'Metric'])['Value'].transform(lambda x: x[~df.loc[x.index, 'Outlier']].mean())
    df['Adjusted_Value'] = np.where(df['Outlier'], non_outlier_means, df['Value'])
    return df

# ------------------------ PIVOT DATAFRAME ------------------ #
def pivot_dataframe(df):
    df_pivot = df.pivot(index=['Company', 'Year'], columns='Metric', values='Adjusted_Value').reset_index()
    df_pivot = df_pivot.rename(columns=pivot_columns_dict)
    return df_pivot


# ------------------------ DATA ANALYSIS ------------------ #
def data_analysis(df):
    df[revenue] = df[revenue] / 1000 # assuming all figures are in million, divide by 1000 to convert to million
    sum_columns = ['AUM_FI', 'AUM_HF', 'AUM_MA', 'AUM_Other', 'AUM_PD', 'AUM_PE', 'AUM_PubEq']
    df[aum_calculated] = sum(df[col] for col in sum_columns)
    df['AUM_Check'] = np.where(df[aum_calculated] == df[aum_original], 'True', 'False')
    df[aum_pe_ratio] = df[aum_pe] / df[aum_calculated]
    df[aum_hf_ratio] = df[aum_hf] / df[aum_calculated]
    df[aum_4y_cagr] = ((df[aum_calculated] / df[aum_calculated].shift(4)) ** (1/4)) - 1
    df[revenue_4y_cagr] = ((df[revenue] / df[revenue].shift(4)) ** (1/4)) - 1
    return df


# ------------------------ OUTPUT ------------------ #
def format_output(df):
    latest_year = df['Year'].max()
    summary_table = df[df['Year'] == latest_year].reset_index(drop=True)
    # format the columns
    summary_table = summary_table[[company, aum_calculated, aum_pe_ratio, aum_hf_ratio, aum_4y_cagr, revenue, revenue_4y_cagr]]
    summary_table[aum_calculated] = summary_table[aum_calculated].map('{:,.0f}'.format)
    summary_table[aum_pe_ratio] = summary_table[aum_pe_ratio].map('{:.2%}'.format)
    summary_table[aum_hf_ratio] = summary_table[aum_hf_ratio].map('{:.2%}'.format)
    summary_table[aum_4y_cagr] = summary_table[aum_4y_cagr].map('{:.2%}'.format)
    summary_table[revenue] = summary_table[revenue].map('{:,.1f}'.format)
    summary_table[revenue_4y_cagr] = summary_table[revenue_4y_cagr].map('{:.2%}'.format)

    print("\nSummary Table:")
    print(tabulate(summary_table, headers='keys', tablefmt='psql'))



def process():
    df = load_data(data_file)
    df = clean_data(df)
    df_melted = melt_dataframe(df)
    df_outliers = find_outliers(df_melted)
    df_pivot = pivot_dataframe(df_outliers)
    df_final = data_analysis(df_pivot)
    format_output(df_final)

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    
    start_time = time.time()
    process()
    end_time = time.time()
    
    profiler.disable()
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    test_name = 'V1.0'

    # Save the profile output with a timestamp
    profile_filename = f'{logs_folder}profile_output_{timestamp}_{test_name}.txt'
    profiler.dump_stats(profile_filename)
    
    print(f"\nExecution Time: {end_time - start_time:.2f} seconds")
    
    with open(profile_filename, 'w') as f:
        ps = pstats.Stats(profiler, stream=f).sort_stats('cumulative')
        ps.print_stats()