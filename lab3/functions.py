import pandas as pd
from urllib import request
from os import listdir, makedirs, walk, path
from shutil import rmtree
from datetime import datetime
from re import search


def check_folder(folder_path):
    if listdir(folder_path):
        rmtree(folder_path)
        makedirs(folder_path)


def download_data(province_id):
    url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={province_id}&year1=1981&year2=2024&type=Mean'

    try:
        vhi = request.urlopen(url).read().decode('utf-8')
        now = datetime.now()
        formatted_time = now.strftime('%d%m%Y%H%M%S')
        with open(f'data/vhi_id_{province_id}_{formatted_time}.csv', 'w') as f:
            f.write(vhi)

    except Exception as e:
        print(f'An error occurred while loading file with province id {province_id}')


def create_df(file_path, norm_province_id):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    temp_df = pd.read_csv(file_path, header=1, names=headers)
    temp_df = temp_df.drop(temp_df.loc[temp_df['VHI'] == -1].index)
    temp_df.loc[0, 'Year'] = temp_df.loc[0, 'Year'][9:]
    temp_df = temp_df.drop(columns='empty').drop(temp_df.index[-1])
    temp_df['area'] = norm_province_id
    temp_df['Year'] = temp_df['Year'].astype(int)
    temp_df = temp_df.drop(['SMN', 'SMT'], axis=1)
    temp_df['Week'] = temp_df['Week'].astype(int)

    return temp_df


def get_paths(dir_path):
    file_paths = []
    for root, dirs, files in walk(dir_path):
        for i in files:
            file_paths.append(path.join(root, i))

    return file_paths


def find_province_id(file_path):
    with open(file_path, 'r') as f:
        return int(search(r'Province\s*=\s*(\d+)', f.readline()).group(1))


replacements = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 12: 9,
              13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 25, 21: 17, 22: 18,
              23: 6, 24: 1, 25: 2, 26: 7, 27: 5}
