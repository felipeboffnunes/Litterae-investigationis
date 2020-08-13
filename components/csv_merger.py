import os
import glob
import pandas as pd

def progress():
    if not os.path.exists(rf'.\\results'):
        os.makedirs(rf'.\\results')
    os.chdir(rf'.\\results')
    all_filenames = [i for i in glob.glob('Page_*')]
    return len(all_filenames)

def concatenate_csv(name):
    os.chdir(f'./results')
    all_filenames = [i for i in glob.glob(f'Page_*.csv')]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

    #Delete csv files
    for filename in all_filenames:
        os.remove(filename)

    os.chdir(path)
    combined_csv.to_csv( f'{name}.csv', index=False, encoding='utf-8-sig')