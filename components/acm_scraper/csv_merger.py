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
    all_filenames = [i for i in glob.glob(f'./results/Page_*.csv')]
    if len(all_filenames) > 1:
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    else:
        combined_csv = pd.read_csv(all_filenames[0])
    #Delete csv files
    for filename in all_filenames:
        os.remove(filename)

    combined_csv.to_csv( f'./results/{name}.csv', index=False, encoding='utf-8-sig')