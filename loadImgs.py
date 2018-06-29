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
tbl_list = pd.read_csv('VideoListRick.csv')
os.chdir('LBE_data')
tbl_list.columns 
tbl_list.ix[tbl_list['CLIPPED']=='yes']
num_img = 12
vid_loc = 'D:/Projects/LBE_Analysis_Clipped_Videos'

for idx, row in tbl_list.iterrows():
        break
    print row.SiteID
    # create subject-set using the UID
    ttl = 'UID:%s' % row.UID
    # create subject-set
    set_call = 'panoptes subject-set create %s "%s"' % (proj_num, ttl)
#    subprocess.call(set_call)
    # get set ID number given by Zooniverse.org for loading....
#    set_id_str = subprocess.check_output('panoptes subject-set ls -p %s' % proj_num) # OLD WAY
    set_id_str = subprocess.check_output(set_call)
    set_no = set_id_str.split(ttl)[0].split('\n')[-1].replace(' ','')
    # Create manifest and images in new dir
    os.mkdir(str(row.UID))
    # grab 9 images from video and write out as jpeg
    vid = imageio.get_reader('%s/%s' % (vid_loc,row.Clipped_Filename))
    shots = vid.get_length()
    num_lst = range((shots / num_img) / 2, shots, (shots / num_img))
    imgs = []
    for num in num_lst:
        imgs.append('shot_%s.jpeg' % (num))
        image = vid.get_data(num)
        imageio.imwrite('./%s/shot_%s.jpeg' % (row.UID,num), image)
    # make manifest.csv with all 9 images in single row
    imgDict = {(i+1):[x] for i,x in enumerate(imgs)}
    mani = pd.DataFrame(imgDict)
    mani.columns = ['image_%s' % c for c in mani.columns]
    mani['UID'] = row.UID
    mani['SiteID'] = row.SiteID

#    mani = mani[['Image1','Image2','Image3','Image4','Image5','Image6','Image7','Image8','Image9','Image10','Image11','Image12','SiteID']]
    # need to be in directory for command line call
    os.chdir(str(row.UID))
    mani.to_csv('manifest.csv',index=False)
    cmd = 'panoptes subject-set upload-subjects %s manifest.csv' % set_no
    subprocess.call(cmd)
    os.chdir('..')
###############################################################################
cmd = 'panoptes subject-set ls 30055'
set_id_str = subprocess.check_output(cmd)

from panoptes_client import SubjectSet, Subject, Project, Panoptes
control = pd.read_csv('control.csv')
for _, row in control.iterrows():
    print row.number
    print row.UID
    subject_set = SubjectSet.find(row.number)
    subs = [int(subject.id) for subject in subject_set.subjects]
    subbies = str(subs)[1:-1].replace(',','')
    cmd = 'panoptes subject-set remove-subjects {} subject-ids {}'.format(row.number, subbies)
    subprocess.call(cmd)
    os.chdir(str(row.UID))
    tbl = pd.read_csv('manifest.csv')
    new = tbl[['image']].T
    new.columns = ['image_%s' % (c + 1) for c in new.columns]
    new.reset_index(drop=True,inplace=True)
    new.insert(loc=0,column='UID',value=[tbl.loc[0,'UID']])
    new.insert(loc=0,column='SiteID',value=[tbl.loc[0,'SiteID']])
    new.to_csv('manifest.csv',index=False)
    cmd = 'panoptes subject-set upload-subjects %s manifest.csv' % row.number
    subprocess.call(cmd)
    os.chdir('..')


###############################################################################
tbl_list.loc[tbl_list.UID == 176751]
tbl_list = tbl_list.loc[83:84]

#UID                                      176751
#SiteID                              GLBA15-1026
#Original_Filename        DVR010316_0017_001.avi
#Clipped_Filename     DVR010316_0017_001clip.mp4
#Name: 83, dtype: object

a = pd.read_csv('VideoListRick.csv')
b = pd.read_csv('cleaned.csv')

have = os.listdir('D:/Projects/LBE_Analysis_Clipped_Videos')
for f in a.Clipped_Filename:
#    break
    if not f in have:
        print f

[x for x in have if x[:7] == 'STMR085']
## RE_FORMAT COLUMN WITH CLIPPED NAMES....NAMES IN TABLE DON'T MATCH UP W/ DIR
#
#tbl_list.drop('clip_name',axis=1,inplace=True)
#clips = os.listdir('./BetaTestingVideosClipped')
#
#for idx, row in tbl_list.iterrows():
#    exp = row.Filename.split('.')[0]
#    name = [clip for clip in clips if exp in clip][0]
#    tbl_list.loc[idx,'clip_name'] = name
#    
#tbl_list[['Filename','clip_name']]
#
#tbl_list.to_csv('CitSci_VideoList_beta.csv',index=False)
###############################################################################
#ls_output = subprocess.check_output(['panoptes', 'info'])
#
#len(pd.unique(tbl_list.UID))
#
#os.getcwd()
#
#
#    
#for root, dirs, files in os.walk('./processing_RD2'):
#    print dirs
#
#ds = ['GLBA15-1041', 'GLBA15-1056', 'GLBA15-1069', 'GLNS15-2058', 'GLNS15-2192', 'LHLEC-029', 'LHLEC-033', 'LHLEC-037', 'LHLEC-102', 'LHLEC-111', 'LHLEC-115', 'LHLEC-120', 'NCCA15-01', 'NCCA15-07', 'NCCAGL10-1039', 'NCCAGL10-1046', 'NCCAGL10-1047', 'NCCAGL10-1066', 'NCCAGL10-1069', 'NCCAGL10-1113', 'NCCAGL10-GLBA10-004', 'NCCAGL10-GLBA10-122', 'NCCAGL10-NPS09-029', 'NCCAGL10-NPS09-050', 'STMR-001', 'STMR-003', 'STMR-006', 'STMR-012', 'STMR-013', 'STMR-019', 'STMR-021', 'STMR-023', 'STMR-024', 'STMR-041', 'STMR-046', 'STMR-051', 'STMR-052', 'STMR-053', 'STMR-073', 'STMR-074', 'STMR-078', 'STMR-081', 'STMR-082', 'STMR-084', 'STMR-094', 'STMT-003', 'STMT-027', 'STMT-088', 'STMT-092', 'STMT-093', 'STMT-094', 'STMT-096']
#for d in ds:
#    tbl = pd.read_csv('./processing_RD2/%s/manifest.csv'% d)
#    if not tbl.iloc[-1].Video in os.listdir('./processing_RD2/%s'% d):
#        print d
#        tbl.iloc[:-1].to_csv('./processing_RD2/%s/manifest.csv'% d, index=False)
#
#for d in ds:
#    tbl = pd.read_csv('./processing_RD2/%s/manifest.csv'% d)
#    print len(tbl) == len(os.listdir('./processing_RD2/%s'% d))-1
#    
#'%.1f' % (float(b)/1000000) + ' MB'
#
#tot = 0
#count =0
#for d in ds:
#    a = 1
#    
#    for f in os.listdir('./processing_RD3/%s'% d):
#        tot+=1    
#        size = os.path.getsize('./processing_RD3/%s/%s'% (d,f))
#        if size > 3e6:
#            if a:
##                print '#!' + d
#                a=0
#            print f + ' = %.1f' % (float(size)/1000000) + ' MB'
#            count+=1
#        
#d = 'LHLEC-115'
#f = 'LHLEC15_115GoProclip_4.mp4'
#os.stat('./processing_RD2/%s/%s'% (d,f)).st_size
###############################################################################
c = 0
for f in have:
    vid = f.split('.')[0].split('clip')[0]
    if vid in tbl.clip_name.tolist():
        c += 1
    else:
        print vid
        
tbl['clip_name'] = tbl.Filename.apply(lambda x: x.split('.')[0])
'DVR150624_1055_001' in tbl.clip_name.tolist()

for idx, row in tbl.iterrows():
#    break
    for f in have:
        vid = f.split('.')[0].split('clip')[0]
        if vid == row.clip_name:
#            break
            tbl.loc[idx,'clip_full'] = f

here = a[0]
boom = pd.DataFrame({'os_fns':have})
tbl_list.columns.tolist()
tbl_list.loc[tbl_list.Clipped_Filename.isin(boom.os_fns)]
boom['raw_name'] = boom.os_fns.apply(lambda x: x.split('.')[0])
new['raw_name'] = new.Clipped_Filename.apply(lambda x : x.split('.')[0])
new['raw_name2'] = new.raw_name.apply(lambda x : x.split('.')[0])
tbl_list.loc[:1101]
tbl_list.loc[1201:1221]
new = tbl_list.loc[:1101].copy()
new = new.append(tbl_list.loc[1201:1221])

final = pd.merge(boom, new, on='raw_name')
final = final[['UID','SiteID','Clipped_Filename']]

boom.loc[~boom.raw_name.isin(a)].raw_name


425         DVR150624_1055_001.mp4
555     Dvr150829_1336_001clip.mp4
642     NCCA15_01GoPro.MP4clip.mp4
648     NCCA15_07GoPro.MP4clip.mp4
699    STMR15_012GoPro.MP4clip.mp4
709    STMR15_023GoPro.MP4clip.mp4
741              STMT097_2clip.mp4

425        DVR150624_1055_001
555    Dvr150829_1336_001clip
642            NCCA15_01GoPro
648            NCCA15_07GoPro
699           STMR15_012GoPro
709           STMR15_023GoPro
741             STMT097_2clip
Name: raw_name, dtype: object

new.loc[new.raw_name == 'DVR150624_1055_001']
'DVR150624_1055_001' in new.raw_name.tolist()

have = os.listdir('LBE_Analysis_Clipped_Videos')


DVR150624_1055_001.mp4
DVR150624_1055_001clip.mp4

new.drop('raw_name2',axis=1,inplace=True)
new = new[['UID','SiteID','Clipped_Filename','raw_name','ALBERS_X','ALBERS_Y']]
new.columns.tolist()

new.loc[707,'raw_name'] = 'STMT097clip'
