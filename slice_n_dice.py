# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 09:11:41 2018

TODO: add manifest file to directory of videos
TODO: don't add vids that aren't certain length

@author: Rdebbout
"""

import os
import subprocess
import pandas as pd
from moviepy.editor import VideoFileClip

def julienne(fn='test', site='superior', where='./test'):
    out = '{}/{}'.format(where, site)
    if not os.path.exists(out):
        os.mkdir(out)
    video = VideoFileClip('{}.mp4'.format(fn), audio=False)
    num_windows = int(round((video.duration/15),0)) 
    end = round(video.duration % 15,1) # return remainder        
    clip_window_times = zip(range(0, 240, 15),range(15, 255, 15)) #max_len 4 min
    out_files = []
    for idx, seconds in enumerate(clip_window_times[:num_windows]):
        start = seconds[0]
        stop = seconds[1]
        if idx == num_windows-1:
            if end < 8:  # less than 8 seconds, dump!
                print 'yay'
                break
            stop = start + end
        out_files.append('{0}_{1}.mp4'.format(fn, (idx+1)))        
        clip = video.subclip(start,stop)
        clip.write_videofile('{0}/{1}_{2}_b4.mp4'.format(out, fn, (idx+1)))
        subprocess.call(('ffmpeg -i {0}/{1}_{2}_b4.mp4 -vf scale=640:360'
                ' {0}/{1}_{2}.mp4').format(out, fn, (idx+1)))
        # files compress better when resolution changed after clipping
        os.remove('{0}/{1}_{2}_b4.mp4'.format(out, fn, (idx+1)))
    return out_files


if __name__ == '__main__':
    
    test_dir = './processing_RD3'
    xl = pd.read_excel('CitSci_VideoList_New1.xlsx')
    xl = xl.ix[xl.BetaTestVideos == 'yes'].copy()
    # get filename w/o extension or path
    xl['clip_name'] = xl.Clipped_Hyperlink.apply(
                                    lambda x: x.split('.')[0].split('\\')[-1])

    for _, row in xl.iterrows():
        # make sure they're all there before processing
        print row.clip_name, row.SiteID
        if os.path.exists('./{}.mp4'.format(row.clip_name)):
            tbl = pd.DataFrame(columns=['Video','SiteID','Year','Waterbody'])
            tbl.Video = julienne(row.clip_name, row.SiteID, test_dir)
            tbl.SiteID = row.SiteID
            tbl.Year = row.Year
            tbl.Waterbody = row.Waterbody
            tbl.to_csv('{}/{}/manifest.csv'.format(test_dir, row.SiteID),
                       index=False)