import os
import subprocess
import queue
import asyncio
import time


def convert_video():
    path = os.getcwd()+'/'
    print(path)
    files= os.listdir(path)
    q = queue.Queue()
    i = 1
    for file in files:
        if file =='11.mp4' :
            print(file)
            q.put(file)
        elif file =='22.mp4':
            print(file)
            q.put(file)
    while not q.empty():
        video = q.get()

        async def transfer_720p():
            try:
                subprocess.call('ffmpeg -i ' + path + video + ' -b 2M -r 30 -s 1280x720 -c:a copy '+path+'/720_'+video, shell=True)
                return '720p videos all transeferred'
            except Exception:
                return 'transfer failed'

        async def transfer_480p():
            try:
                subprocess.call('ffmpeg -i ' + path + video + ' -b 1M -r 30 -s 720x480 -c:a copy ' + path + '/480_'+video, shell=True)
                return '480p videos all transeferred'
            except Exception:
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



def main():

    start = time.clock()
    convert_video()
    # test_name(path)
    # test_duration()
    elapsed = time.clock()-start
    print("Time used:",elapsed)


if __name__=='__main__':
    main()
