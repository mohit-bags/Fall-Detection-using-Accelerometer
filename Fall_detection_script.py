import numpy as np 
import pandas as pd
import glob
import sys

def extract_mean_max_min(data,start_time,win_size=50): #25Hz sampling rate
    avg=0
    min_mag=1e9
    max_mag=-1e9
    diff_max_min=0
    for i in range(start_time,start_time+win_size):
        if(i>=len(data)):
            break
        mag=(data.loc[i,'Magnitude'])
        avg+=mag
        min_mag=min(min_mag,mag)
        max_mag=max(max_mag,mag)
        diff_max_min=max(diff_max_min,max_mag-min_mag)
    return round(avg/win_size,2),min_mag,max_mag,diff_max_min
    

def detect_free_fall(df,threshold_tending_0,impact_activity,inactivity,win_size=50,overlap_win=25):
    faller=0
    for i in range(0,df.index[-1]-win_size,overlap_win): 
        if(faller>0):
            faller-=1
            continue
        avg_mag,min_mag,max_mag,diff_max_min=extract_mean_max_min(df,i,win_size)

        if(min_mag<=threshold_tending_0):#fall detected
            print(i,"Free Fall detected")
            #Searching for impact
            if(diff_max_min>=impact_activity):#min max diff
                print(i,"Impact detected , val:",diff_max_min)
                temp_size=5 #window size for calculating average
                no_of_iterations = 30 #considering 2s [10*10==100 -> 25Hz in 1s]
                sum_diff=0
                for j in range(0,no_of_iterations+1):
                    sum_diff+=extract_mean_max_min(df,i+win_size+ (j*temp_size),temp_size)[3]
                avg_sum_diff = sum_diff/no_of_iterations
                if(avg_sum_diff<=inactivity):
                    print(i,"Inactivness, FALL CONFIRMED")
                    faller=2
                else:
                    print(i,"Inactivness not detected, but value:",avg_sum_diff)   


#Give parent folder path too data
folder_path = '/Users/mohitbagaria/Fall-Detection-using-Accelerometer/test_datas'
#Ensure data os in csv format
file_list = glob.glob(folder_path + "/*.csv")
sys.stdout=open("/Users/mohitbagaria/Fall-Detection-using-Accelerometer/test_outputs.txt","w")

for i in range(0,len(file_list)):
    print("------",file_list[i],"-------")
    df = pd.read_csv(file_list[i],header=None)
    df=df.loc[:,1:3]
    df.columns=['X','Y','Z']
    df['Magnitude']=np.sqrt(df['X']*df['X']+df['Y']*df['Y']+df['Z']*df['Z'])
    print(detect_free_fall(df,500,2000,300))

sys.stdout.close()
