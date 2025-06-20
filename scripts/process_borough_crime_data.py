#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 15:24:43 2025

@author: hishamdemmisse
"""

import pandas as pd
import numpy as np

# File path to the raw data
DATA_PATH = '/Users/hishamdemmisse/Desktop/Github/london-liveability-score/data/raw/MPS Borough Level Crime (most recent 24 months).csv'

# Load data
data = pd.read_csv(DATA_PATH)
data_copy = data.copy() #The Df we wish to adapt

# Add a 'Total Count' column summing all crime counts across months (from 3rd column onwards)
data_copy['Total Count'] = data.iloc[:, 3:].sum(axis=1)

# Dictionary to group crimes into broader categories
crime_group_map = {
    'HOMICIDE': 'Violent Crime',
    'VIOLENCE WITH INJURY': 'Violent Crime',
    'VIOLENCE WITHOUT INJURY': 'Violent Crime',
    'VIOLENT DISORDER': 'Violent Crime',
    'ROBBERY OF PERSONAL PROPERTY': 'Violent Crime',
    'ROBBERY OF BUSINESS PROPERTY': 'Violent Crime',
    'POSSESSION OF WEAPONS': 'Violent Crime',
    'RAPE': 'Sexual Crime',
    'OTHER SEXUAL OFFENCES': 'Sexual Crime',
    'BURGLARY - RESIDENTIAL': 'Residential Burglary',
    'BURGLARY IN A DWELLING': 'Residential Burglary',
    'BURGLARY BUSINESS AND COMMUNITY': 'Non-Residential Burglary and Theft',
    'BURGLARY NON-DWELLING': 'Non-Residential Burglary and Theft',
    'BICYCLE THEFT': 'Non-Residential Burglary and Theft',
    'OTHER THEFT': 'Non-Residential Burglary and Theft',
    'SHOPLIFTING': 'Non-Residential Burglary and Theft',
    'THEFT FROM THE PERSON': 'Non-Residential Burglary and Theft',
    'AGGRAVATED VEHICLE TAKING': 'Non-Residential Burglary and Theft',
    'INTERFERING WITH A MOTOR VEHICLE': 'Non-Residential Burglary and Theft',
    'THEFT FROM A VEHICLE': 'Non-Residential Burglary and Theft',
    'THEFT OR UNAUTH TAKING OF A MOTOR VEH': 'Non-Residential Burglary and Theft',
    'POSSESSION OF DRUGS': 'Drug Offences',
    'TRAFFICKING OF DRUGS': 'Drug Offences',
    'ARSON': 'Property Damage and Arson',
    'CRIMINAL DAMAGE': 'Property Damage and Arson',
    'MISC CRIMES AGAINST SOCIETY': 'Public Order and Society Offences',
    'OTHER OFFENCES PUBLIC ORDER': 'Public Order and Society Offences',
    'PUBLIC FEAR ALARM OR DISTRESS': 'Public Order and Society Offences',
    'RACE OR RELIGIOUS AGG PUBLIC FEAR': 'Public Order and Society Offences',
    'FRAUD AND FORGERY': 'Fraud and Forgery'
}

# Remove existing 'CrimeGroup' column if present to avoid conflicts
if 'CrimeGroup' in data_copy.columns:
    data_copy.drop(columns=['CrimeGroup'], inplace=True)

# Map 'MinorText' column to crime groups
data_copy['CrimeGroup'] = data_copy['MinorText'].map(crime_group_map)

# Reorder columns so 'CrimeGroup' is the second column
cols = list(data_copy.columns)
cols.insert(3, cols.pop(cols.index('CrimeGroup')))
data_copy = data_copy[cols]

# Drop columns MajorText and MinorText, since our CrimeGroup is sufficient a label class
# This orders our data to show the first column as Borough and second as the Crime label
data_copy.drop(columns = ['MajorText','MinorText'],inplace = True)
#print(data_copy.head())

# Columns containing frequency counts (all columns from index 2 onwards)
freq_cols = data_copy.columns[2:]
#print("Frequency columns:", list(freq_cols))  # Looks fine

# Use group_by attribute and the sum function to add up frequencies of the same crime

grouped_df = data_copy.groupby(['BoroughName', 'CrimeGroup'], as_index=False)[freq_cols].sum()

#print(grouped_df.iloc[:,1:].head())   # Fantastic, moving on.


def f(score):  # Non-linearity to handle the severity gap between petty crime and serious crime. 
    return score ** 8

# Making a function to recieve and process score from user inputs

def get_score(prompt):
    while True:
        value_str = input(f"{prompt} (1-10): ")
        try: # Used to handle the int(value_str) error with a print(error) rather than a crash out of the loop
            value = int(value_str)
            if 1 <= value <= 10:
                return round(f(value)) # Rounded to avoid issues when interacting with integer datatypes later
                                     # The function choice is an area of exploration
            else:
                print("Input must be an integer between 1 and 10. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

print("\nPlease provide a severity score (1-10) for each crime category:\n")

# Intilise a new dictionary to track user scores for each crime

crime_scores = {}

# Cycle through categories prompts in alphabetical order
for category in sorted(set(crime_group_map.values())): 
    crime_scores[category] = get_score(category)

# Initilise our weighted_df

weighted_df = grouped_df.copy()
freq_cols = weighted_df.columns[2:]


for category, weight in crime_scores.items():
    mask = category == weighted_df['CrimeGroup']
    weighted_df.loc[mask,freq_cols] *= weight


#print(grouped_df)
#print(weighted_df)

#Awesome looking good so far! Next we will add up all the points for each borough

final_df = weighted_df.copy()
borough_scores = final_df.groupby(['BoroughName'], as_index=False)[freq_cols].sum()

#print(borough_scores) # Nice

scaled_scores = borough_scores.loc[:,['BoroughName','Total Count']]

min_score = scaled_scores['Total Count'].min()
max_score = scaled_scores['Total Count'].max()

scaled_scores['Scaled Crime Score (0–100)'] = round((
    (borough_scores['Total Count'] - min_score) / (max_score - min_score)
) * 100)


#print(scaled_scores) # Looks fine


import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects


def clean_names(df, column):
    df[column] = df[column].str.lower().str.strip()
    return df


def prepare_geodata(gdf_path, borough_names=None):
    gdf = gpd.read_file(gdf_path)
    gdf = clean_names(gdf, 'LAD13NM')
    if borough_names is not None and len(borough_names) > 0:
        borough_names = [b.lower().strip() for b in borough_names]
        gdf = gdf[gdf['LAD13NM'].isin(borough_names)].copy()
    return gdf


def merge_scores(gdf, scores_df):
    scores_df = clean_names(scores_df, 'BoroughName')
    merged = gdf.set_index('LAD13NM').join(scores_df.set_index('BoroughName'), how='left')
    missing = merged[merged['Scaled Crime Score (0–100)'].isna()]
    if not missing.empty:
        print("⚠️ Warning: Unmatched boroughs with no score:", missing.index.tolist())
    return merged


def plot_crime_heatmap(gdf, score_col='Scaled Crime Score (0–100)', show_labels=True):
    fig, ax = plt.subplots(figsize=(12, 10))
    gdf.plot(
        column=score_col,
        cmap='Reds',
        linewidth=0.8,
        edgecolor='0.8',
        legend=True,
        ax=ax,
        missing_kwds={"color": "lightgrey", "edgecolor": "red", "hatch": "///", "label": "No data"}
    )
    if show_labels:
        for idx, row in gdf.iterrows():
            if row['geometry'].geom_type in ['Polygon', 'MultiPolygon']:
                centroid = row['geometry'].centroid
                ax.text(
                    centroid.x, centroid.y, idx.title(),
                    fontsize=7, ha='center', va='center', color='black',
                    path_effects=[path_effects.withStroke(linewidth=2, foreground='white')]
                )
    ax.set_title('London Boroughs - Crime Risk Visualisation', fontsize=16)
    ax.axis('off')
    plt.tight_layout()
    plt.show()


# --- Usage Example ---

GEO_PATH = '/Users/hishamdemmisse/Desktop/Github/london-liveability-score/data/raw/topo_lad.json'

# Make sure borough_list is a list, not a pandas Index or Series
borough_list = list(scaled_scores['BoroughName'].unique())

gdf = prepare_geodata(GEO_PATH, borough_names=borough_list)
merged = merge_scores(gdf, scaled_scores)
plot_crime_heatmap(merged, show_labels=True)
