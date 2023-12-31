##################################
# 前処理
##################################

import pandas as pd

# 最頻値で欠損値を埋める
def fillna_with_mode(df, columns):
    for col in columns:
        mode_value = df[col].mode().iloc[0]
        df[col].fillna(mode_value, inplace=True)

# yearカラムの修正
def fix_year_column(df):
    df['year'] = df['year'].apply(lambda x: x if x <= 2023 else x - 1000)
    return df

# odometerカラムの修正
def fix_odometer_column(df):
    df['odometer'] = df['odometer'].apply(lambda x: -1 if x < 0 else x)
    return df

# stateカラムの欠損値を埋める
def fill_missing_state(df, area_mapping):
    missing_state_rows = df[df['state'].isnull()]
    for index, row in missing_state_rows.iterrows():
        region = row['region']
        state = df[df['region'] == region]['state'].iloc[0]
        if pd.isnull(state):
            state = area_mapping[region]
        df.at[index, 'state'] = state

# manufacturerカラムの整形
def normalize_manufacturer_column(df):
    # スペースの除去
    df['manufacturer'] = df['manufacturer'].str.replace(' ', '')
    # 小文字に統一
    df['manufacturer'] = df['manufacturer'].str.lower()          
    # 半角に統一
    df['manufacturer'] = df['manufacturer'].str.normalize('NFKC')  
    # 文字コードの統一
    df['manufacturer'] = df['manufacturer'].str.encode('ascii', 'ignore').str.decode('utf-8') 

def preprocess_manufacturer(input_df):
    output_df = input_df.copy()
    output_df['manufacturer'] = output_df['manufacturer'].str.lower().str.normalize("NFKC")
    output_df.loc[output_df['manufacturer'].str.startswith('ni'), 'manufacturer'] = 'nissan'
    output_df.loc[output_df['manufacturer'].str.startswith('toyo'), 'manufacturer'] = 'toyota'
    output_df.loc[output_df['manufacturer'].str.startswith('lex'), 'manufacturer'] = 'lexus'
    output_df.loc[output_df['manufacturer'].str.endswith('cura'), 'manufacturer'] = 'acura'
    output_df.loc[output_df['manufacturer'].str.endswith('ler'), 'manufacturer'] = 'chrysler'
    output_df.loc[output_df['manufacturer'].str.endswith('ru'), 'manufacturer'] = 'subaru'
    output_df.loc[output_df['manufacturer'].str.endswith('turn'), 'manufacturer'] = 'saturn'
    output_df.loc[output_df['manufacturer'].str.endswith('wagen'), 'manufacturer'] = 'volkswagen'
    return output_df

# sizeカラムの整形
def normalize_size_column(df):
    # ハイフンの統一
    df['size'] = df['size'].str.replace('ー', '-').str.replace('−', '-')
    return df
    
# conditionカラムのエンコード
def encode_condition_column(df):
    condition_ranking = {
        'new': 5,
        'like new': 4,
        'excellent': 3,
        'good': 2,
        'fair': 1,
        'salvage': 0
    }
    df['condition'] = df['condition'].map(condition_ranking)
    return df