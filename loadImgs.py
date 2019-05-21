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
tbl_list = pd.read_excel('CitSci_VideoList_New2.xlsx')
tbl_list.columns 
tbl_list.ix[tbl_list['CLIPPED']=='yes']
num_img = 12

for idx, row in tbl_list.iterrows():
#        break
    print row.DLE_UID
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
    num_lst = range((shots / num_img) / 2, shots, (shots / num_img))
    imgs = []
    for num in num_lst:
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
# new method for loading up Phase II videos into 1 SubjectSet!!
# make 50 vids in different locations into jst one subject set..
from shutil import copyfile
tbl = pd.read_csv('PhaseIIBetaTestList_new.csv')
tbl = tbl[tbl.BetaTestVid.notnull()]
tbl = tbl[['DLE_UID','SiteID','BetaTestVid','clipped_files']]
mani = pd.DataFrame(columns=['DLE_UID','SiteID','video'])
for idx, group in tbl.groupby('DLE_UID'):
#    print(idx)
#    print(group)
    for idx, row in group.iterrows():
#        print idx
        mani.loc[idx] = [row.DLE_UID, row.SiteID, os.path.join(os.getcwd(),row.clipped_files)]
        copyfile('out/%s/%s' %(row.DLE_UID,row.clipped_files), 'upload/%s' % row.clipped_files)
mani.to_csv('manifest.csv', index=False)

set_call = 'panoptes subject-set create %s "PhaseII"' % (proj_num)
subprocess.call(set_call)
set_id_str = subprocess.check_output('panoptes subject-set ls -p %s' % proj_num)
set_no = set_id_str.split("PhaseII")[0].split('\n')[-1].replace(' ','')
os.chdir('upload')
cmd = 'panoptes subject-set upload-subjects %s manifest.csv' % set_no
subprocess.call(cmd)

# above didn't work
from panoptes_client import SubjectSet, Subject, Project, Panoptes

Panoptes.connect(username='debbout.rick@epa.gov', password='Donsende1')
project = Project.find(id = 5483)
subject_set = SubjectSet.find(75635)
subject_set = SubjectSet.find(72471)
subject = Subject()
subject.links.project = project
subject.add_location({'video/mp4': './NIAG-001_B_01_trim_1.mp4'})
subject.metadata['site_id'] = 'BOGUS'
subject.save()
subject_set.add(subject)

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
tbl_list.loc[:1101]
tbl_list.loc[1201:1221]
new = tbl_list.loc[:1101].copy()
new = new.append(tbl_list.loc[1201:1221])

a = pd.merge(boom, new, on='raw_name').raw_name
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

import panoptes_client
workflow = project.links.workflows[4]
sets_to_unlink = workflow.links.subject_sets
for item in sets_to_unlink:
    try:
        workflow.remove_subject_sets(item.id)
        print(item)
    except panoptes_client.panoptes.PanoptesAPIException:
        print('fail')
        pass # take appropriate action
        

a=os.listdir('.')
uno = a[1]

set_call = 'panoptes subject-set create %s "%s"' % (proj_num, uno)
subprocess.call(set_call)
set_id_str = subprocess.check_output('panoptes subject-set ls -p %s' % proj_num)
set_no = set_id_str.split(uno)[0].split('\n')[-1].replace(' ','')
os.chdir(uno)
cmd = 'panoptes subject-set upload-subjects %s manifest.csv' % set_no
subprocess.call(cmd)



for uno in os.listdir('.'):
    print uno
    mani = '{}/manifest.csv'.format(uno)
    tbl = pd.read_csv(mani)
    for _,row in tbl.iterrows():
        row.Video = row.Video.split('/')[-1]
    tbl.to_csv(mani, index=False)


for uno in os.listdir('.'):
    mani = '{}/manifest.csv'.format(uno)
    tbl = pd.read_csv(mani)
    if '/' in tbl.loc[0,'Video']:
        print uno

        for i,row in tbl.iterrows():
            tbl.loc[i,'Video'] = tbl.loc[i,'Video'].split('/')[-1]
        tbl.to_csv(mani, index=False)
