import numpy as np
import pandas as pd
import scipy.signal as sg

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

import os

'''
Goal: We are trying to fit the data from a switching pulse to the conductivity response of potassium and sodium.

To achieve this, we will calculate the instantaneous conductance of the switching pulse at each point in time
and then average them according to the same time window as in the simulation. Afterwards, we can compare the
plots and see if we can fit the experimental data to the simulated data trend, or we try to solve some max conductance value.

'''

save_dir = "/Users/jasonyuan/Desktop"

def HH_func(input_array,n_00,n_01,t_0,tau_1,g_max):
    # n_00 = 0.1            # unitless ----> Gating prob at rest V
    # n_01 = 0.55            # unitless ----> Gating prob at V_step
    # t_0 = 3.1               # ms -----> Time where the rise begins
    # tau_1 = 0.02             # ms -----> Gating time constant
    # g_max = 0.22           # mS -----> Reflects the max conductance

    np_input = np.array(input_array)
    output = []

    gating_out = n_01 + (n_00-n_01)*np.exp(-(np_input-t_0)/tau_1)
    output = g_max * np.power(gating_out,4)

    return output

def conductance_plot(input_file, sim_dt=0.001, t_max=np.inf):
    # sim_dt default value is 1 ms

    # Read in the data from the input_file
    if "csv" in input_file:
        df = pd.read_csv(input_file)
        sub_df = df.to_numpy()[:,[0,3,1]]
        rows,cols = sub_df.shape
    else:
        df = pd.read_excel(input_file,sheet_name='Data')
        sub_df = df.filter(items=['TimeOutput','IMeasCh1','VMeasCh1']).to_numpy()
        rows,cols = sub_df.shape

    # Remove some number of points from the beginning of the data
    sub_df = sub_df[26:,:]

    ############################################################################

    # Calculate the instantaneous conductance that has been measured
    g = []
    time = []
    time_all = sub_df[:,0].tolist()

    for n in time_all:
        if n < t_max:
            time.append(n)

    for n in range(0,len(time)):
        if sub_df[n,2] == 0:
            g_val = 0.
        else:
            g_val = sub_df[n,1]/sub_df[n,2]   # Calculate instantaneous G

        g.append(g_val)

    ############################################################################

    # Average the instantaneous conductance by grouping sections of the data together
    t_start = time[0]
    t_end = time[0]+sim_dt

    time_dt = [0]
    g_dt = [0]
    while (t_start < time[-1]):
        if (t_end > time[-1]):
            average = 0
            n_points = 0
            for n in range(0,len(time)):
                if (time[n] > t_start):
                    average += g[n]
                    n_points += 1

            average = average/n_points
            time_dt.append(time[-1])
            g_dt.append(average)

            t_start += sim_dt
            t_end += sim_dt
        else:
            average = 0
            n_points = 0
            for n in range(0,len(time)):
                if (time[n] > t_start) and (time[n] < t_end):
                    average += g[n]
                    n_points += 1

            average = average/n_points
            time_dt.append(t_end)
            g_dt.append(average)

            t_start += sim_dt
            t_end += sim_dt

    ############################################################################

    # Save the conductance outputs to excel and csv values
    newly_processed = {}
    newly_processed['time'] = time_dt
    newly_processed['conductance'] = g_dt
    df_new = pd.DataFrame(newly_processed)
    df_new.to_excel(save_dir+'/'+'Conductance.xlsx')

    newly_processed_inst = {}
    newly_processed_inst['time'] = time
    newly_processed_inst['conductance'] = g
    df_new_inst = pd.DataFrame(newly_processed_inst)
    df_new_inst.to_csv(save_dir+'/'+'Conductance_inst.csv')

    ############################################################################

    # Plot the HH function and see how it models the instantaneous conductance
    time = np.array(time) * 1e3     # Convert time in seconds to milliseconds
    t_idx = 0

    # This part is for the rise portion of the plot
    for n in range(0,len(time)):
        if time[n] >= 1.65:          # This parameter should be tuned based on the data
            t_idx = n-1
            break
    ############################################################################

    # # This part is for the relaxation portion of the plot
    # for n in range(0,len(time)):
    #     if time[n] >= 8.0:          # This parameter should be tuned based on the data
    #         t_idx = n-1
    #         break
    ############################################################################
    vert_offset = 1.3e-9
    output1 = HH_func(time,0.1,0.6,0.5,0.03,7e-9) + vert_offset     # Rise plot
    output2 = HH_func(time,0.6,0.1,1.7,0.25,5e-9) + vert_offset      # Relaxation plot

    start_idx = 0
    start_idx_2 = 0

    ############################################################################

    # This part is for the rise portion of the plot -- where the rise starts
    for n in range(0,len(output1)):
        if time[n] >= 0.49:      # This parameter may be tuned depending on the data
            start_idx = n-1
            break
    ############################################################################

    # This part is for the relaxation portion of the plot -- where it starts to relax
    for n in range(0,len(output2)):
        if time[n] >= 1.65:      # This parameter may be tuned depending on the data
            start_idx_2 = n
            break
    ############################################################################

    g = np.array(g) * 1e3           # Convert Siemens to millisiemens

    # In Gloria's data, smoothing of the read pulse section
    # This part is for the relaxation portion of the plot

    last_positive = 0
    for n in range(t_idx,len(g)):
        if (sub_df[n,2] > 0.09) and (g[n] >= 0):
            last_positive = g[n]
        else:
            g[n] = last_positive
    ############################################################################

    # Save the complete output of rise and relaxation separately
    rise_data = {}
    rise_data['time'] = time
    rise_data['conductance'] = output1
    df_rise = pd.DataFrame(rise_data)
    df_rise.to_csv(save_dir+'/'+'HH_Rise_fit.csv')

    relax_data  = {}
    relax_data['time'] = time
    relax_data['conductance'] = output2
    df_rise = pd.DataFrame(relax_data)
    df_rise.to_csv(save_dir+'/'+'HH_Relax_fit.csv')

    # relax_data = {}
    # relax_data['time'] = time
    # relax_data['conductance'] = output2
    # df_relax = pd.DataFrame(relax_data)
    # df_relax.to_csv(save_dir+'/'+'HH_Relax_fit.csv')

    ############################################################################
    # moving_avg_g = sg.savgol_filter(x=g,window_length=7,polyorder=1,deriv=0)

    # Graph g_dt and time_dt
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1,label='1')
    ax2 = fig.add_subplot(2,1,2,label='2')
    # ax3 = fig.add_subplot(2,1,1,label='3',frame_on=False)

    ax1.plot(time[t_idx:],g[t_idx:],linestyle='-',label='Instantaneous G')
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.set_xlabel('time (ms)', color='k')
    ax1.set_ylabel('G (mS)', color='cornflowerblue')
    ax1.tick_params(axis='x', which='both', labelcolor='k')
    ax1.tick_params(axis='y', which='both', labelcolor='cornflowerblue')
    ax1.set_title('Instantaneous Conductance against Time')
    ax1.grid(linestyle='--', color='silver')
    # ax1.legend(loc='upper right')

    ax2.plot(time_dt,g_dt,linestyle='-',label='Average G')
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.set_xlabel('time (s)', color='k')
    ax2.set_ylabel('G (1/\u03A9)', color='cornflowerblue')
    ax2.tick_params(axis='x', which='both', labelcolor='k')
    ax2.tick_params(axis='y', which='both', labelcolor='cornflowerblue')
    ax2.set_title('Window Averaged Conductance against Time')
    ax2.grid(linestyle='--', color='silver')
    ax2.legend(loc='upper right')

    # ax3.plot(sub_df[t_idx:,0],sub_df[t_idx:,2],color='r',linestyle='--',label='Voltage')
    # ax3.tick_params(axis='x', which='both', bottom=False, labelbottom=False, labelcolor='r')
    # ax3.tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True, labelcolor='red')

    # ax1.plot(time[start_idx:],output1[start_idx:],color='r',linestyle='--',label='HH G')        # Rise part
    ax1.plot(time[start_idx_2:],output2[start_idx_2:],color='r',linestyle='--',label='HH G')    # Relax part
    # ax1.plot(time[start_idx:],np.append(output1[start_idx:start_idx_2],output2[start_idx_2:]),color='r',linestyle='--',label='HH G')  # Combined part

    # ax3.xaxis.set_minor_locator(AutoMinorLocator())
    # ax3.yaxis.set_minor_locator(AutoMinorLocator())
    # ax3.yaxis.tick_right()
    # ax3.set_ylabel('G (mS)', color='r')
    # ax3.tick_params(axis='x', which='both', bottom=False, labelbottom=False, labelcolor='r')
    # ax3.tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True, labelcolor='red')
    # ax3.yaxis.set_label_position('right')

    lines1,labels1 = ax1.get_legend_handles_labels()
    # lines3,labels3 = ax1.get_legend_handles_labels()
    # lgd = ax1.legend(lines1+lines3,labels1+labels3,loc='upper left')
    lgd = ax1.legend(lines1,labels1,loc='best')
    fig.tight_layout()

    fig.savefig(os.path.join(save_dir,'Conductance_plots.png'),bbox_inches='tight',format='png',dpi=600)
    plt.close(fig)

    return True

def main():

    excel_path = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Ion Channel/zihanrelax.xlsx"

    # conductance_plot(excel_path,sim_dt=0.0001,t_max=1.2*10**(-3))     # This is for rise
    conductance_plot(excel_path,sim_dt=0.0001,t_max=2.7*10**(-3))      # This is for relaxation and combined part

    return True

if __name__ == "__main__":
    main()
