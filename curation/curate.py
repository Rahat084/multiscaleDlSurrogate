import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import seaborn as sns
import re
from scipy.signal import find_peaks

def plot_dictdf(dict_df):
    """ A function that takes a dictionary of dataframes as input and returns
     a Figure object comprises of an array of axes of shape (11,3). The 
     three columns are stress/stress component plotted against the loading 
     direction and the rows are different loading conditions
     """
    # Create figure and axes object
    fig,axs=plt.subplots(11,3,figsize=(18,60))
    # map the loading condition to a particular axes
    axes_map={"uniten_0":0, "unicomp_0": 1, "biten_0": 2, "bicomp_0":3,\
            "bitencomp_0":4,"uniten_2":5, "unicomp_2": 6, "biten_2": 7,\
             "bicomp_2":8,"bitencomp_2":9,"simple_2":10}
    for df_name in dict_df.keys():
        # get the dataframe
        df=dict_df[df_name]              
        #parse the nanoparticle parms
        m=re.search(r'(\d+\.\d+)_(\d+\.\d+)',df_name)
        label=m.group(1)+","+ m.group(2)
        axes_key=[ i for i in axes_map.keys() if i in df_name] # get the axes key
        # plot each stress component to their axes for a particular loading condition
        if "simple" in df_name:
            axs[axes_map[axes_key[0]],0].plot(df["strain12"],df["stress11"],label=label)
            axs[axes_map[axes_key[0]],0].legend()
            axs[axes_map[axes_key[0]],1].plot(df["strain12"],df["stress22"],label=label)
            axs[axes_map[axes_key[0]],1].legend()
            axs[axes_map[axes_key[0]],2].plot(df["strain12"],df["stress12"],label=label)
            axs[axes_map[axes_key[0]],2].legend()
            
        else:
            axs[axes_map[axes_key[0]],0].plot(df["strain11"],df["stress11"],label=label)
            axs[axes_map[axes_key[0]],0].legend()
            axs[axes_map[axes_key[0]],1].plot(df["strain11"],df["stress22"],label=label)
            axs[axes_map[axes_key[0]],1].legend()
            axs[axes_map[axes_key[0]],2].plot(df["strain11"],df["stress12"],label=label)
            axs[axes_map[axes_key[0]],2].legend()
    return fig

def point2percent_offset(strain,stress):
    """
    0.2% offset criteria to identify yield point
    """
    y1= stress.to_numpy()
    x=strain.to_numpy()
    m=(y1[500]-y1[0])/(x[500]-x[0])
    print(m)
    y= m*(x-0.003)
    d= (y1-y)**2
    plt.plot(x,y1)
    plt.plot(x,y)
    return np.argmin(d)

def iso2d_label(input_dict_df):
    
    """
    Function that takes dictionary of dataframes with stress strain values and adds defect classification label
    
    """
    
    dict_df=input_dict_df.copy()
    dict_keys= input_dict_df.keys()
    for n,dfname in enumerate(dict_keys):
        # Loading case: Uniaxial and Biaxial Tension
        if ("uniten" in dfname) or ("biten_" in dfname):
            print(n,dfname)
            thresh_map={"uniten_0": 1.779,"uniten_2":1.291,"biten_0":1.425,"biten_2":1.664}
            for tkey in thresh_map.keys():
                if tkey in dfname:
                    thresh=thresh_map[tkey]
            dict_df[dfname]["defect_mode"]=0
            idx1=dict_df[dfname]["stress11"].idxmax()
            print(idx1)
            dict_df[dfname]["defect_mode"].iloc[0:idx1]=1
            idx2=abs(dict_df[dfname]["stress11"].sub(thresh)).idxmin()
            print(idx2)
            dict_df[dfname]["defect_mode"][idx2:]=-1
        # Loading case: uniaxial compression, biaxial compression and biaxial tension compression
        elif ("unicomp" in dfname) or ("bicomp" in dfname) or ("bitencomp" in dfname):
            print(n,dfname)
            peaks,props=find_peaks(abs(dfs[dfname]["stress11"].to_numpy()),width=4)
            idx=peaks[0]
            dict_df[dfname]["defect_mode"]=0
            dict_df[dfname]["defect_mode"].iloc[0:idx]=1 
            print(idx)
        # Loading case: Simple Shear 
        elif "simple" in dfname:
            print(n,dfname)
            dict_df[dfname]["defect_mode"]=0
            idx=dict_df[dfname]["stress12"].idxmax()
            dict_df[dfname]["defect_mode"].iloc[0:idx]=1
            print(idx)
            
    return dict_df
