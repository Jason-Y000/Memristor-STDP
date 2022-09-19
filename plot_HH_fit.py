import os

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, LogLocator, FormatStrFormatter

import pandas as pd


# This will be the path to the HH fit file. Path 1 is rise and 2 is relax
HH_pth1 = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Ion Channel/Zihan's Conductance v2/Combined/HH_Rise_fit.csv"
HH_pth2 = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Ion Channel/Zihan's Conductance v2/Combined/HH_Relax_fit.csv"

# For this path, you can use the Conductance_inst.csv which was made with using a moving windows average like method
# Otherwise, you'll need to calculate the instantaneous conductance and then filter from the original raw data
# In this example, I've used the raw data, but without smoothing/averaging
data_pth = "/Users/jasonyuan/Desktop/Kherani Lab/Memristor/Ion Channel/zihanrelax.xlsx"

if __name__ == "__main__":

    # This first part is for reading in the data

    df_data = pd.read_excel(data_pth,sheet_name='Data')
    np_data = df_data.filter(items=['TimeOutput','IMeasCh1','VMeasCh1']).to_numpy()
    np_data = np_data[26:,:]
    rows_data, cols_data = np_data.shape

    df_HH_1 = pd.read_csv(HH_pth1)
    np_HH_1 = df_HH_1.filter(items=['time','conductance']).to_numpy()
    rows_HH_1, cols_HH_1 = np_HH_1.shape

    df_HH_2 = pd.read_csv(HH_pth2)
    np_HH_2 = df_HH_2.filter(items=['time','conductance']).to_numpy()
    rows_HH_2, cols_HH_2 = np_HH_2.shape

    # This part is to filter certain points in the read in data
    # For the HH data, start plotting points after its t_0 value
    for n in range(rows_data):
        if (np_data[n,0]*1000 > 0.5):
            start_data = n
            break
    for n in range(rows_data):  # Applies to Zihan's data
        if (np_data[n,0]*1000 > 2.7):
            end_data = n
            break

    for n in range(rows_HH_1):
        if (np_HH_1[n,0] > 0.5):
            start_HH_1 = n
            break
    for n in range(rows_HH_1):
        if (np_HH_1[n,0] > 1.68):
            end_HH_1 = n
            break

    for n in range(rows_HH_2):
        if (np_HH_2[n,0] > 1.68):
            start_HH_2 = n
            break

    # This part plots
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(np_data[start_data:end_data,0]*1000, np_data[start_data:end_data,1]/np_data[start_data:end_data,2]*1000,color='b',linestyle='-',label='Data')
    ax1.plot(np_HH_1[start_HH_1:end_HH_1,0],np_HH_1[start_HH_1:end_HH_1,1],color='r',linestyle='--',label='HH G Rise')
    ax1.plot(np_HH_2[start_HH_2:,0],np_HH_2[start_HH_2:,1],color='r',linestyle='--',label='HH G Relax')

    ax1.set_yscale("log")
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    # ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(LogLocator())
    ax1.set_xlabel('time (ms)', color='k')
    ax1.set_ylabel('G (mS)', color='cornflowerblue')
    ax1.tick_params(axis='x', which='both', labelcolor='k')
    ax1.tick_params(axis='y', which='both', labelcolor='cornflowerblue')
    ax1.yaxis.set_minor_formatter(FormatStrFormatter("%.1f"))
    ax1.set_title('Conductance change over time')
    ax1.grid(linestyle='--', color='silver')
    ax1.legend(loc='upper right')

    fig.tight_layout()
    plt.show()
