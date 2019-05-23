# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 09:11:41 2018



@author: Rdebbout
"""

import os
import sys
import math
from os.path import expanduser
import subprocess
import pandas as pd
from moviepy.editor import VideoFileClip
try: from Tkinter import *; import tkMessageBox as messagebox# Py2
except ImportError: from tkinter import *; from tkinter import messagebox # Py3
try: from tkFileDialog import askopenfilename, askdirectory
except ImportError: from tkinter.filedialog import askopenfilename, askdirectory

Tk().withdraw()

class tkWindow:

    def __init__(self, master, columns, text, multi):

        master.minsize(width=350,height=400)
        master.winfo_toplevel().title('Split-Cat Evaluation Vars')

        self.frame = Frame(master)
        self.frame.pack()
        
        self.ok = Button(self.frame, text="OK", command=self.get_selection)
        self.ok.pack(side=BOTTOM)

        self.label = Label(self.frame, text=text)
        self.label.config(font=("Courier", 14))
        self.label.pack()
        
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        if multi:
            self.listbox = Listbox(self.frame, height=20, selectmode=MULTIPLE)
        else:
            self.listbox = Listbox(self.frame, height=20)
        self.listbox.pack(expand=True)
        for field in columns:
            self.listbox.insert(END, field)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)



class tkWindowSingle (tkWindow):

    def get_selection (self):
        self.select = self.listbox.get(self.listbox.curselection())
        self.frame.quit()

class tkWindowMulti (tkWindow):

    def get_selection (self):
        total = list()
        selection = self.listbox.curselection()
        for i in selection:
            entry = self.listbox.get(i)
            total.append(entry)
        self.select = total
        self.frame.quit()
        
def getField(*args, **kwargs):
    '''
    Runs the tkinter window for selection of column field w/in the table.
    '''    
    root = Tk()
    multi = kwargs.get('multi')
    if multi:
        app = tkWindowMulti(root, **kwargs)
    else:
        app = tkWindowSingle(root, **kwargs)
    root.mainloop()
    root.destroy()
    return (app.select)

if __name__ == '__main__':

    vid_dir = askdirectory(title='Select directory where the videos are stored',
                                               initialdir=expanduser("~"))
    os.chdir(vid_dir)
    out_dir = askdirectory(title='Select directory where to write out trimmed video folders',
                                               initialdir=expanduser("~"))
    ftypes = [("Acceptable Files",("*.csv","*.xlsx")),("All Files", "*.*")]
    f = askopenfilename(title='Select the control file ',
                        filetypes=ftypes,
                        initialdir=os.path.dirname(vid_dir))

    if f.split('.')[-1] == 'csv':
        control = pd.read_csv(f)
    if f.split('.')[-1] == 'xlsx':
        control = pd.read_excel(f)

    f_string = ("Select the Field\nthat aligns with the filename\nin the "
                                    "video directory\nthat you selected:")
    fname = getField(multi=False, columns=control.columns, text=f_string)
#    print len(control[fname].tolist())
#    control[fname].tolist() 
    v_files = [v.split('.')[0] for v in os.listdir(vid_dir)]
    if not set(v_files).issubset(set(control[fname].tolist())):
        print (('The following files don\'t have a matching title in the '
               '"%s" column of the csv:') % fname)
        for i in set(v_files):
            if not i in set(control[fname].tolist()):
                print ('\t' + i)
        sys.exit()
    control.drop_duplicates(fname, inplace=True)
    control = control.loc[control[fname].isin(v_files)].copy()


    # we are going under the assumption that the vid files will all be ".mp4" ext!!
    f_string = "Select the unique field for Subject Set naming in Zooniverse:"
    uid = getField(multi=False, columns=control.columns, text=f_string)
    fs_string = "Select additional fields that you want in Zooniverse:"
    keep = getField(multi=True, columns=control.columns, text=fs_string)


    for _, row in control.iterrows():
#        if row[uid] == toot:
#            break
        out = '{}/{}'.format(out_dir, row[uid])
#        if os.path.exists(out): continue
        if not os.path.exists(out):
            os.mkdir(out)

        print 'working on....{}'.format(row[uid])


        video = VideoFileClip('{}.mp4'.format(row[fname]), audio=False)

        columns = ['Video'] + keep
        tbl = pd.DataFrame(columns=columns)

        if video.duration < 15:
            finished = '{0}/{1}.mp4'.format(out, row[fname])
            subprocess.call(('ffmpeg -i {0}.mp4 -vf scale=640:360'
                    ' {1}').format(row[fname], finished))
            tbl_row = {fld:row[fld] for fld in keep}
            tbl_row['Video'] = finished.split('/')[-1]
            tbl = tbl.append(tbl_row, ignore_index=True)
            tbl.to_csv('{}/manifest.csv'.format(out), index=False)
            continue

        num_windows = int(math.ceil(video.duration/15))
        end = round(video.duration % 15,2) # return remainder        
        clip_window_times = zip(range(0, 480, 15),range(15, 495, 15)) #max_len 8 min
#        out_files = []
        for idx, seconds in enumerate(clip_window_times[:num_windows]):
#            break
            idx += 1
            start = seconds[0]
            stop = seconds[1]

            if idx == num_windows:
                if end < 5 and num_windows > 1:  # less than 5 seconds, dump!
                    continue
                if num_windows == 1:
                    pass
                stop = start + end

            print('\ttrimming {}/{} videos'.format(idx,
                                  num_windows-1 if end<5 else num_windows))

            clip = video.subclip(start,stop)
            finished = '{0}/{1}_{2}.mp4'.format(out, row[fname], idx)
            raw = finished.split('.')[0] + '_b4'
            clip.write_videofile('{}.mp4'.format(raw))
            subprocess.call(('ffmpeg -i {0}.mp4 -vf scale=640:360'
                    ' {1}').format(raw, finished))
            # files compress better when resolution changed after clipping
            os.remove('{}.mp4'.format(raw))

            tbl_row = {fld:row[fld] for fld in keep}
            tbl_row['Video'] = finished.split('/')[-1]
            tbl = tbl.append(tbl_row, ignore_index=True)
        tbl.to_csv('{}/manifest.csv'.format(out), index=False)



#
#    for _, row in xl.iterrows():
#        # make sure they're all there before processing
#        if not os.path.exists('{}/{}'.format(test_dir,row.SiteID)) and row.clip_name in shorts:
#            print row.clip_name, row.SiteID
#            break
#
#shorts = ['NIAG-061_B_01_trim','NIAG-059_B_02_trim','NIAG-070_B_01_trim',
#'NIAG-054_B_01_trim','NIAG-072_B_01_trim','NIAG-075_B_01_trim',
#'NIAG-046_B_01_trim','NIAG-065_B_01_trim','NIAG-046_B_02_trim',
#'17_B_trim_drop1','thess18_camB','NIAG-100_B_02_trim','NIAG-048_B_01_trim',]

##    test_dir = './processing_RD3'
#    test_dir = 'D:/Projects/to_the_zooniverse/vid_clips_05_2019'
#    xl = pd.read_excel('CitSci_VideoList_New1.xlsx')
#    xl = xl.ix[xl.BetaTestVideos == 'yes'].copy()
#    # get filename w/o extension or path
#    xl['clip_name'] = xl.Trimmed_Filename
#    xl['clip_name'] = xl.Clipped_Hyperlink.apply(
#                                    lambda x: x.split('.')[0].split('\\')[-1])
#
#in_dir = [f.split('.')[0] for f in os.listdir('Phase II Trimmed Videos')]
#xl = xl.loc[xl.Trimmed_Filename.isin(in_dir)]
#xl.drop_duplicates('Trimmed_Filename',inplace=True)