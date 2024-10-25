import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Title of the app
st.title("Display DataFrames from Population, Huggingface Models, and Common Crawl")

# 1. Load Population Data from local file (replace with your own file)
@st.cache_data
def load_population_data():
    df = pd.read_csv("./data/dataverse_files/Table_of_Languages.tab", sep='\t')
    df = df.rename(columns={'ISO_639': 'iso639', 'L1_Users': 'l1_users', 'All_Users': 'all_users'})
    df = df[df['Is_Written'] == "T"].reset_index(drop=True)
    total_users = df['all_users'].sum(skipna=True)
    df['all_users_percentage'] = (df['all_users'] / total_users) * 100
    return df

# 2. Scrape Huggingface models data
@st.cache_data
def load_huggingface_data():
    url = "https://huggingface.co/languages"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table and extract the data
    table = soup.find('table')
    headers = [header.text.strip() for header in table.find_all('th')]
    
    rows = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        rows.append([cell.text.strip() for cell in cells])
    
    # Create a DataFrame from the scraped data
    df = pd.DataFrame(rows, columns=headers)
    
    # Clean up the 'Models' column
    df['Models'] = df['Models'].str.replace(',', '').astype(int)
    total_models = df['Models'].sum(skipna=True)
    df['model_percentages'] = (df['Models'] / total_models) * 100
    return df

# 3. Load third CSV (Common Crawl Language Data)
@st.cache_data
def load_common_crawl_data():
    url = "https://commoncrawl.github.io/cc-crawl-statistics/plots/languages.csv"
    df = pd.read_csv(url)
    # Get the data for the most recent crawl (assuming the most recent one is at the bottom)
    most_recent_crawl = df[df['crawl'] == df['crawl'].iloc[-1]]
    # Convert pages column to percentages of the total pages
    total_pages = most_recent_crawl['pages'].replace(',', '', regex=True).astype(float).sum()
    most_recent_crawl['pages_percentage'] = most_recent_crawl['pages'].replace(',', '', regex=True).astype(float) / total_pages * 100
    most_recent_crawl = most_recent_crawl.rename(columns={'primary_language': 'iso639'})
    return most_recent_crawl.reset_index(drop=True)

# Display Population Data
population_data = load_population_data()
st.write("### Population Data from CSV")
st.dataframe(population_data)

# Display Huggingface models data
huggingface_data = load_huggingface_data()
st.write("### Huggingface Models Data")
st.dataframe(huggingface_data)

# Display Common Crawl Language Data
common_crawl_data = load_common_crawl_data()
st.write("### Common Crawl Languages CSV")
st.dataframe(common_crawl_data)

st.write("### Merged datasets")
merged_df = pd.merge(population_data, common_crawl_data, how='left', on='iso639')
merged_df = merged_df[['iso639', 'Uninverted_Name', 'all_users', 'all_users_percentage', 'pages_percentage']]
merged_df['pages_percentage'] = merged_df['pages_percentage'].fillna(0)
merged_df['representation_ratio'] = merged_df['pages_percentage'] / merged_df['all_users_percentage']
merged_df = merged_df.sort_values(by=['representation_ratio', 'all_users'], ascending=[True, True])

st.write(merged_df)


# Perform a left join to find all rows in df_crawl with or without a match in df_population
anti_join_df = pd.merge(common_crawl_data, population_data, how='left', on='iso639', indicator=True)
# Filter rows where the merge was unsuccessful, i.e., the iso639 code was not found in df_population
# '_merge' column indicates the source of the row (left_only, right_only, or both)
missing_languages = anti_join_df[anti_join_df['_merge'] == 'left_only']
# Drop the '_merge' column since it is no longer needed
missing_languages = missing_languages.drop(columns=['_merge'])

st.write("### Languages in Common Crawl but Absent in Population Data")
st.dataframe(missing_languages)