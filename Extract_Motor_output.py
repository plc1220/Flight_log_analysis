import pandas as pd
import numpy as np
import os
import glob
import math
from matplotlib import pyplot as plt

# Directory

dirname = "C:/Users/liche/Desktop/Log Analysis/UPM"

extension = 'csv'

# See number of files
file_list = os.listdir(dirname)

os.chdir(dirname)

result = glob.glob('*.{}'.format(extension))

#print(result)

# Read csv
for filename in result:
    df = pd.read_csv((dirname+'/'+filename), index_col=0, low_memory=False)
    #print(df)

    # Extract out GPS1 value
    GPS=df.loc["GPS"].iloc[:,[0,9]]
    GPS.columns = ['time','speed']
    GPS_list = GPS.astype({'speed':'float64'}).values.tolist()
    speed_column = GPS['speed']
    max_speed = float(speed_column.max())
    print(max_speed)
    #filtered_GPS=GPS[GPS['speed'>(max_speed*0.85)]]
    #print(filtered_GPS)
    max_speed_round = int(math.ceil(max_speed))
    
    # Extract out RCout value
    RCou = df.loc["RCOU"].iloc[:,[0,1,2,3,4,5,6]]
    RCou.columns = ['time','M1','M2','M3','M4','M5','M6']
    RCou_list = RCou.astype('int32').values.tolist()

    # Extract time that fit speed criteria & get the gps speed list for plotting
    time_list = []
    GPS_S_list = []
    for i in range(len(GPS_list)):
        if (GPS_list[i][1]>(max_speed*0.9)):
            time = int(GPS_list[i][0])
            time_list.append(time)
            GPS_S_list.append(GPS_list[i])

    # Create speed df
    S_df = pd.DataFrame(GPS_S_list,columns = ['time','GPS'])
    S_df.set_index('time',inplace=True)

    # Map time with RCout output
    final_list = []
    for j in range(len(time_list)-1):
        include_list = [k for k in RCou_list if time_list[j]<int(k[0])<time_list[j+1]]
        final_list.extend(include_list)

    final_df = pd.DataFrame(final_list)
    final_df.columns = ['time','M1','M2','M3','M4','M5','M6']
    
    final_df.set_index('time',inplace=True)
    
    print(final_df.shape)

    final_filename = dirname+'/'+filename[:-4]

    final_df.to_csv(final_filename+'_%i.csv'%(max_speed_round))

    #plot
    fig, ax = plt.subplots()
    final_df.plot(ax=ax)
    S_df.plot(ax=ax,secondary_y = True, style ='g--')
    plt.show()
    fig.savefig(final_filename+'.png')