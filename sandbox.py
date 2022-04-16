import pandas as pd
import numpy as np

from subprocess import check_output

GZIP_FOLDER = "res/data/gzip-files"
GZIP_FILE_LIST = [GZIP_FOLDER + "/" + f \
            for f in check_output(["ls", GZIP_FOLDER]).decode("utf8").split()]

#list_of_dfs = [pd.read_csv(filename) for filename in GZIP_FILE_LIST]
#for dataframe, filename in zip(list_of_dfs, GZIP_FILE_LIST)
#    dataframe['filename'] = filename
#combined_df = pd.concat(list_of_dfs, ignore_index=True)

list_of_dfs = []
total_size = 0

for curFile in GZIP_FILE_LIST:
    curFileIdx = GZIP_FILE_LIST.index(curFile)
    preLine = "%i / %i [%.2f%%]" % (curFileIdx, len(GZIP_FILE_LIST), (curFileIdx/len(GZIP_FILE_LIST))*100)
    print(preLine + "\t"+ curFile)

    #Don't parse dates. It adds so much time and the format can be
    #Easily manipulated as a string
    print(preLine + "\tBuilding Init DF...")
    list_of_dfs.append(pd.read_csv(curFile, compression='gzip', header=0, sep=',', quotechar='"'))

    print(preLine + "\tExplode Coordinates...")
    #DropNA to remove 2nd file's extra columns (one row has data there? Wonder what it is.)
    list_of_dfs[-1][['loc_x', 'loc_y']] = list_of_dfs[-1]['coordinate'] \
                                            .str.split(',', expand=True) \
                                            .dropna(axis='columns')

    print(preLine + "\tCategorize user_id...")
    #TODO: Figure out how to convert user_id to number
    #df['ssn_anon'] = df['ssn'].astype('category').cat.codes
    list_of_dfs[-1]['user_id_cat'] = list_of_dfs[-1]['user_id'] \
                                            .astype('category').cat.codes

    print(preLine + "\tDropping un-necessary columns...")
    list_of_dfs[-1] = list_of_dfs[-1].drop(columns=['coordinate', 'user_id'])

    total_size+=len(list_of_dfs[-1])

    print(preLine + "\tRows: " + f'{len(list_of_dfs[-1]):,}')
    print(preLine + "\tTotal Size: " + f'{total_size:,}')
    #print(place_data.head())
    #print(place_data.columns)
    #print(place_data.info())

combined_df = pd.concat(list_of_dfs, ignore_index=True)
combined_df.to_pickle(path="res/data/dataframe.pkl")
