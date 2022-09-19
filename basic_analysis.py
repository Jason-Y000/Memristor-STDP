import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import scipy.signal as sig              # For the Savitzky-Golay filter
import numpy as np
import math
import pandas as pd
import os
import re
import csv

file_path = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Keithley Data/Jason - 24mtorr Vertical Crossbar/Block 1/Oct 30/Pulse_Before_4_10_11.xls"
file_path2 = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Keithley Data/Jason - 24mtorr Vertical Crossbar/Block 1/Oct 30/Pulse_After_4_10_11.xls"

dir_path = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/14 mTorr Raw Data/Block 2 Location (2, 3)/Temp"   # Block directory
img_dir = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/14 mTorr Raw Data/Block 2 Location (2, 3)"
# new_file = open("/Users/jasonyuan/Desktop/Test_vals.dat","w+")
# new_file2 = open("/Users/jasonyuan/Desktop/Test_Vals2.dat","w+")

def analysis(f_path):
    # analysis1() function, but you can specify the file_path
    data = pd.read_excel(f_path,sheet_name="Data")
    sub_data = data.filter(items=["TimeOutput","IMeasCh1","VMeasCh1"]).to_numpy()
    nrows,ncols = sub_data.shape
    t_min = 35.0*10**(-5)
    t_max = 35.4*10**(-5)
    # t_min = 8.0*10**(-5)
    # t_max = 10*10**(-5)

    current_avg = 0
    voltage_avg = 0
    n_points = 0

    for r in range(0,nrows):
        if (sub_data[r,0] > t_min) and (sub_data[r,0] < t_max):
            current_avg += sub_data[r,1]
            voltage_avg += sub_data[r,2]
            n_points += 1
            # if (sub_data[r,1] >= -2*10**(-9)) and (sub_data[r,1] <= 2*10**(-9)):
            #     current_avg += sub_data[r,1]       # Trying something new, going to |current| since mag of current should still reflect the resistance
            #     voltage_avg += sub_data[r,2]
            #     n_points += 1
            # if sub_data[r,1] < 0:
            #     continue
            # else:
            #     current_avg += sub_data[r,1]
            #     voltage_avg += sub_data[r,2]
            #     n_points += 1

    current_avg = current_avg/n_points
    voltage_avg = voltage_avg/n_points

    R_avg = abs(voltage_avg/current_avg)

    # print(n_points)
    print("-----------------------------------------------------------------------------------")
    print("Current: {}".format(current_avg))
    print("Voltage: {}".format(voltage_avg))
    print("Resistance: {}".format(R_avg))
    print("Points: {}".format(n_points))
    print("-----------------------------------------------------------------------------------")

    return R_avg

def analysis1():
    # Function for determining resistance before and after when a separate SegArb was called for the probing pulse

    data = pd.read_excel(file_path,sheet_name="Data")
    sub_data = data.filter(items=["TimeOutput","IMeasCh1","VMeasCh1"]).to_numpy()
    nrows,ncols = sub_data.shape
    t_min = 0.3*10**(-5)
    t_max = 1.07*10**(-5)

    current_avg_before = 0
    voltage_avg_before = 0
    n_points = 0

    for r in range(0,nrows):
        if (sub_data[r,0] > t_min) and (sub_data[r,0] < t_max):
            current_avg_before += sub_data[r,1]
            voltage_avg_before += sub_data[r,2]
            n_points += 1

    current_avg_before = current_avg_before/n_points
    voltage_avg_before = voltage_avg_before/n_points

    data2 = pd.read_excel(file_path2,sheet_name="Data")
    sub_data2 = data2.filter(items=["TimeOutput","IMeasCh1","VMeasCh1"]).to_numpy()
    nrows,ncols = sub_data2.shape
    t_min = 0.3*10**(-5)
    t_max = 1.07*10**(-5)

    current_avg_after = 0
    voltage_avg_after = 0
    n_points = 0
    for r in range(0,nrows):
        # new_file2.write(str(sub_data[r,0])+"\n")
        if (sub_data2[r,0] > t_min) and (sub_data2[r,0] < t_max):
            # new_file.write(str(sub_data[r,0])+"\n")
            current_avg_after += sub_data2[r,1]
            voltage_avg_after += sub_data2[r,2]
            n_points += 1

    current_avg_after = current_avg_after/n_points
    voltage_avg_after = voltage_avg_after/n_points

    R_after = voltage_avg_after/current_avg_after
    R_before = voltage_avg_before/current_avg_before

    print(n_points)
    print("Current Before: {}".format(current_avg_before),"Current After: {}".format(current_avg_after))
    print("Resistance Before: {}".format(R_before),"Resistance After: {}".format(R_after))

    return True

def analysis2():
    # Function to determine resistance when the probing pulses were a part of the spike waveform pulses
    file_path3 = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Keithley Data/Jason - 24mtorr Vertical Crossbar/Block 1/Nov 13/STDP_100us_5_2_52.xls"

    data = pd.read_excel(file_path3,sheet_name="Data")
    sub_data = data.filter(items=["TimeOutput","IMeasCh1","VMeasCh1"]).to_numpy()
    nrows,ncols = sub_data.shape

    t_min_before = 0.40*10**(-5)
    t_max_before = 0.60*10**(-5)
    t_min_after = 12.60*10**(-5)
    t_max_after = 12.75*10**(-5)

    current_avg_before = 0
    voltage_avg_before = 0
    current_avg_after = 0
    voltage_avg_after = 0
    n_points_before = 0
    n_points_after = 0

    for r in range(0,nrows):
        if (sub_data[r,0] > t_min_before) and (sub_data[r,0] < t_max_before):
            # new_file2.write(str(sub_data[r,2])+"\n")
            current_avg_before += sub_data[r,1]
            voltage_avg_before += sub_data[r,2]
            n_points_before += 1
        elif (sub_data[r,0] > t_min_after) and (sub_data[r,0] < t_max_after):
            # new_file.write(str(sub_data[r,2])+"\n")
            current_avg_after += sub_data[r,1]
            voltage_avg_after += sub_data[r,2]
            n_points_after += 1

    current_avg_before = current_avg_before/n_points_before
    voltage_avg_before = voltage_avg_before/n_points_before
    current_avg_after = current_avg_after/n_points_after
    voltage_avg_after = voltage_avg_after/n_points_after

    R_after = abs(voltage_avg_after/current_avg_after)
    R_before = abs(voltage_avg_before/current_avg_before)

    base = os.path.basename(file_path3)
    delta_T = base.split("_")[1]
    p = "[-\d]+|\d+"
    delta_T = int(re.findall(p,delta_T)[0])

    if not os.path.isfile('/Users/jasonyuan/Desktop/Kherani Lab/Memristor/STDP/24mmTorr/Block 1/(5,2)_One-Sided'+'/'+'Data_vals.csv'):
        new_file = open('/Users/jasonyuan/Desktop/Kherani Lab/Memristor/STDP/24mmTorr/Block 1/(5,2)_One-Sided'+'/'+"Data_vals.csv","w+")
        writer = csv.writer(new_file)
        header = ["delta_T","R_before","R_after"]
        writer.writerow(header)
        writer.writerow([delta_T,R_before,R_after])
    else:
        new_file = open('/Users/jasonyuan/Desktop/Kherani Lab/Memristor/STDP/24mmTorr/Block 1/(5,2)_One-Sided'+'/'+"Data_vals.csv","a")
        writer = csv.writer(new_file)
        writer.writerow([delta_T,R_before,R_after])
    new_file.close()

    print("-------------------------------------------------------------------")
    print("Voltage Before: {}".format(voltage_avg_before),"Voltage After: {}".format(voltage_avg_after))
    print("Current Before: {}".format(current_avg_before),"Current After: {}".format(current_avg_after))
    print("Resistance Before: {}".format(R_before),"Resistance After: {}".format(R_after))
    print("delta_T: ",delta_T)
    print("Before: ",n_points_before)
    print("After: ",n_points_after)

    return True

def analysis3(input_file=None,t_min=None,t_max=None,filter=False):
    # Function for determining resistance of the combined spike waveform train
    if input_file == None:
        file_to_use = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Keithley Data/Jason - 24mtorr Vertical Crossbar/Block 1/Dec 7/Pulse_Before_5_7_Combined.xls"
    else:
        file_to_use = input_file

    data = pd.read_excel(file_to_use,sheet_name="Data")
    sub_data = data.filter(items=["TimeOutput","IMeasCh1","VMeasCh1"]).to_numpy()   # Change CH1 according to needle descriptions
    nrows,ncols = sub_data.shape

    if (t_min == None) or (t_max == None):
        t_min = 0.2*10**(-5)
        t_max = 0.8*10**(-5)

    current_avg = 0
    voltage_avg = 0
    cum_R = 0
    n_points = 0

    if not filter:
        for r in range(0,nrows):
            if (sub_data[r,0] > t_min) and (sub_data[r,0] < t_max):
                current_avg += sub_data[r,1]
                voltage_avg += sub_data[r,2]
                cum_R += abs(voltage_avg/current_avg)
                n_points += 1

        current_avg = abs(current_avg/n_points)
        voltage_avg = abs(voltage_avg/n_points)

        # R_avg = voltage_avg/current_avg
        R_avg = cum_R/n_points

    else:
        current_array = []
        voltage_array = []
        for r in range(0,nrows):
            if (sub_data[r,0] > t_min) and (sub_data[r,0] < t_max):
                current_array.append(sub_data[r,1])
                voltage_array.append(sub_data[r,2])
                n_points += 1

        filtered_current = sig.savgol_filter(x=current_array,window_length=13,polyorder=1,deriv=0)
        filtered_voltage = sig.savgol_filter(x=voltage_array,window_length=13,polyorder=1,deriv=0)

        for n in range(len(filtered_current)):
            cum_R += abs(filtered_voltage[n]/filtered_current[n])

        current_avg = abs(sum(filtered_current)/n_points)
        voltage_avg = abs(sum(filtered_voltage)/n_points)

        # R_avg = voltage_avg/current_avg
        R_avg = cum_R/n_points

    print(n_points)
    print("Current: {}".format(current_avg))
    print("Voltage: {}".format(voltage_avg))
    print("Resistance: {}".format(R_avg))
    print("----------------------------------------------------------------")

    return current_avg,voltage_avg,R_avg

def synaptic_weight_combined_analysis(t_file,input_file,save_dir,reverse=True,filter=False):
    # Analysis function for the combined spike waveform, manually have to go
    # through and determine the time intervals

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    data_times = pd.read_excel(t_file) # Columns will be t_min,t_max
    rows,cols = data_times.shape

    new_data = {}
    delta_T = [0]
    R_before = []
    R_after = []
    delta_w = []
    R_min = math.inf

    for i in range(5,65,5):
        if not reverse:
            delta_T.append(i)
            delta_T.append(-i)
        else:
            delta_T.append(-i)
            delta_T.append(i)
    for i in range(70,110,10):
        if not reverse:
            delta_T.append(i)
            delta_T.append(-i)
        else:
            delta_T.append(-i)
            delta_T.append(i)
    new_data["delta_T"] = delta_T

    for idx in range(0,rows):          # Modify for separate pulse_before
        t_min = data_times.iloc[idx]["t_min"]
        t_max = data_times.iloc[idx]["t_max"]

        if (t_min == -1) and (t_max == -1):
            I,V,R = analysis3()
        else:
            I,V,R = analysis3(input_file,t_min,t_max,filter)

        R_min = min(R,R_min)

        if (idx == 0):
            R_before.append(R)
        elif (idx == rows-1):
            R_after.append(R)
        else:
            R_before.append(R)
            R_after.append(R)
    new_data["R_before"] = R_before
    new_data["R_after"] = R_after
    new_data["R_min"] = R_min

    for n in range(0,len(R_before)):
        w_instance = synaptic_weight_calc(R_before[n],R_after[n],R_min)
        delta_w.append(w_instance)
    new_data["delta_w"] = delta_w

    filename = input_file.split("/")[len(input_file.split("/"))-1].split(".")[0]
    df_newdata = pd.DataFrame(new_data)
    df_newdata = df_newdata.sort_values(by="delta_T",axis=0)
    df_newdata.to_csv(save_dir+"/"+"Processed_{}.csv".format(filename))

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1,label="1")
    ax.scatter(delta_T,delta_w,color="cornflowerblue",label="Synaptic Weight")
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel('ΔT (μs)',color='k')
    ax.set_ylabel('∆w%', color='cornflowerblue')
    ax.tick_params(axis='x', which='both', labelcolor='k')
    ax.tick_params(axis='y', which='both', labelcolor='cornflowerblue')

    ax.grid(linestyle="--",color="silver")
    ax.set_title(filename)
    fig.tight_layout()

    fig.savefig(save_dir+"/"+'{}_∆w_plot.png'.format(filename),bbox_inches='tight',format='png',dpi=600)
    plt.close(fig)

    print("Finished processing {}".format(filename))
    return True

def synaptic_weight_calc(R_before,R_after,R_min):
    delta_w = (1/R_after-1/R_before)/(1/R_min)*100
    return delta_w

def synaptic_weight_analysis_basic(coord):

    dict_R = {}
    R_min = math.inf
    points = []
    all_points = []
    file_count = 0

    for sub_dir in os.listdir(dir_path):
        sub_dir_path = os.path.join(dir_path,sub_dir)
        if not os.path.isdir(sub_dir_path):
            continue
        for filename in os.listdir(sub_dir_path):
            if (("_{}_{}_".format(coord[0],coord[1]) in filename) and ("before" in filename.lower())) or (("_{}_{}_".format(coord[0],coord[1]) in filename) and ("after" in filename.lower())):
                print("Probe Pulse: ",filename)
                file_count += 1

                f_path = os.path.join(sub_dir_path,filename)

                split_name = filename.split("_")

                if (split_name[len(split_name)-1].split(".")[0]) not in dict_R:
                    dict_R[split_name[len(split_name)-1].split(".")[0]] = []

                R_avg = analysis(f_path)
                R_min = min(R_min,R_avg)

                if ("before" in filename.lower()):
                    dict_R[split_name[len(split_name)-1].split(".")[0]] = dict_R[split_name[len(split_name)-1].split(".")[0]] + [("B",R_avg)]
                elif ("after" in filename.lower()):
                    dict_R[split_name[len(split_name)-1].split(".")[0]] = dict_R[split_name[len(split_name)-1].split(".")[0]] + [("A",R_avg)]

            elif (("STDP" in filename) and ("_{}_{}_".format(coord[0],coord[1]) in filename)):
                print("STDP: ",filename)
                file_count += 1

                split_name = filename.split("_")

                if (split_name[len(split_name)-1].split(".")[0]) not in dict_R:
                    dict_R[split_name[len(split_name)-1].split(".")[0]] = []

                delta_T = filename.split("_")[1]
                p = "[-\d]+|\d+"
                delta_T = int(re.findall(p,delta_T)[0])

                dict_R[split_name[len(split_name)-1].split(".")[0]] = dict_R[split_name[len(split_name)-1].split(".")[0]] + [("T",delta_T)]

    for key,val in dict_R.items():
        for element in val:
            if (element[0] == "B"):
                R_before = element[1]
            elif (element[0] == "A"):
                R_after = element[1]
            else:
                T_sep = element[1]
        delta_w = synaptic_weight_calc(R_before,R_after,R_min)
        all_points.append([T_sep,delta_w])

    all_points = sorted(all_points,key=lambda x:x[0])
    n_points = 0
    for time,weight in all_points:
        if (n_points == 0):
            temp_t = time
            temp_weight = weight
            n_points = 1
        else:
            if (time != temp_t):
                points.append([temp_t,temp_weight/n_points])
                temp_t = time
                temp_weight = weight
                n_points = 1
            else:
                temp_weight += weight
                n_points += 1

    points.append([temp_t,temp_weight/n_points])
    points = np.asarray(points,dtype=np.double)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1,label='1')
    ax.scatter(points[:,0],points[:,1],color="cornflowerblue",label="Synaptic Weight")
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel('ΔT (μs)',color='k')
    ax.set_ylabel('∆w%', color='cornflowerblue')
    ax.tick_params(axis='x', which='both', labelcolor='k')
    ax.tick_params(axis='y', which='both', labelcolor='cornflowerblue')

    ax.grid(linestyle="--",color="silver")
    ax.set_title("Synaptic Weight change of device {} as a function\n of pulse time separation".format(coord))
    fig.tight_layout()

    # plt.show()
    if not os.path.isdir(os.path.join(img_dir,str(coord))):
        os.makedirs(os.path.join(img_dir,str(coord)))

    fig.savefig(os.path.join(img_dir,str(coord))+'/'+'{}_∆w_plot.png'.format(coord),bbox_inches='tight',format='png',dpi=600)
    plt.close(fig)

    # Write data to csv file
    new_file = open(os.path.join(img_dir,str(coord))+'/'+"Data_vals.csv","w+")
    new_file2 = open(os.path.join(img_dir,str(coord))+'/'+"R_vals.csv","w+")
    writer = csv.writer(new_file)
    writer2 = csv.writer(new_file2)
    header = ["delta_T", "delta_w"]
    header2 = ["delta_T","R_before","R_after"]
    writer.writerow(header)
    writer2.writerow(header2)

    for p in points:
        writer.writerow(p)
    for key,val in dict_R.items():
        for element in val:
            if (element[0] == "B"):
                R_before = element[1]
            elif (element[0] == "A"):
                R_after = element[1]
            else:
                T_sep = element[1]
        writer2.writerow([T_sep,R_before,R_after])

    new_file.close()
    new_file2.close()

    print("Files processed: ",file_count)
    print(R_min)

    return True

if __name__ == "__main__":
    # analysis("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Keithley Data/8mTorr/Block 3/Dec 16/STDP_Combined_1_10.xls")
    # analysis1()
    # analysis2()
    # analysis3()

    t_file = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Time_Range_General_2.xlsx"
    save_dir = "/Users/jasonyuan/Desktop"
    # save_base = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Block 1/Cleaned Plots"
    input_base = ""
    input_file = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/24mTorr/Block 2/STDP_Combined_3_10.xls"

    if input_base == "":
        synaptic_weight_combined_analysis(t_file,input_file,save_dir,reverse=True,filter=True)
    else:
        for name in os.listdir(input_base):
            if os.path.isdir(os.path.join(input_base,name)):
                continue
            if name == ".DS_Store":
                continue
            input_file = os.path.join(input_base,name)
            save_dir = os.path.join(save_base,name.split(".")[0])
            synaptic_weight_combined_analysis(t_file,input_file,save_dir,reverse=True,filter=True)

    # coord = (2,3)
    # synaptic_weight_analysis_basic(coord)

    # ------------------------------------------------------------------------------------------------------------------------- #
    # save_dir = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Average of best devices 2"
    # df = pd.read_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Average of best devices 2/Average.csv")
    #
    # delta_T = df["delta_T"].to_numpy()
    # delta_w = df["delta_w"].to_numpy()
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1,label='1')
    # ax.scatter(delta_T,delta_w,color="cornflowerblue",label="Synaptic Weight")
    # ax.xaxis.set_minor_locator(AutoMinorLocator())
    # ax.yaxis.set_minor_locator(AutoMinorLocator())
    # ax.set_xlabel('ΔT (μs)',color='k')
    # ax.set_ylabel('∆w%', color='cornflowerblue')
    # ax.tick_params(axis='x', which='both', labelcolor='k')
    # ax.tick_params(axis='y', which='both', labelcolor='cornflowerblue')
    #
    # ax.grid(linestyle="--",color="silver")
    # ax.set_title("Averaged ∆w% of 8 devices at 14mTorr pressure")
    # fig.tight_layout()
    #
    # # plt.show()
    #
    # fig.savefig(save_dir+'/'+'Avg_∆w_plot.png',bbox_inches='tight',format='png',dpi=600)
    # plt.close(fig)
    # ------------------------------------------------------------------------------------------------------------------------- #
    # This part is for averaging repeated trials -- do tomorrow morning
    # df1 = pd.read_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Block 1/Cleaned Plots/STDP_Combined_2_1/Processed_STDP_Combined_2_1.csv")
    # df2 = pd.read_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Block 1/Cleaned Plots/STDP_Combined_4_5/Processed_STDP_Combined_4_5.csv")
    # df3 = pd.read_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Block 1/Cleaned Plots/STDP_Combined_5_4/Processed_STDP_Combined_5_4.csv")
    # df4 = pd.read_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Block 1/Cleaned Plots/STDP_Combined_1_6/Processed_STDP_Combined_1_6.csv")
    # df5 = pd.read_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Block 1/Cleaned Plots/STDP_Combined_3_8/Processed_STDP_Combined_3_8.csv")
    # df6 = pd.read_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Block 2/Cleaned Plots/STDP_Combined_4_5/Processed_STDP_Combined_4_5.csv")
    # df7 = pd.read_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Block 4/Cleaned Plots/STDP_Combined_4_4/Processed_STDP_Combined_4_4.csv")
    # df8 = pd.read_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Block 4/Cleaned Plots/STDP_Combined_5_5/Processed_STDP_Combined_5_5.csv")
    # data_avg = {}
    #
    # delta_w_1 = df1["delta_w"]
    # delta_w_2 = df2["delta_w"]
    # delta_w_3 = df3["delta_w"]
    # delta_w_4 = df4["delta_w"]
    # delta_w_5 = df5["delta_w"]
    # delta_w_6 = df6["delta_w"]
    # delta_w_7 = df7["delta_w"]
    # delta_w_8 = df8["delta_w"]
    #
    # delta_w_avg = []
    # delta_T = df1["delta_T"]
    #
    # # delta_T = [0,-5,5,-10,10,-15,15,-20,20,-25,25,-30,30,-35,35,-40,40,-45,45,-50,50,-55,55,-60,60,-70,70,-80,80,-90,90,-100,100]
    # # total_times = len(delta_T)
    # # counter = 0
    # # to_avg = 0
    # # val = 0
    # #
    # # while (counter < total_times):
    # #     for element in [df1,df2,df3,df4,df5,df6,df7,df8]:
    # #         if (delta_T[counter] in element["delta_T"].values):
    # #             idx = element[element["delta_T"] == delta_T[counter]].index[0]
    # #             val += element["delta_w"][idx]
    # #             to_avg += 1
    # #     val = val/to_avg
    # #     delta_w_avg.append(val)
    # #
    # #     counter += 1
    # #     to_avg = 0
    # #     val = 0
    #
    # for n in range(0,len(delta_w_1)):
    #     val = (delta_w_1[n] + delta_w_2[n]+ delta_w_3[n] + delta_w_4[n] + delta_w_5[n] + delta_w_6[n] + delta_w_7[n] + delta_w_8[n])/8
    #     delta_w_avg.append(val)
    #
    # data_avg["delta_T"] = delta_T
    # data_avg["delta_w"] = delta_w_avg
    #
    # df_avg = pd.DataFrame(data_avg)
    # df_avg.to_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Average of best devices 2/Average.csv")
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1,label="1")
    # ax.scatter(delta_T,delta_w_avg,color="cornflowerblue",label="Synaptic Weight")
    # ax.xaxis.set_minor_locator(AutoMinorLocator())
    # ax.yaxis.set_minor_locator(AutoMinorLocator())
    # ax.set_xlabel('ΔT (μs)',color='k')
    # ax.set_ylabel('∆w%', color='cornflowerblue')
    # ax.tick_params(axis='x', which='both', labelcolor='k')
    # ax.tick_params(axis='y', which='both', labelcolor='cornflowerblue')
    #
    # ax.grid(linestyle="--",color="silver")
    # ax.set_title("Averaged ∆w% of 8 devices at 14mTorr pressure")
    # fig.tight_layout()
    #
    # fig.savefig("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Cleaned Data/14mTorr/Average of best devices 2/Avg_∆w_plot.png",bbox_inches='tight',format='png',dpi=600)
    # plt.close(fig)

    # ------------------------------------------------------------------------------------------------------------------------- #
    # This part can be ignored. Was used for special case like situations

    # data1 = pd.read_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/STDP/24mmTorr/Block 1/(5, 2)/R_vals1.csv")
    # data2 = pd.read_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/STDP/24mmTorr/Block 1/(5, 2)/R_vals2.csv")
    # # data1 = pd.read_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/STDP/24mmTorr/Block 1/(5,2)_One-Sided/Data_vals.csv")
    # # data1 = data1.sort_values(by=['delta_T'])
    # #
    # combined = data1.append(data2)
    # combined = combined.sort_values(by=['delta_T'])
    # combined.to_csv("/Users/jasonyuan/Desktop/Kherani Lab/Memristor/STDP/24mmTorr/Block 1/(5, 2)/R_vals3.csv",index=False)
    #
    # points = combined.to_numpy()
    #
    # new = open('/Users/jasonyuan/Desktop/Kherani Lab/Memristor/STDP/24mmTorr/Block 1/(5, 2)'+'/'+'Data_vals3.csv','w+')
    # writer = csv.writer(new)
    # writer.writerow(["delta_T","delta_w"])
    #
    # # new = open('/Users/jasonyuan/Desktop/Kherani Lab/Memristor/STDP/24mmTorr/Block 1/(5,2)_One-Sided'+'/'+'Processed.csv','w+')
    # # writer = csv.writer(new)
    # # writer.writerow(["delta_T","delta_w"])
    #
    # # points = data1.to_numpy()
    #
    # R_min = np.amin(points[:,1:])
    # processed = []
    # for i in range(0,points.shape[0]):
    #     delta_w = synaptic_weight_calc(points[i,1],points[i,2],R_min)
    #     processed.append([points[i,0],delta_w])
    #     writer.writerow([points[i,0],delta_w])
    # new.close()
    #
    # processed = np.array(processed)
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1,label='1')
    # ax.scatter(processed[:,0],processed[:,1],color="cornflowerblue",label="Synaptic Weight")
    # ax.xaxis.set_minor_locator(AutoMinorLocator())
    # ax.yaxis.set_minor_locator(AutoMinorLocator())
    # ax.set_xlabel('ΔT (us)',color='k')
    # ax.set_ylabel('∆w%', color='cornflowerblue')
    # ax.tick_params(axis='x', which='both', labelcolor='k')
    # ax.tick_params(axis='y', which='both', labelcolor='cornflowerblue')
    #
    # ax.grid(linestyle="--",color="silver")
    # ax.set_title("Synaptic Weight change of device {} as a function\n of pulse time separation".format(coord))
    # fig.tight_layout()
    #
    # # fig.savefig('/Users/jasonyuan/Desktop/Kherani Lab/Memristor/STDP/24mmTorr/Block 1/(5,2)_One-Sided'+'/'+'(5,2)_single_∆w_plot.png',bbox_inches='tight',format='png',dpi=600)
    #
    # # # plt.show()
    # if not os.path.isdir(os.path.join(img_dir,str(coord))):
    #     os.makedirs(os.path.join(img_dir,str(coord)))
    #
    # fig.savefig(os.path.join(img_dir,str(coord))+'/'+'{}_∆w_plot.png'.format(coord),bbox_inches='tight',format='png',dpi=600)
    # plt.close(fig)
