import os
import subprocess
import queue
import asyncio
import time
from pytest import approx
import json
from pathlib import Path


def convert_video(path):
    files= os.listdir(path+'/in/')
    q = queue.Queue()
    i = 1
    for file in files:
        print(file)
        q.put(file)
    while not q.empty():
        video = q.get()
        async def transfer_720p():
            try:
                subprocess.call('ffmpeg -i ' +path + '/in/' + video + ' -b 2M -r 30 -s 1280x720 -c:a copy '+path+'/out/720_'+video, shell=True)
                return '720p videos all transeferred'
            except:
                return 'transfer failed'
        async def transfer_480p():
            try:
                subprocess.call('ffmpeg -i '+ path + '/in/' + video +' -b 1M -r 30 -s 720x480 -c:a copy '+path+'/out/480_'+video, shell=True)
                return '480p videos all transeferred'
            except:
                return 'transfer failed'

        tasks = [asyncio.ensure_future(transfer_720p()),asyncio.ensure_future(transfer_480p()),]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

        for task in tasks:
            print('Task: ', task.result())
        i += 1
        q.task_done()
        # q.join()
    print(str(i-1) +' videos have been transferred into 720p and 480p type')



def ffprobe_sync(filein: Path) -> dict:
    """ get media metadata """
    meta = subprocess.check_output(['ffprobe', '-v', 'warning',
                                	'-print_format', 'json',
                                	'-show_streams',
                                	'-show_format',
                                	str(filein)], universal_newlines = True)
    return json.loads(meta)


def test_duration():
    fnin = 'in\\11.mp4'
    fnin2 = 'in\\22.mp4'
    fnout = 'out\\480_11.mp4'
    fnout2 = 'out\\720_11.mp4'
    fnout3 = 'out\\480_22.mp4'
    fnout4 = 'out\\720_22.mp4'

    orig_meta = ffprobe_sync(fnin)
    orig_duration = float(orig_meta['streams'][0]['duration'])

    meta_480 = ffprobe_sync(fnout)
    duration_480 = float(meta_480['streams'][0]['duration'])
    meta_720 = ffprobe_sync(fnout2)
    duration_720 = float(meta_720['streams'][0]['duration'])

    orig_meta = ffprobe_sync(fnin2)
    orig_duration1 = float(orig_meta['streams'][0]['duration'])

    meta_480 = ffprobe_sync(fnout3)
    duration_480_22 = float(meta_480['streams'][0]['duration'])
    meta_720 = ffprobe_sync(fnout4)
    duration_720_22 = float(meta_720['streams'][0]['duration'])
    assert orig_duration == approx(duration_480) == approx(duration_720)
    assert orig_duration1 == approx(duration_480_22) == approx(duration_720_22)


# def test_name(convert_video):
#     aa=convert_video()
#     assert aa==0

# @pytest.fixture(scope='function')
# def test_convert_video(path):
#     files= os.listdir(path+'/in/')
#     q = queue.Queue()
#     i = 1
#     for file in files:
#         print(file)
#         q.put(file)
#     while not q.empty():
#         video = q.get()
#         async def transfer_720p():
#             try:
#                 subprocess.call('ffmpeg -i ' +path + '/in/' + video + ' -b 2M -r 30 -s 1280x720 -c:a copy '+path+'/out/720_'+video, shell=True)
#                 a= '720p videos all transeferred'
#             except:
#                 a= 'transfer failed'
#             return a
#         async def transfer_480p():
#             try:
#                 subprocess.call('ffmpeg -i '+ path + '/in/' + video +' -b 1M -r 30 -s 720x480 -c:a copy '+path+'/out/480_'+video, shell=True)
#                 a= '480p videos all transeferred'
#             except:
#                 a= 'transfer failed'
#             return a
#
#         tasks = [asyncio.ensure_future(transfer_720p()),asyncio.ensure_future(transfer_480p()),]
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(asyncio.wait(tasks))
#
#         for task in tasks:
#             print('Task: ', task.result())
#
#
#         i += 1
#         q.task_done()
#         # q.join()
#     print(str(i-1) +' videos have been transferred into 720p and 480p type')
#     files_output= os.listdir(path+'/out/')
#     for file in files_output:
#         # print (file)
#         if(os.path.basename(os.path.realpath(__file__))=='720_11.mp4'):
#             filename1 = '720_11.mp4'
#         elif(os.path.basename(os.path.realpath(__file__))=='480_11.mp4'):
#             filename2 = '480_11.mp4'
#         # elif(file == '720_22.mp4'):
#         #     filename3 = '720_22.mp4'
#         # elif(file == '480_22.mp4'):
#         #     filename4 = file == '480_22.mp4'
#     assert filename1== '720_11.mp4'
#     assert filename2== '480_11.mp4'
#     assert filename3== '720_11.mp4'
#     assert filename4== '480_11.mp4'
#     # assert task.result()=='720p videos all transeferred'
#     # assert transfer_720p()=='720p videos all transeferred'
#     # assert transfer_720p()=='480p videos all transeferred'
def main():

    start = time.clock()
    path = os.getcwd()
    convert_video(path)
    # test_name(path)
    test_duration()
    elapsed = time.clock()-start
    print("Time used:",elapsed)


if __name__=='__main__':
    main()
