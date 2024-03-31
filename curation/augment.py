import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import seaborn as sns
import re

def cubic_sym(df):
    """ Function to perform cubic symmetry transformation"""
    tmp=df["strain11"].copy()
    df["strain11"]= df["strain22"].copy()
    df["strain22"]= tmp
    df["strain12"]= 1*df["strain12"].copy()

    tmp=df["stress11"].copy()
    df["stress11"]= df["stress22"].copy()
    df["stress22"]= tmp
    df["stress12"]= 1*df["stress12"].copy()
    return df

def inverse_shear_sym(df):
    """ Function to perform inverse shear symmetry transformation"""
    df["strain12"]= -1*df["strain12"].copy()
    df["stress12"]= -1*df["stress12"].copy()
    return df

def iso2d_augment(input_dict_df):
    """ Function that takes simulation data frames and provides augmented dataframes"""
    # Make a copy of dictionary
    dict_df=input_dict_df.copy()
    # Map of the transformations
    cubic_map={ "uniten_0":"uniteny_0","unicomp_0":"unicompy_0","bitencomp_0":"bitencompy_0","uniten_2":"uniteny_2",\
            "unicomp_2":"unicompy_2","bitencomp_2":"bitencompy_2"}
    inv_shear_map={ "uniten_2":"uniten_-2","unicomp_2":"unicomp_-2","bitencomp_2":"bitencomp_-2",\
            "biten_2":"biten_-2", "bicomp_2":"bicomp_-2","simple_2":"simple_-2"}
    cubic_map2={"uniten_-2":"uniteny_-2","unicomp_-2":"unicompy_-2","bitencomp_-2":"bitencompy_-2"}
    #pattern=re.compile(r"\w+_(\d+\.\d+)_(\d+\.\d+)_((\w+)_(\d))")
    pattern=re.compile(r"(\w+_-?\d)(.+)$")
    dict_keys=input_dict_df.keys()
    for dfname in dict_keys:
        m=pattern.match(dfname)
        if m[1] in cubic_map.keys():
            # cubic transformed dataframe name
            tdf_name=pattern.sub(cubic_map[m[1]]+"\\2",dfname)
            dict_df[tdf_name]=cubic_sym(dict_df[dfname].copy())
        if m[1] in inv_shear_map.keys():
            # inverse shear transformed dataframe name
            tdf_name=pattern.sub(inv_shear_map[m[1]]+"\\2",dfname)
            dict_df[tdf_name]=inverse_shear_sym(dict_df[dfname].copy())
    dict_keys=list(dict_df.keys()).copy()
    for dfname in dict_keys:
        m=pattern.match(dfname)
        if m[1] in cubic_map2.keys():
            # 2nd cubic transformed dataframe name
            tdf_name=pattern.sub(cubic_map2[m[1]]+"\\2",dfname)
            dict_df[tdf_name]=cubic_sym(dict_df[dfname].copy())
    return dict_df
