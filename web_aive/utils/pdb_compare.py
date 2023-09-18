from django.conf import settings
import pandas as pd
import numpy as np
import math
import os
import glob
import json
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
    
import datetime

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#pdb 파일 경로
wdir = 'F:/projectFiles/NEWGEANS/result/'
#변이 앞뒤 길이
trgt_len = 10
#변이와 거리
trgt_dist = 20

def parsing_pdb(pdb_path, header):
    f = open(pdb_path,'r')

    list_pdb = f.readlines()
    
    dic_pdb = {}
    # dfPdb = pd.DataFrame(columns=['ATOM','ATOM_SEQ','ATOM_NM','RESIDUE_NM','CHAIN_ID','RESIDUE_NM_SEQ','POS_X','POS_Y','POS_Z','OCCPANCY','TEMP_FACTOR','ATOM_SYMBOL'])
    
    for i, pdb_line in enumerate(list_pdb, start=0):
        atoms = pdb_line.split()
        # dfPdb.loc[i] = atoms
        # atom = atoms[0]
        # atom_seq = atoms[1]
        # atom_nm = atoms[2]
        # if atom == 'ATOM':
        #     char_alt_loc = ''
        #     residue_nm = atoms[3]
        #     chain_id = atoms[4]
        #     residue_nm_seq = atoms[5]
        #     achar_icode = ''
        #     pos_x = atoms[6]
        #     pos_y = atoms[7]
        #     pos_z = atoms[8]
        #     occpancy = atoms[9]
        #     temp_factor = atoms[10]
        #     atom_symbol = atoms[11]
        #     chg_atom = ''
            
        
        atom = pdb_line[0:6].replace(' ','')
        atom_seq = pdb_line[6:11].replace(' ','')
        atom_nm = pdb_line[12:16].replace(' ','')
        if atom == 'ATOM':
            char_alt_loc = pdb_line[16]
            residue_nm = pdb_line[17:20].replace(' ','')
            chain_id = pdb_line[21].replace(' ','')
            residue_nm_seq = pdb_line[22:26].replace(' ','')
            achar_icode = pdb_line[26].replace(' ','')
            pos_x = float(pdb_line[30:38].replace(' ',''))
            pos_y = float(pdb_line[38:46].replace(' ',''))
            pos_z = float(pdb_line[46:54].replace(' ',''))
            occpancy = pdb_line[54:60].replace(' ','')
            temp_factor = pdb_line[60:66].replace(' ','')
            atom_symbol = pdb_line[76:78].replace(' ','')
            chg_atom = pdb_line[78:80].replace(' ','')
        
        dic_pdb[i] = [atom, atom_seq, atom_nm, char_alt_loc, residue_nm, chain_id, residue_nm_seq, achar_icode, pos_x, pos_y, pos_z, occpancy, temp_factor, atom_symbol, chg_atom]

    dfPdb = pd.DataFrame.from_dict(dic_pdb, orient='index')
        
    dfPdb.columns=[f'{header}ATOM',f'{header}ATOM_SEQ',f'{header}ATOM_NM',f'{header}CHAR_ALT_LOC',f'{header}RESIDUE_NM',f'{header}CHAIN_ID',f'{header}RESIDUE_NM_SEQ',f'{header}ACHAR_ICODE',f'{header}POS_X',f'{header}POS_Y',f'{header}POS_Z',f'{header}OCCPANCY',f'{header}TEMP_FACTOR',f'{header}ATOM_SYMBOL',f'{header}CHG_ATOM']
        
    #dfPdb = pd.DataFrame(columns=['ATOM','ATOM_SEQ','ATOM_NM','CHAR_ALT_LOC','RESIDUE_NM','CHAIN_ID','RESIDUE_NM_SEQ','ACHAR_ICODE','POS_X','POS_Y','POS_Z','OCCPANCY','TEMP_FACTOR','ATOM_SYMBOL','CHG_ATOM'])
           
    # dfPdb.loc[i] = [atom, atom_seq, atom_nm, char_alt_loc, residue_nm, chain_id, residue_nm_seq, achar_icode, pos_x, pos_y, pos_z, occpancy, temp_factor, atom_symbol, chg_atom]    
    return dfPdb

def drawPdb(in_pdb: pd.DataFrame):
    x = []
    y = []
    z = []

    #전체 좌표 찍기
    for idx, pdb_info in in_pdb.iterrows():
        x.append(pdb_info[0])
        y.append(pdb_info[1])
        z.append(pdb_info[2])
        
    # #3d 차트 그리기 샘플
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')    
    
    ax.plot(x, y, z)
    
    plt.show()    

def find_center_pos(in_pdb: pd.DataFrame):
    #중심좌표 찾기
    df_s_max = in_pdb.groupby(['RESIDUE_NM_SEQ']).max(numeric_only=True).sort_values(by='RESIDUE_NM_SEQ').loc[:,['POS_X','POS_Y','POS_Z']]
    df_s_min = in_pdb.groupby(['RESIDUE_NM_SEQ']).min(numeric_only=True).sort_values(by='RESIDUE_NM_SEQ').loc[:,['POS_X','POS_Y','POS_Z']]
    
    df_s_cen = (df_s_max + df_s_min) / 2
    
    return df_s_cen

def calc_distinct(in_pdb: pd.DataFrame):
    dic_result = {}
    dic_pdb = in_pdb.to_dict(orient='list')
   
    for i, lst_pos_x in enumerate(dic_pdb['POS_X']):
       arr_dist = []
       for j, lst_pos_x in enumerate(dic_pdb['POS_X']):
           arr_dist.append(math.sqrt((dic_pdb['POS_X'][i] - dic_pdb['POS_X'][j]) ** 2 + (dic_pdb['POS_Y'][i] - dic_pdb['POS_Y'][j]) ** 2 + (dic_pdb['POS_Z'][i] - dic_pdb['POS_Z'][j]) ** 2))
           
       dic_result[i] = arr_dist
    
    df_result = pd.DataFrame.from_dict(dic_result, orient='index')
    
    return df_result
    
def read_pdb():
    
    pdb_path_1 = f'{wdir}/65_MUT_MT/ranked_0.pdb'
    pae_path_1 = f'{wdir}/65_MUT_MT/ranked_0_PAE.csv'
    pdb_path_2 = f'{wdir}/70_MUT_MT/ranked_0.pdb'
    pae_path_2 = f'{wdir}/70_MUT_MT/ranked_0_PAE.csv'
    
    df_wild = parsing_pdb(pdb_path_1,'')
    df_mut = parsing_pdb(pdb_path_2, '')
    
    # df_wild.to_csv('df_pdb1.csv')
    # df_mut.to_csv('df_pdb2.csv')
    
    # df_wild = pd.read_csv('df_pdb1.csv')
    # df_mut = pd.read_csv('df_pdb2.csv')
    
    df_cen_wild = find_center_pos(df_wild)
    df_cen_mut = find_center_pos(df_mut)
    
    df_dist_wild = calc_distinct(df_cen_wild)
    df_dist_mut = calc_distinct(df_cen_mut)
    
    
    drawPdb(df_cen_wild)
    drawPdb(df_cen_mut)
    
    pae1 = pd.read_csv(pae_path_1, sep=',', header=None)
    pae2 = pd.read_csv(pae_path_2, sep=',', header=None)
    
def print_time(msg):
    print(msg,datetime.datetime.now())
    return

if __name__ == '__main__':
    print_time('start')
    
    read_pdb()
    
    print_time('emd')
    