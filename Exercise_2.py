import os
import subprocess
import queue
import asyncio
import time
import pytest

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
                subprocess.call('ffmpeg -i ' +path + '/in/' + video + ' -b 2M -r 30 -s 1280x720 -c:a copy '+path+'/out/720_'+video+str(i)+'.mp4', shell=True)
                return '720p videos all transeferred'
            except:
                return 'transfer failed'
        async def transfer_480p():
            try:
                subprocess.call('ffmpeg -i '+ path + '/in/' + video +' -b 1M -r 30 -s 720x480 -c:a copy '+path+'/out/480_'+video+str(i)+'.mp4', shell=True)
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
#                 subprocess.call('ffmpeg -i ' +path + '/in/' + video + ' -b 2M -r 30 -s 1280x720 -c:a copy '+path+'/out/720_'+video+str(i)+'.mp4', shell=True)
#                 return '720p videos all transeferred'
#             except:
#                 return 'transfer failed'
#         async def transfer_480p():
#             try:
#                 subprocess.call('ffmpeg -i '+ path + '/in/' + video +' -b 1M -r 30 -s 720x480 -c:a copy '+path+'/out/480_'+video+str(i)+'.mp4', shell=True)
#                 return '480p videos all transeferred'
#             except:
#                 return 'transfer failed'
#
#         tasks = [asyncio.ensure_future(transfer_720p()),asyncio.ensure_future(transfer_480p()),]
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(asyncio.wait(tasks))
#
#         for task in tasks:
#             print('Task: ', task.result())
#         i += 1
#         q.task_done()
#         # q.join()
#     print(str(i-1) +' videos have been transferred into 720p and 480p type')

def main():
    start = time.clock()
    path = os.getcwd()
    convert_video(path)
    elapsed = time.clock()-start
    print("Time used:",elapsed)


if __name__=='__main__':
    main()
