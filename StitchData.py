import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

dir_path = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Keithley Data/Jason - 24mTorr Vertical Crossbar/Block 3/Feb 10/(1,5) Pulses"
save_dir = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Raw Data Plots/24mTorr/Block 3/Timing/Feb 10/Stitched Plot"
mode = "Pulse"      # Mode for pulse or timing

def sortkey(x):
    if (x == ".DS_Store"):
        return 0
    return int(x.split("_")[-1].split(".")[0])

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

if __name__ == "__main__":

    stitched_data = {}
    t_all = np.array([])
    V_all = np.array([])
    I_all = np.array([])

    files_sorted = sorted(os.listdir(dir_path),key=sortkey)
    print(files_sorted)

    for filename in files_sorted:
        file_path = os.path.join(dir_path,filename)

        if (not os.path.isfile(file_path)) or (not filename.endswith('.xls')):
            continue
        else:
            # Do the plotting
            print(filename)

            data = pd.read_excel(file_path,sheet_name='Data')
            if (mode == "Timimg"):
                time = data['TimeOutput'].to_numpy()
                voltage = data['VMeasCh1'].to_numpy()
                current = data['IMeasCh1'].to_numpy()
            else:
                time = data['A_T'].to_numpy()
                voltage = data['AWFMV'].to_numpy()
                current = data['AWFMI'].to_numpy()

            if (len(t_all) == 0):
                t_all = np.append(t_all,time)
                V_all = np.append(V_all,voltage)
                I_all = np.append(I_all,current)
            else:
                t_all = np.append(t_all,time+t_all[-1])
                V_all = np.append(V_all,voltage)
                I_all = np.append(I_all,current)

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1,label='1')
    ax2 = fig.add_subplot(1,1,1,label='2',frame_on=False)
    ax3 = fig.add_subplot(1,1,1,label='3',frame_on=False)

    ax1.plot(t_all, V_all,linestyle='-',color='cornflowerblue',label="Voltage")
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.set_xlabel('time (s)',color='k')
    ax1.set_ylabel('Voltage (V)', color='cornflowerblue')
    ax1.tick_params(axis='x', which='both', labelcolor='k')
    ax1.tick_params(axis='y', which='both', labelcolor='cornflowerblue')

    ax2.plot(t_all, I_all,linestyle='-',color='darkorange',label="Current")
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    # ax2.set_xticks([])
    ax2.yaxis.tick_right()
    ax2.tick_params(axis='x', which='both', bottom=False, labelbottom=False, labelcolor='darkorange')
    ax2.tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True, labelcolor='darkorange')
    ax2.set_ylabel('Current (A)', color='darkorange')
    ax2.yaxis.set_label_position('right')

    current_avg = movingaverage(I_all,50)
    # z = np.polyfit(t_all,I_all,2)
    # p = np.poly1d(z)
    ax3.plot(t_all,current_avg,linestyle='-',color='red',label="Rolling")
    # ax3.plot(t_all,p(t_all),linestyle='-',color='red',label="Fit")
    ax3.tick_params(axis='x', which='both', bottom=False, labelbottom=False, labelcolor='darkorange')
    ax3.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False, labelcolor='darkorange')

    ax1.grid(linestyle="--",color='silver')
    ax2.grid(linestyle="--",color='silver')
    ax3.grid(linestyle="--",color='silver')

    ax2.set_title("Combined pulse for 24mTorr device (1,5)")

    lines1,labels1 = ax1.get_legend_handles_labels()
    lines2,labels2 = ax2.get_legend_handles_labels()
    lines3,labels3 = ax3.get_legend_handles_labels()
    lgd = fig.legend(lines1+lines2+lines3,labels1+labels2+labels3,bbox_to_anchor=(1.07,0.75),loc="center")
    fig.tight_layout()
    # ax2.legend(lines1+lines2,labels1+labels2)
    # plt.show()

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    fig.savefig(save_dir+'/'+"Combined"+'.png',bbox_extra_artists=(lgd,),bbox_inches='tight',format='png',dpi=600)

    plt.close(fig)

    stitched_data["Time"] = t_all
    stitched_data["Voltage"] = V_all
    stitched_data["Current"] = I_all

    df_stitched = pd.DataFrame(stitched_data)
    df_stitched.to_excel(save_dir+"/"+"Combined.xlsx")
