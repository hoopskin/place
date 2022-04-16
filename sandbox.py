import pandas as pd
import numpy as np

from subprocess import check_output

GZIP_FOLDER = "res/data/gzip-files"
GZIP_FILE_LIST = [GZIP_FOLDER + "/" + f \
            for f in check_output(["ls", GZIP_FOLDER]).decode("utf8").split()]

for curFile in GZIP_FILE_LIST:
    print(curFile)

    print(curFile + "\tBuilding Init DF...")
    place_data = pd.read_csv(curFile, compression='gzip',
                                     header=0, sep=',', quotechar='"')

    #Convert coordinate to loc_x and loc_y
    #place_data.coordinate.str.split(',',expand=True).rename(columns={0:'loc_x', 1:'loc_y'})

    #df = pd.concat([place_data, place_data.coordinate.str.split(',',expand=True)\
    #                            .rename(columns={0:'loc_x', 1:'loc_y'})])

    #place_data['loc_x'] = place_data.coordinate.str.split(",", expand=True)\
    #                            .rename(columns={0:'loc_x', 1:'loc_y'})['loc_x']
    #
    #place_data['loc_y'] = place_data.coordinate.str.split(",", expand=True)\
    #                            .rename(columns={0:'loc_x', 1:'loc_y'})['loc_y']

    print(curFile + "\tExplode Coordinates...")
    place_data[['loc_x', 'loc_y']] = place_data['coordinate'].str.split(',', expand=True)

    print(curFile + "\tCategorize user_id...")
    #TODO: Figure out how to convert user_id to number
    #df['ssn_anon'] = df['ssn'].astype('category').cat.codes
    place_data['user_id_cat'] = place_data['user_id'].astype('category').cat.codes

    print(curFile + "\tDropping un-necessary columns...")
    place_data = place_data.drop(columns=['coordinate', 'user_id'])

    print(place_data.head())
    print(place_data.columns)
    print(place_data.info())
