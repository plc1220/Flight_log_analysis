import pandas as pd
import os
import glob

dirname = "C:/Users/liche/Desktop/Log Analysis/Aerotree-Gem2/11.11"

extension = 'csv'

# See number of files
file_list = os.listdir(dirname)

os.chdir(dirname)

result = glob.glob('*.{}'.format(extension))

for filename in result:
    df = pd.read_csv((dirname+'/'+filename), index_col=0, low_memory=False)
    POS = df.loc["POS"].iloc[:,[1,2,3,4]]
    S_height = df.loc["CTUN"].iloc[:,[9]]
    POS.columns = ['lat','lon','ASL','Relative alt']
    POS.reset_index(drop=True, inplace=True)
    S_height.columns = ['Sensor_height']
    S_height.reset_index(drop=True, inplace=True)
    final_df = pd.concat([POS, S_height], axis=1, join='inner')    
    new_filename = filename[:-4] + '_POS.csv'
    final_df.to_csv((dirname+'/'+new_filename))