# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:18:21 2017

This script is used to make to command line calls to load subject sets and
their subjects using the panoptes-cli and a manifest CSV file that is
written out from the slice_n_dice.py file. It assumes that the folder naming
conventions used will be unique as well as NOT have been used in this project
prior.

@author: Rdebbout
"""
import os
import subprocess
try: from tkFileDialog import askdirectory
except ImportError: from tkinter.filedialog import askdirectory

# Zooniverse Underwater World project number 5483
project_number = '5483'

def load(f):

    set_call = ['panoptes','subject-set', 'create', project_number , f]
    out = subprocess.Popen(set_call, stdout=subprocess.PIPE)
    set_no = out.communicate()[0].decode('utf-8').split(' ')[0]
    os.chdir(f)
    cmd = ['panoptes','subject-set','upload-subjects',set_no,'manifest.csv']
    subprocess.call(cmd)
    os.chdir('..')

if __name__ == '__main__':

#    ls_output = subprocess.check_output(['panoptes', 'info'])
#    print(ls_output.decode("utf-8"))

    msg = 'Select directory where trimmed folders were written out to:'
    vid_dir = askdirectory(title=msg, initialdir=os.path.expanduser("~"))
    os.chdir(vid_dir)
    total = len(os.listdir(vid_dir))
    for i, video in enumerate(os.listdir(vid_dir)):
        print(f'processing.../{video}/....{i+1} of {total} directories')
        load(video)
##############################################################################
# **CODE FOR SPLITTING INTO 9 IMAGES**

#import imageio
#import pandas as pd
#os.chdir('..')
#tbl_list = pd.read_excel('CitSci_VideoList_New2.xlsx')
#tbl_list.columns
#tbl_list.ix[tbl_list['CLIPPED']=='yes']
#num_img = 12
#
#for idx, row in tbl_list.iterrows():
##        break
#    print row.DLE_UID
#    # create subject-set using the UID
#    ttl = 'UID:%s' % row.UID
#    # create subject-set
#    set_call = 'panoptes subject-set create %s "%s"' % (project_number, ttl)
#    subprocess.call(set_call)
#    # get set ID number given by Zooniverse.org for loading....
#    set_id_str = subprocess.check_output('panoptes subject-set ls -p %s' % project_number)
#    set_no = set_id_str.split(ttl)[0].split('\n')[-1].replace(' ','')
#    # Create manifest and images in new dir
#    os.mkdir(str(row.UID))
#    # grab 9 images from video and write out as jpeg
#    vid = imageio.get_reader('./BetaTestingVideosClipped/%s' % row.clip_name)
#    shots = vid.get_length()
#    num_lst = range((shots / num_img) / 2, shots, (shots / num_img))
#    imgs = []
#    for num in num_lst:
#        imgs.append('shot_%s.jpeg' % (num))
#        image = vid.get_data(num)
#        imageio.imwrite('./%s/shot_%s.jpeg' % (row.UID,num), image)
#    # make manifest.csv with all 9 images in single row
#    imgDict = {'Image%s' % (x+1):[imgs[x]] for x in range(len(imgs))}
#    imgDict['SiteID'] = row.SiteID
#    mani = pd.DataFrame(imgDict)
#    # need to be in directory for command line call
#    os.chdir(str(row.UID))
#    mani.to_csv('manifest.csv',index=False)
#    cmd = 'panoptes subject-set upload-subjects %s manifest.csv' % set_no
#    subprocess.call(cmd)
#    os.chdir('..')
##############################################################################
# **USE THE PYTHON API** -- NEVER USED
#from panoptes_client import SubjectSet, Subject, Project, Panoptes
#
#Panoptes.connect(username='debbout.rick@epa.gov', password='Donsende1')
#project = Project.find(id = 5483)
#subject_set = SubjectSet.find(75635)
#subject_set = SubjectSet.find(72471)
#subject = Subject()
#subject.links.project = project
#subject.add_location({'video/mp4': './NIAG-001_B_01_trim_1.mp4'})
#subject.metadata['site_id'] = 'BOGUS'
#subject.save()
#subject_set.add(subject)
