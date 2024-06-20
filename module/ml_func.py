import streamlit as st
import numpy as np
import pandas as pd
import os
import pickle
import base64
#import sklearn

PAGE_CONFIG = {"page_title"             : "Recomendator Shows and Movies Model - Streamlit",
                # "page_icon"             : ":film:",   
                 "layout"                : "wide"}
                # "initial_sidebar_state" : "expanded"}


abreviaciones_a_nombres = {
    'US': 'United States of America',
    'GB': 'United Kingdom of Great Britain and Northern Ireland',
    'IN': 'India',
    'CA': 'Canada',
    'FR': 'France',
    'JP': 'Japan',
    'DE': 'Germany',
    'ES': 'Spain',
    'KR': 'South Korea',
    'IT': 'Italy',
    'CN': 'China',
    'AU': 'Australia',
    'MX': 'Mexico',
    'BR': 'Brazil',
    'NG': 'Nigeria',
    'AR': 'Argentina',
    'BE': 'Belgium',
    'ZA': 'South Africa',
    'HK': 'Hong Kong',
    'PH': 'Philippines',
    'TR': 'Turkey',
    'PL': 'Poland',
    'EG': 'Egypt',
    'SE': 'Sweden',
    'CO': 'Colombia',
    'TW': 'Taiwan',
    'IE': 'Ireland',
    'ID': 'Indonesia',
    'DK': 'Denmark',
    'NL': 'Netherlands',
    'NO': 'Norway',
    'TH': 'Thailand',
    'NZ': 'New Zealand',
    'RU': 'Russia',
    'IL': 'Israel',
    'CH': 'Switzerland',
    'CZ': 'Czech Republic',
    'CL': 'Chile',
    'LB': 'Lebanon',
    'SG': 'Singapore',
    'AT': 'Austria',
    'AE': 'United Arab Emirates',
    'MY': 'Malaysia',
    'PS': 'Estado de Palestina',
    'RO': 'Romania',
    'HU': 'Hungary',
    'IS': 'Iceland',
    'PT': 'Portugal',
    'FI': 'Finland',
    'PR': 'Puerto Rico',
    'SA': 'Saudi Arabia',
    'SU': 'Russia',
    'GR': 'Greece',
    'LU': 'Luxembourg',
    'IR': 'Iran',
    'SK': 'Slovakia',
    'UY': 'Uruguay',
    'QA': 'Qatar',
    'UA': 'Ukraine',
    'PE': 'Peru',
    'VN': 'Vietnam',
    'KE': 'Kenya',
    'KW': 'Kuwait',
    'BG': 'Bulgaria',
    'MA': 'Morocco',
    'JO': 'Jordan',
    'AF': 'Afghanistan',
    'VE': 'Venezuela',
    'DO': 'Dominican Republic',
    'YU': 'Republic of Serbia',
    'PK': 'Pakistan',
    'SN': 'Senegal',
    'CU': 'Cuba',
    'TN': 'Tunisia',
    'BD': 'Bangladesh',
    'GE': 'Georgia',
    'TZ': 'Tanzania',
    'RS': 'Republic of Serbia',
    'PA': 'Panama',
    'SY': 'Syria',
    'EE': 'Estonia',
    'XC': 'Montenegro',
    'KH': 'Cambodia',
    'BO': 'Bolivia',
    'AL': 'Albania',
    'EC': 'Ecuador',
    'DZ': 'Algeria',
    'MC': 'Monaco',
    'GH': 'Ghana',
    'IO': 'British Indian Ocean Territory',
    'GT': 'Guatemala',
    'MN': 'Mongolia',
    'CM': 'Cameroon',
    'IQ': 'Iraq',
    'NP': 'Nepal',
    'CR': 'Costa Rica',
    'RW': 'Rwanda',
    'HN': 'Honduras',
    'ET': 'Ethiopia',
    'TT': 'Trinidad and Tobago',
    'XK': 'Kosovo',
    'LV': 'Latvia',
    'CD': 'Democratic Republic of the Congo',
    'PY': 'Paraguay',
    'BS': 'The Bahamas',
    'BY': 'Belarus',
    'SB': 'Solomon Islands',
    'KZ': 'Kazakhstan',
    'SZ': 'Eswatini',
    'BA': 'Bosnia and Herzegovina',
    'LT': 'Lithuania',
    'CI': 'Ivory Coast',
    'MK': 'Macedonia',
    'CY': 'Cyprus',
    'LI': 'Liechtenstein',
    'SI': 'Slovenia',
    'MT': 'Malta',
    'MW': 'Malawi',
    'ZW': 'Zimbabwe',
    'AO': 'Angola',
    'LK': 'Sri Lanka',
    'VU': 'Vanuatu',
    'NI': 'Nicaragua',
    'SV': 'El Salvador',
    'TC': 'Islas Turcas y Caicos',
    'VA': 'Vatican City',
    'KN': 'Saint Kitts and Nevis',
    'BF': 'Burkina Faso',
    'GL': 'Greenland',
    'MU': 'Mauritius',
    'FO': 'Faroe Islands',
    'AZ': 'Azerbaijan',
    'NA': 'Namibia',
    'GD': 'Grenada',
    'CF': 'Central African Republic',
    'UZ': 'Uzbekistan',
    'AQ': 'Antarctica',
    'BM': 'Bermuda',
    'JM': 'Jamaica',
    'SO': 'Somalia',
    'FM': 'Micronesia',
    'FJ': 'Fiji',
    'PF': 'French Polynesia',
    'NC': 'New Caledonia',
    'HR': 'Croatia',
    'AN': 'Netherlands Antilles',
    'OM': 'Oman',
    'UG': 'Uganda',
    'KI': 'Kiribati',
    'BW': 'Botswana',
    'BT': 'Bhutan',
    'KG': 'Kyrgyzstan',
    'ZM': 'Zambia'}

#@st.cache_data
def read_data():

    df = pd.read_csv("source/df.csv")

    df.columns = ['id', 'title', 'type', 'description', 'release_year',
       'age_certification', 'runtime', 'genres', 'production_countries',
       'seasons', 'imdb_id', 'imdb_score', 'imdb_votes', 'tmdb_popularity',
       'tmdb_score', 'actors', 'actor_ids', 'directors', 'director_ids',
       'platform', 'titleyear']
    
    df = df.drop(['id', 'description','imdb_id','tmdb_popularity','tmdb_score','actor_ids','director_ids', 'titleyear'], axis=1)

    df['genres'] = df['genres'].str.replace(r'[','').str.replace(r"'",'').str.replace(r']','')

    df['genres'] = df['genres'].fillna('desconocido')


    df['production_countries'] = df['production_countries'].str.replace(r"[", '').str.replace(r"'", '').str.replace(r"]", '')
    df['production_countries'] = df['production_countries'].replace('', np.nan)

    df.loc[df['title'] == 'once bitten', 'runtime'] = 94
    df.loc[df['title'] == 'superfish', 'runtime'] = 52
    df.loc[df['title'] == 'scenes from a marriage', 'runtime'] = 169
    df.loc[df['title'] == 'chhote ustaad-precaution is better than cure', 'runtime'] = 123


    return df

