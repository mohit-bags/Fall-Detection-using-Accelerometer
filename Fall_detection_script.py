import numpy as np 
import pandas as pd
import glob

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
    
    for i in range(0,df.index[-1]-win_size,overlap_win): 
        avg_mag,min_mag,max_mag,diff_max_min=extract_mean_max_min(df,i,win_size)

        if(min_mag<=threshold_tending_0):#fall detected
            print(i,"Free Fall detected")
            #case where impact and free fall in same window
            if(diff_max_min>=impact_activity):#min max diff
                print(i,"Impact also deteced-SAME WINDOW")
                temp_size=10 #window size for calculating average
                no_of_iterations = 15 #considering 2s [10*10==100 -> 25Hz in 1s]
                sum_diff=0
                for j in range(0,no_of_iterations+1):
                    sum_diff+=extract_mean_max_min(df,i+win_size+ (j*temp_size),temp_size)[3]
                avg_sum_diff = sum_diff/no_of_iterations
                if(avg_sum_diff<=inactivity):
                    print(i,"Inactivness, FALL CONFIRMED")
                else:
                    print(i,"Inactivness not detected, but value:",avg_sum_diff)   
            #Searching for Impact in next window
            elif(extract_mean_max_min(df,i+overlap_win,overlap_win)[3]>=impact_activity):#min max diff
                print(i,"Impact also deteced-NEXT WINDOW")
                temp_size=5 #window size for calculating average
                no_of_iterations = 30 #considering 2s [10*10==100 -> 25Hz in 1s]
                sum_diff=0
                for j in range(0,no_of_iterations+1):
                    sum_diff+=extract_mean_max_min(df,i+win_size+ (j*temp_size),temp_size)[3]
                avg_sum_diff = sum_diff/no_of_iterations
                if(avg_sum_diff<=inactivity):
                    print(i,"Inactivness, FALL CONFIRMED")
                else:
                    print(i,"Inactivness not detected, but value:",avg_sum_diff)    

folder_path = '/Users/mohitbagaria/Fall-Detection-using-Accelerometer/test_datas'
file_list = glob.glob(folder_path + "/*.csv")
for i in range(0,len(file_list)):
    print("------",file_list[i],"-------")
    df = pd.read_csv(file_list[i],header=None)
    df=df.loc[:,1:3]
    df.columns=['X','Y','Z']
    df['Magnitude']=np.sqrt(df['X']*df['X']+df['Y']*df['Y']+df['Z']*df['Z'])
    print(detect_free_fall(df,120,2000,200))

