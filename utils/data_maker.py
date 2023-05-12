import pandas as pd
import json
import os

def final_file_generator():
    df = pd.DataFrame(columns=['endTime','artistName','trackName','msPlayed'])

    data_path = 'data/all_history'
    out_data_path = 'data/final_file'

    for filename in os.listdir(data_path):
        if filename == ".gitkeep":
            continue
        filepath = os.path.join(data_path, filename)
        # checking if it is a file
        f = open(filepath)
        file = json.load(f)

        dfItem = pd.DataFrame.from_records(file)
        dfItem['endTime'] = pd.to_datetime(dfItem['endTime'])
        df = pd.concat([df, dfItem], ignore_index=True)    

    df = df.drop_duplicates()
    df = df.groupby(["artistName", "trackName"]).count()
    df = df.rename(columns={"msPlayed": "cnt"})
    df = df.reset_index()

    df.to_json(out_data_path+'/data.json', orient = 'split', compression = 'infer')  
    print(df)
