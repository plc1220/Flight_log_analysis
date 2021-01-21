import pandas as pd
import numpy as np
from statistics import mean

# Read csv
df = pd.read_csv("C:/Users/liche/Desktop/Log Analysis/00000039.csv", index_col=0,low_memory=False)

# Extract out the RC9(pump pwm) value
RCout=df.loc["RCOU"]
RC9 = RCout.iloc[:,[0,9]].astype('int32').values.tolist()
print(len(RC9))

# Extract out GPS1 value
GPS=df.loc["GPS"].iloc[:,[0,6,7]]
GPS.columns = ['time','lat','lon']
GPS_list = GPS.astype({'lat':'float64','lon':'float64'}).values.tolist()
print(len(GPS_list))

# Extract final position data
POS=df.loc["POS"].iloc[:,[0,1,2]]
POS.columns = ['time','lat','lon']
POS_list = POS.astype({'lat':'float64','lon':'float64'}).values.tolist()
print(len(POS_list))

time_list = []
for i in range(len(RC9)):
    if (RC9[i][1]==1900 and RC9[i-1][1]<=1100) or (RC9[i][1]==1900 and RC9[i+1][1]==1100):
        time_range = POS_list[i][0]
        time_list.append(time_range)

lat_list = []
lon_list = []
POS_lat_list = []
POS_lon_list = []

for j in range(int((len(time_list))/2)):
    GPS_Trigger_x = [item[1] for item in GPS_list if time_list[2*j]<=item[0]<=time_list[(2*j)+1]]
    GPS_Trigger_y = [item[2] for item in GPS_list if time_list[2*j]<=item[0]<=time_list[(2*j)+1]]
    POS_Trigger_x = [item[1] for item in POS_list if time_list[2*j]<=item[0]<=time_list[(2*j)+1]]
    POS_Trigger_y = [item[2] for item in POS_list if time_list[2*j]<=item[0]<=time_list[(2*j)+1]]
    lat_list.append(GPS_Trigger_x)
    lon_list.append(GPS_Trigger_y)
    POS_lat_list.append(POS_Trigger_x)
    POS_lon_list.append(POS_Trigger_y)

avg_lat_list = [mean(item) for item in lat_list]
avg_lon_list = [mean(item) for item in lon_list]
avg_POSx_list = [mean(item) for item in POS_lat_list]
avg_POSy_list = [mean(item) for item in POS_lon_list]

avg_gps_points = list(zip(avg_lat_list,avg_lon_list))
avg_POS_points = list(zip(avg_POSx_list,avg_POSy_list))
final_df = pd.DataFrame(avg_gps_points)
final_df.columns = ['lat','lon']
final_df.to_csv("C:/Users/liche/Desktop/Log Analysis/trigger.csv")

final_df2 = pd.DataFrame(avg_POS_points)
final_df2.columns = ['lat','lon']
final_df2.to_csv("C:/Users/liche/Desktop/Log Analysis/POS.csv")
