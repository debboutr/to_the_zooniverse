# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:18:21 2017

This script clips 9 images out of videos at equal intervals based on length.
Creates a manifest.csv file for uplaoding subject-sets to www.zooniverse.org
through the panoptes-cli package. Command line calls are made using the 
subprocess module. 

@author: Rdebbout
"""
import os
import imageio
import subprocess
import pandas as pd

# Zooniverse Underwater World project number 5483
proj_num = 5483
os.chdir('..')
tbl_list = pd.read_excel('CitSci_VideoList_New.xlsx')
tbl_list.columns 
tbl_list.ix[tbl_list['CLIPPED']=='yes']

for idx, row in tbl_list.iterrows():
#        break
    print row.SiteID
    # create subject-set using the UID
    ttl = 'UID:%s' % row.UID
    # create subject-set
    set_call = 'panoptes subject-set create %s "%s"' % (proj_num, ttl)
    subprocess.call(set_call)
    # get set ID number given by Zooniverse.org for loading....
    set_id_str = subprocess.check_output('panoptes subject-set ls -p %s' % proj_num)
    set_no = set_id_str.split(ttl)[0].split('\n')[-1].replace(' ','')
    # Create manifest and images in new dir
    os.mkdir(str(row.UID))
    # grab 9 images from video and write out as jpeg
    vid = imageio.get_reader('./BetaTestingVideosClipped/%s' % row.clip_name)
    shots = vid.get_length()
    nums = range((shots / 9) / 2, shots, (shots / 9))
    imgs = []
    for num in nums:
        imgs.append('shot_%s.jpeg' % (num))
        image = vid.get_data(num)
        imageio.imwrite('./%s/shot_%s.jpeg' % (row.UID,num), image)
    # make manifest.csv with all 9 images in single row
    imgDict = {'Image%s' % (x+1):[imgs[x]] for x in range(len(imgs))}
    imgDict['SiteID'] = row.SiteID
    mani = pd.DataFrame(imgDict)
    # need to be in directory for command line call
    os.chdir(str(row.UID))
    mani.to_csv('manifest.csv',index=False)
    cmd = 'panoptes subject-set upload-subjects %s manifest.csv' % set_no
    subprocess.call(cmd)
    os.chdir('..')

###############################################################################
# RE_FORMAT COLUMN WITH CLIPPED NAMES....NAMES IN TABLE DON'T MATCH UP W/ DIR

tbl_list.drop('clip_name',axis=1,inplace=True)
clips = os.listdir('./BetaTestingVideosClipped')

for idx, row in tbl_list.iterrows():
    exp = row.Filename.split('.')[0]
    name = [clip for clip in clips if exp in clip][0]
    tbl_list.loc[idx,'clip_name'] = name
    
tbl_list[['Filename','clip_name']]

tbl_list.to_csv('CitSci_VideoList_beta.csv',index=False)
###############################################################################
ls_output = subprocess.check_output(['panoptes', 'info'])

len(pd.unique(tbl_list.UID))

os.getcwd()


    
for root, dirs, files in os.walk('./processing_RD2'):
    print dirs

ds = ['GLBA15-1041', 'GLBA15-1056', 'GLBA15-1069', 'GLNS15-2058', 'GLNS15-2192', 'LHLEC-029', 'LHLEC-033', 'LHLEC-037', 'LHLEC-102', 'LHLEC-111', 'LHLEC-115', 'LHLEC-120', 'NCCA15-01', 'NCCA15-07', 'NCCAGL10-1039', 'NCCAGL10-1046', 'NCCAGL10-1047', 'NCCAGL10-1066', 'NCCAGL10-1069', 'NCCAGL10-1113', 'NCCAGL10-GLBA10-004', 'NCCAGL10-GLBA10-122', 'NCCAGL10-NPS09-029', 'NCCAGL10-NPS09-050', 'STMR-001', 'STMR-003', 'STMR-006', 'STMR-012', 'STMR-013', 'STMR-019', 'STMR-021', 'STMR-023', 'STMR-024', 'STMR-041', 'STMR-046', 'STMR-051', 'STMR-052', 'STMR-053', 'STMR-073', 'STMR-074', 'STMR-078', 'STMR-081', 'STMR-082', 'STMR-084', 'STMR-094', 'STMT-003', 'STMT-027', 'STMT-088', 'STMT-092', 'STMT-093', 'STMT-094', 'STMT-096']
for d in ds:
    tbl = pd.read_csv('./processing_RD2/%s/manifest.csv'% d)
    if not tbl.iloc[-1].Video in os.listdir('./processing_RD2/%s'% d):
        print d
        tbl.iloc[:-1].to_csv('./processing_RD2/%s/manifest.csv'% d, index=False)

for d in ds:
    tbl = pd.read_csv('./processing_RD2/%s/manifest.csv'% d)
    print len(tbl) == len(os.listdir('./processing_RD2/%s'% d))-1
    
'%.1f' % (float(b)/1000000) + ' MB'

tot = 0
count =0
for d in ds:
    a = 1
    
    for f in os.listdir('./processing_RD3/%s'% d):
        tot+=1    
        size = os.path.getsize('./processing_RD3/%s/%s'% (d,f))
        if size > 3e6:
            if a:
#                print '#!' + d
                a=0
            print f + ' = %.1f' % (float(size)/1000000) + ' MB'
            count+=1
        
d = 'LHLEC-115'
f = 'LHLEC15_115GoProclip_4.mp4'
os.stat('./processing_RD2/%s/%s'% (d,f)).st_size