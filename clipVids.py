# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 16:14:41 2017

this is now a practice space, images being clipped w/ loadImgs.py

@author: Rdebbout
"""

import os
import pylab
import imageio

for f in os.listdir('./vids'):    
    break
    vid = imageio.get_reader('./BetaTestingVideosClipped/%s' % f)
    shots = vid.get_length()
    nums = range((shots / 6) / 2, shots, (shots / 6))
    if not os.path.exists('./%s' % f.split('.')[0]):
        os.mkdir('./%s' % f.split('.')[0])
    for num in nums:
        image = vid.get_data(num)
        imageio.imwrite('%s/test_%s.jpeg' % (f.split('.')[0],num), image)
        fig = pylab.figure()
        fig.suptitle('{}/nimage #{}'.format(f,num), x=.5, y=1.1, fontsize=20)
        pylab.imshow(image)
    pylab.show()
    
    
f = os.listdir('./vids')[1]
f = 'bit_down2.mp4'

from moviepy.editor import VideoFileClip
clip = VideoFileClip('./%s' % f,audio=False).subclip(0,15)
clip.write_videofile('bit_down2_clip.mp4')
# easy!!
# length of video 
clip.duration

os.getcwd()

vid = imageio.get_reader('./test_out4.mp4')
shots = vid.get_length()
nums = range(0,shots,4)

with imageio.get_writer('test_num.mp4',mode='I') as writer:
    for num in nums:
        img = vid.get_data(num)
        writer.append_data(img)

''' ...when writing to .mp4...
WARNING:root:IMAGEIO FFMPEG_WRITER WARNING: input image is not divisible by 
macro_block_size=16, resizing from (1080L, 1920L) to (1088L, 1920L) to ensure 
video compatibility with most codecs and players. To prevent resizing, make 
your input image divisible by the macro_block_size or set the macro_block_size 
to None (risking incompatibility). You may also see a FFMPEG warning concerning 
speedloss due to data not being aligned.        
'''
imageio.get_writer?


a = VideoFileClip('./test_out3.mp4')
a.preview()

imageio.imwrite('crop.jpeg', image[:,160:1765,:])

# bit rate
#(img) C:/Users/Rdebbout/Downloads/vids_DUL>ffmpeg -i test_out4.mp4 -b 1397520 bit_down2.mp4
# resolution
#(img) C:/Users/Rdebbout/Downloads/vids_DUL>ffmpeg -i test_out4.mp4 -vf scale=960:540 bit_down_scale.mp4

# ffprobe -v quiet -print_format json -show_format -show_streams test_out4.mp4 > op.json

################################################################################
# Test frame rate
#TODO: UID and SiteID
TESTS = [ 'DVR150712_1230_001clip.mp4',
         'DVR150719_1534_001clip.mp4',
         'DVR150811_1230_001clip.mp4',
         'DVR150917_1805_001clip.mp4',
         'DVR150924_1230_001clip.mp4',
         'DVR150924_1331_001clip.mp4',
         'DVR150925_1048_001clip.mp4',
         'DVR150925_1432_001clip.mp4',]

tbl_list = pd.read_excel('CitSci_VideoList_New.xlsx')
tbl_list.columns 

work = tbl_list.loc[tbl_list['BetaTestVideos'] =='yes',['UID','SiteID','Clipped_Hyperlink']]

def trim(string):
    out = string.split('\\')[-1].split('.')[0]
    return out if out[-4:]=='clip' else out + 'clip' # excel file misnomer
# All filenames adjusted to have a lower case 'mp4' extension in PowerShell
work['Clipped_Name'] = work['Clipped_Hyperlink'].apply(trim)
inDir = [f.split('.')[0] for f in os.listdir('.') if 'clip.mp4' in f]
for f in inDir:
    if not f in work['Clipped_Name'].tolist():
        print f

from moviepy.editor import VideoFileClip
for f in TESTS:
    clip = VideoFileClip('./BetaTestingVideosClipped/%s' % f,
                         audio=False).subclip(37,47)
    clip.write_videofile('./test_frame_rate/duo_%s' % f)


from panoptes_client import SubjectSet, Subject, Project, Panoptes

Panoptes.connect(username='debbout.rick@epa.gov', password='Donsende1')
project = Project.find(id = 5483)
subject_set = SubjectSet.find(17639)
subject = Subject()
subject.links.project = project
subject.add_location({'video/mp4': ('C:/Users/Rdebbout/Downloads/vids_DUL/'
                        'test_frame_rate/duo_DVR150925_1432_001clip.mp4')})
subject.metadata['site_id'] = 'NCCAGL10-1047'
subject.save()
subject_set.add(subject)


os.listdir('./test_frame_rate')
test_frame_rate\duo_DVR150925_1432_001clip.mp4

################################################################################
import os
import subprocess
import pandas as pd

here = 'C:/Users/Rdebbout/Downloads/vids_DUL/test_frame_rate/prepare_ye'
tbl_list = pd.read_csv('CitSci_VideoList_beta.csv')

for f in os.listdir(here):
    print f
    subprocess.call('ffmpeg -i {0} -vf scale=960:540 {1}_test.mpeg'.format(f,f.split('.')[0]))


################################################################################
# create 15s clips of the entire video
# seems better to reduce resolution after the clip has been made 
import os
import subprocess
import pandas as pd
from moviepy.editor import VideoFileClip

def window_video(fn='test', site='superior', where='./test'):
    out = '{}/{}'.format(where, site)
    if not os.path.exists(out):
        os.mkdir(out)
    video = VideoFileClip('{}.mp4'.format(fn), audio=False)
    num_windows = int(round((video.duration/15),0))
    end = round(video.duration % 15,1) # return remainder
    clip_window_times = zip(range(0, 240, 15),range(15, 255, 15)) #max_len 4 min
    for idx, seconds in enumerate(clip_window_times[:num_windows]):
        start = seconds[0]
        stop = seconds[1]
        if idx == num_windows-1:
            stop = start + end
        clip = video.subclip(start,stop)
        clip.write_videofile('{0}/{1}_{2}_b4.mp4'.format(out, fn, (idx+1)))
        subprocess.call(('ffmpeg -i {0}/{1}_{2}_b4.mp4 -vf scale=960:540'
                ' {0}/{1}_{2}.mp4').format(out, fn, (idx+1)))
        os.remove('{0}/{1}_{2}_b4.mp4'.format(out, fn, (idx+1)))

test_dir = './processing_RD'
xl = pd.read_excel('CitSci_VideoList_New1.xlsx')
xl = xl.ix[xl.BetaTestVideos == 'yes'].copy()
xl['clip_name'] = xl.Clipped_Hyperlink.apply(
                                    lambda x: x.split('.')[0].split('\\')[-1])

for filename, site_id in zip(xl.clip_name, xl.SiteID): # make sure they're all there before processing
    print filename, site_id
    if os.path.exists('./{}.mp4'.format(filename)):
        window_video(filename, site_id, test_dir)


# vids are smaller b4 fffmpeg???










junk = './processing_RD/GLBA15-1069/GLBA15-1069/DVR150910_1636_001clip_1.mp4'
subprocess.call(('ffmpeg -i {0} -vf scale=960:540'
                ' {0}').format(junk))


count = 0
for root, dirs, files in os.walk('.'):
    for f in files:
        if '.mp4' in f:
            print f
            count+=1







def window_video(fn='test', site='superior', where='./test'):
    out = '{0}/{1}'.format(where, site)
    if not os.path.exists(out):
        os.mkdir(out)
    video = VideoFileClip('{}.mp4'.format(fn), audio=False)
    num_windows = int(round((video.duration/15),0))
    end = round(video.duration % 15,1) # return remainder
    clip_window_times = zip(range(0, 240, 15),range(15, 255, 15)) #max_len 4 min
    for idx, seconds in enumerate(clip_window_times[:num_windows]):
        start = seconds[0]
        stop = seconds[1]
        if idx == num_windows-1:
            stop = start + end
        clip = video.subclip(start,stop)
        return clip
    
        clip.write_videofile('{0}/{1}_{2}.mp4'.format(out, fn, (idx+1)))



def make_windows(video, win_len=15)
    num_windows = int(round((video.duration/win_len),0))
    end = round(video.duration % 15,1) # return remainder
    clip_window_times = zip(range(0, 240, win_len),range(15, 255, win_len)) #max_len 4 min
