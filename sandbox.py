import pandas as pd
import numpy as np

from subprocess import check_output

GZIP_FOLDER = "res/data/gzip-files"
GZIP_FILE_LIST = [GZIP_FOLDER + "/" + f \
            for f in check_output(["ls", GZIP_FOLDER]).decode("utf8").split()]



list_of_dfs = []
list_of_ids = []
total_size = 0

for curFile in GZIP_FILE_LIST:
    curFileIdx = GZIP_FILE_LIST.index(curFile)
    preLine = "%i / %i [%.2f%%]" % (curFileIdx, len(GZIP_FILE_LIST)-1, (curFileIdx/(len(GZIP_FILE_LIST)-1))*100)
    print(preLine + "\t"+ curFile)

    #Don't parse dates. It adds so much time and the format can be
    #Easily manipulated as a string
    print(preLine + "\tCapturing User ID Hashes...")
    list_of_ids.append(pd.read_csv(curFile, compression='gzip', usecols=['user_id']))#.squeeze("columns"))
    #print(preLine + "\tBuilding Init DF...")
    #list_of_dfs.append(pd.read_csv(curFile, compression='gzip', header=0, sep=',', quotechar='"'))

    #print(preLine + "\tExplode Coordinates...")
    #DropNA to remove 2nd file's extra columns (one row has data there? Wonder what it is.)
    ###############
    #From The Site#
    ###############

    #Inside the dataset there are instances of moderators using a rectangle drawing tool
    #to handle inappropriate content. These rows differ in the coordinate tuple
    #which contain four values instead of two–“x1,y1,x2,y2” corresponding to the
    #upper left x1, y1 coordinate and the lower right x2, y2 coordinate of the moderation rect.
    #These events apply the specified color to all tiles within those two points, inclusive.

    #TODO: Need to find these and call them out
    #list_of_dfs[-1][['loc_x', 'loc_y']] = list_of_dfs[-1]['coordinate'] \
    #                                        .str.split(',', expand=True) \
    #                                        .dropna(axis='columns')

    #print(preLine + "\tCategorize user_id...")
    ##TODO: Figure out how to convert user_id to number
    ##df['ssn_anon'] = df['ssn'].astype('category').cat.codes
    #list_of_dfs[-1]['user_id_cat'] = list_of_dfs[-1]['user_id'] \
    #                                        .astype('category').cat.codes
    #
    #print(preLine + "\tDropping un-necessary columns...")
    #list_of_dfs[-1] = list_of_dfs[-1].drop(columns=['coordinate', 'user_id'])

    total_size+=len(list_of_ids[-1])

    print(preLine + "\tRows: " + f'{len(list_of_ids[-1]):,}')
    print(preLine + "\tTotal Size: " + f'{total_size:,}')
    #print(pd.concat(list_of_ids, ignore_index=True).user_id.astype('category').cat.codes.value_counts())
    #print(place_data.head())
    #print(place_data.columns)
    #print(place_data.info())

print("Concat-ing all Hashes...")
combined_df = pd.concat(list_of_ids, ignore_index=True)

#print("Pickling and Compressing User ID Hashes...")
#combined_df.to_pickle(path="res/data/user-id-hashes.pkl.gzip", compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1})

print("Done!")
