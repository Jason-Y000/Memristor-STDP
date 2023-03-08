import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, LogLocator
import numpy as np
import pandas as pd
import os

# dir_path is path to the folder with excel files
dir_path = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Keithley Data/Jason - 24mTorr Vertical Crossbar/Block 3/Feb 10/(1,5) Pulses"
base_pth = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Raw Data Plots/24mTorr/Block 3/Timing/Feb 10/Components of Stitched"

# file_path is path to the excel file
file_path = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Keithley Data/Au Vertical/February 27/1 mA scale/STDP_10V_Full_40mTorr_6_2.xls"

def strSplit(filename):
    string = filename.split("_")

    coord = "({},{})".format(string[len(string)-3],string[len(string)-2])
    rep = string[len(string)-1].split(".")[0]

    if "STDP" in filename:
        delta_T = string[1]
    else:
        delta_T = None

    return coord,rep,delta_T

if __name__ == "__main__":

    if file_path != "":
        data = pd.read_excel(file_path,sheet_name="Data")
        filename = file_path.split("/")[len(file_path.split("/"))-1]
        if "STDP" in filename:
            time = data['TimeOutput'].to_numpy()
            voltage_CH1 = data['VMeasCh1'].to_numpy()
            voltage_CH2 = data['VMeasCh2'].to_numpy()
            current_CH1 = data['IMeasCh1'].to_numpy()
            current_CH2 = data['IMeasCh2'].to_numpy()
        elif 'A_T' not in data:
            time = data['TimeOutput'].to_numpy()
            voltage = data['VMeasCh1'].to_numpy()
            current = data['IMeasCh1'].to_numpy()
        else:
            time = data['A_T'].to_numpy()
            voltage = data['AWFMV'].to_numpy()
            current = data['AWFMI'].to_numpy()

        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1,label='1')
        ax2 = fig.add_subplot(1,1,1,label='2',frame_on=False)

        if "STDP" in filename:
            ax1.plot(time,voltage_CH1,linestyle='-',color='cornflowerblue',label="Voltage CH1")
            ax1.plot(time,voltage_CH2,linestyle='-',color='slategrey',label='Voltage CH2')
            ax1.xaxis.set_minor_locator(AutoMinorLocator())
            ax1.yaxis.set_minor_locator(AutoMinorLocator())
            ax1.set_xlabel('time (s)',color='k')
            ax1.set_ylabel('Voltage (V)', color='cornflowerblue')
            ax1.tick_params(axis='x', which='both', labelcolor='k')
            ax1.tick_params(axis='y', which='both', labelcolor='cornflowerblue')

            ax2.plot(time,current_CH1,linestyle='-',color='darkorange',label="Current CH1")
            # ax2.plot(time,current_CH2,linestyle='-',color='tomato',label='Current CH2')
            ax2.xaxis.set_minor_locator(AutoMinorLocator())
            ax2.yaxis.set_minor_locator(AutoMinorLocator())
            # ax2.set_xticks([])
            ax2.yaxis.tick_right()
            ax2.tick_params(axis='x', which='both', bottom=False, labelbottom=False, labelcolor='darkorange')
            ax2.tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True, labelcolor='darkorange')
            ax2.set_ylabel('Current (A)', color='darkorange')
            ax2.yaxis.set_label_position('right')

        elif "Timing" in filename:
            ax1.plot(time, voltage,linestyle='-',color='cornflowerblue',label="Voltage")
            ax1.xaxis.set_minor_locator(AutoMinorLocator())
            ax1.yaxis.set_minor_locator(AutoMinorLocator())
            ax1.set_xlabel('time (s)',color='k')
            ax1.set_ylabel('Voltage (V)', color='cornflowerblue')
            ax1.tick_params(axis='x', which='both', labelcolor='k')
            ax1.tick_params(axis='y', which='both', labelcolor='cornflowerblue')

            ax2.plot(time, current,linestyle='-',color='darkorange',label="Current")
            ax2.set_yscale("log")
            ax2.xaxis.set_minor_locator(AutoMinorLocator())
            ax2.yaxis.set_minor_locator(LogLocator(base=10))
            # ax2.set_xticks([])
            ax2.yaxis.tick_right()
            ax2.tick_params(axis='x', which='both', bottom=False, labelbottom=False, labelcolor='darkorange')
            ax2.tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True, labelcolor='darkorange')
            ax2.set_ylabel('Current (A)', color='darkorange')
            ax2.yaxis.set_label_position('right')

        else:
            ax1.plot(time, voltage,linestyle='-',color='cornflowerblue',label="Voltage")
            ax1.xaxis.set_minor_locator(AutoMinorLocator())
            ax1.yaxis.set_minor_locator(AutoMinorLocator())
            ax1.set_xlabel('time (s)',color='k')
            ax1.set_ylabel('Voltage (V)', color='cornflowerblue')
            ax1.tick_params(axis='x', which='both', labelcolor='k')
            ax1.tick_params(axis='y', which='both', labelcolor='cornflowerblue')

            ax2.plot(time, current,linestyle='-',color='darkorange',label="Current")
            ax2.xaxis.set_minor_locator(AutoMinorLocator())
            ax2.yaxis.set_minor_locator(AutoMinorLocator())
            # ax2.set_xticks([])
            ax2.yaxis.tick_right()
            ax2.tick_params(axis='x', which='both', bottom=False, labelbottom=False, labelcolor='darkorange')
            ax2.tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True, labelcolor='darkorange')
            ax2.set_ylabel('Current (A)', color='darkorange')
            ax2.yaxis.set_label_position('right')

        ax1.grid(linestyle="--",color='silver')
        ax2.grid(linestyle="--",color='silver')

        ax2.set_title(filename.split(".")[0])
        lines1,labels1 = ax1.get_legend_handles_labels()
        lines2,labels2 = ax2.get_legend_handles_labels()
        lgd = fig.legend(lines1+lines2,labels1+labels2,bbox_to_anchor=(1.07,0.75),loc='center')
        fig.tight_layout()
        # ax2.legend(lines1+lines2,labels1+labels2)
        plt.show()

        # fig.savefig('/Users/jasonyuan/Desktop/'+filename.split(".")[0]+'.png',bbox_extra_artists=(lgd,),bbox_inches='tight',format='png',dpi=600)

    else:
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path,filename)
            if (not os.path.isfile(file_path)) or (not filename.endswith('.xls')):
                continue
            else:
                # Do the plotting
                print(filename)
                coord,rep,delta_T = strSplit(filename)

                data = pd.read_excel(file_path,sheet_name='Data')
                if "STDP" in filename:
                    time = data['TimeOutput'].to_numpy()
                    voltage_CH1 = data['VMeasCh1'].to_numpy()
                    voltage_CH2 = data['VMeasCh2'].to_numpy()
                    current_CH1 = data['IMeasCh1'].to_numpy()
                    current_CH2 = data['IMeasCh2'].to_numpy()
                elif 'A_T' not in data:
                    time = data['TimeOutput'].to_numpy()
                    voltage = data['VMeasCh1'].to_numpy()
                    current = data['IMeasCh1'].to_numpy()
                else:
                    time = data['A_T'].to_numpy()
                    voltage = data['AWFMV'].to_numpy()
                    current = data['AWFMI'].to_numpy()

                # print(data)
                # print(time)

                fig = plt.figure()
                ax1 = fig.add_subplot(1,1,1,label='1')
                ax2 = fig.add_subplot(1,1,1,label='2',frame_on=False)

                if "Timing" in filename:
                    ax1.plot(time, voltage,linestyle='-',color='cornflowerblue',label="Voltage")
                    ax1.xaxis.set_minor_locator(AutoMinorLocator())
                    ax1.yaxis.set_minor_locator(AutoMinorLocator())
                    ax1.set_xlabel('time (s)',color='k')
                    ax1.set_ylabel('Voltage (V)', color='cornflowerblue')
                    ax1.tick_params(axis='x', which='both', labelcolor='k')
                    ax1.tick_params(axis='y', which='both', labelcolor='cornflowerblue')

                    ax2.plot(time, current,linestyle='-',color='darkorange',label="Current")
                    ax2.set_yscale("log")
                    ax2.xaxis.set_minor_locator(AutoMinorLocator())
                    ax2.yaxis.set_minor_locator(LogLocator(base=10))
                    # ax2.set_xticks([])
                    ax2.yaxis.tick_right()
                    ax2.tick_params(axis='x', which='both', bottom=False, labelbottom=False, labelcolor='darkorange')
                    ax2.tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True, labelcolor='darkorange')
                    ax2.set_ylabel('Current (A)', color='darkorange')
                    ax2.yaxis.set_label_position('right')

                elif "STDP" not in filename:
                    ax1.plot(time, voltage,linestyle='-',color='cornflowerblue',label="Voltage")
                    ax1.xaxis.set_minor_locator(AutoMinorLocator())
                    ax1.yaxis.set_minor_locator(AutoMinorLocator())
                    ax1.set_xlabel('time (s)',color='k')
                    ax1.set_ylabel('Voltage (V)', color='cornflowerblue')
                    ax1.tick_params(axis='x', which='both', labelcolor='k')
                    ax1.tick_params(axis='y', which='both', labelcolor='cornflowerblue')

                    ax2.plot(time, current,linestyle='-',color='darkorange',label="Current")
                    ax2.xaxis.set_minor_locator(AutoMinorLocator())
                    ax2.yaxis.set_minor_locator(AutoMinorLocator())
                    # ax2.set_xticks([])
                    ax2.yaxis.tick_right()
                    ax2.tick_params(axis='x', which='both', bottom=False, labelbottom=False, labelcolor='darkorange')
                    ax2.tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True, labelcolor='darkorange')
                    ax2.set_ylabel('Current (A)', color='darkorange')
                    ax2.yaxis.set_label_position('right')

                else:
                    ax1.plot(time,voltage_CH1,linestyle='-',color='cornflowerblue',label="Voltage CH1")
                    ax1.plot(time,voltage_CH2,linestyle='-',color='slategrey',label='Voltage CH2')
                    ax1.xaxis.set_minor_locator(AutoMinorLocator())
                    ax1.yaxis.set_minor_locator(AutoMinorLocator())
                    ax1.set_xlabel('time (s)',color='k')
                    ax1.set_ylabel('Voltage (V)', color='cornflowerblue')
                    ax1.tick_params(axis='x', which='both', labelcolor='k')
                    ax1.tick_params(axis='y', which='both', labelcolor='cornflowerblue')

                    ax2.plot(time,current_CH1,linestyle='-',color='darkorange',label="Current CH1")
                    ax2.plot(time,current_CH2,linestyle='-',color='tomato',label='Current CH2')
                    ax2.xaxis.set_minor_locator(AutoMinorLocator())
                    ax2.yaxis.set_minor_locator(AutoMinorLocator())
                    # ax2.set_xticks([])
                    ax2.yaxis.tick_right()
                    ax2.tick_params(axis='x', which='both', bottom=False, labelbottom=False, labelcolor='darkorange')
                    ax2.tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True, labelcolor='darkorange')
                    ax2.set_ylabel('Current (A)', color='darkorange')
                    ax2.yaxis.set_label_position('right')

                ax1.grid(linestyle="--",color='silver')
                ax2.grid(linestyle="--",color='silver')

                ax2.set_title(filename.split(".")[0])
                # if "STDP" in filename:
                #     ax2.set_title("STDP test of device at {}, iteration {} \n and ΔT = {}".format(coord,rep,delta_T))
                # elif ("before" in filename.lower()) or ("after" in filename.lower()):
                #     ax2.set_title("Probe pulse measurement of device at {} \n and iteration {}".format(coord,rep))
                # else:
                #     ax2.set_title("Pulsed I-V Test \n voltage and current against time")

                lines1,labels1 = ax1.get_legend_handles_labels()
                lines2,labels2 = ax2.get_legend_handles_labels()
                lgd = fig.legend(lines1+lines2,labels1+labels2,bbox_to_anchor=(1.07,0.75),loc="center")
                fig.tight_layout()
                # ax2.legend(lines1+lines2,labels1+labels2)
                # plt.show()

                base = os.path.basename(file_path)
                if not os.path.isdir(base_pth):
                    os.makedirs(base_pth)
                fig.savefig(base_pth+'/'+os.path.splitext(base)[0]+'.png',bbox_extra_artists=(lgd,),bbox_inches='tight',format='png',dpi=600)


                # if ("STDP" in filename) or ("before" in filename.lower()) or ("after" in filename.lower()):
                #     if not os.path.isdir(base_pth + '/' + "{}_{}".format(coord,rep)):
                #         os.makedirs(os.path.join(base_pth,"{}_{}".format(coord,rep)))
                #     fig.savefig(os.path.join(base_pth,"{}_{}".format(coord,rep))+'/'+os.path.splitext(base)[0]+'.png',bbox_extra_artists=(lgd,),bbox_inches='tight',format='png',dpi=600)
                # else:
                #     fig.savefig(base_pth+'/'+os.path.splitext(base)[0]+'.png',bbox_extra_artists=(lgd,),bbox_inches='tight',format='png',dpi=600)

                plt.close(fig)
