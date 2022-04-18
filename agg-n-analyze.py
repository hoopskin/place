import pandas as pd
import numpy as np

import os

GZIP_FOLDER = "res/data/gzip-files"
GZIP_FILE_LIST = [GZIP_FOLDER + "/" + f for f in sorted(os.listdir(GZIP_FOLDER))]

total_pixels_censored = 0
#Moderation (when coord has 4), means there's certain areas we will want
#the whole history, despite the cost. Starting that journey here.
key_pixel_coords_list = []
key_pixel_cnt = 0

for curFile in GZIP_FILE_LIST:
    curFileIdx = GZIP_FILE_LIST.index(curFile)
    preLine = "%i / %i [%.2f%%]" % (curFileIdx, len(GZIP_FILE_LIST)-1, (curFileIdx/(len(GZIP_FILE_LIST)-1))*100)

    print(preLine + "\t"+ curFile)

    print(preLine + "\tBuilding Init DF...")
    df = pd.read_csv(curFile, compression='gzip', header=0, sep=',', quotechar='"')

    print(preLine + "\tBuilding Cnt DF...")
    cnt_df = df.groupby([df.timestamp.str[:13], df.pixel_color, df.coordinate]).count().timestamp

    print(preLine + "\tBuilding Coord DF...")
    coord_df = df.groupby(df.coordinate).count().timestamp

    if len(df.coordinate.str.split(',', expand=True).columns) > 2:
        print("")
        print(preLine + "\t\tModeration Occurred.")
        print(preLine + "\t\tBuilding Mod DF...")
        mod_df = df.coordinate.str.split(',', expand=True)
        #Top Left. Bottom Right.
        mod_df.columns = ['tl_x', 'tl_y', 'br_x', 'br_y']
        cdf = mod_df[mod_df.br_x >= "0"].astype(np.int64)
        cdf['censorship_amt'] = (cdf.br_x - cdf.tl_x) * (cdf.br_y - cdf.tl_y)
        key_pixel_coords_list.append(cdf)
        key_pixel_cnt+=cdf.size

        print("")
        print("--------")
        print(cdf)
        print("--------")
        print("")
        print(preLine + "\t\tCensorship Amt: %i" % (cdf.censorship_amt.sum()))
        total_pixels_censored+=cdf.censorship_amt.sum()
        print("")
        print(preLine + "\t\tTotal Amt: %i" % (total_pixels_censored))
        print("")

    print(preLine + "\tCnt: %.2f%% Smaller" % (100-((cnt_df.size/df.size)*100)))
    print(preLine + "\tCoord: %.2f%% Smaller" % (100-((cnt_df.size/df.size)*100)))

    print(preLine + "Key Pixel Size: %i" % (key_pixel_cnt))

    #Kinda cool way to exit loop on second run without having to declare anything above this
    #try:
    #    os.makedirs("tmp", exist_ok=False)
    #except(FileExistsError):
    #    os.rmdir("tmp")
    #    break
