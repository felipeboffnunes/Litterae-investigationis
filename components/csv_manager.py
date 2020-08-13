import pandas as pd
import glob

def get_search_df(name):
    filename = glob.glob(f'./results/{name}.csv')[0]
    search_df = pd.read_csv(filename)
    return search_df