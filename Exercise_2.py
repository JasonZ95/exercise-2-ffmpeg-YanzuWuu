import os
import subprocess
import queue



def convert_video(path):
    files= os.listdir(path)
    q = queue.Queue()
    i = 1
    for file in files:
        q.put(file)
    while not q.empty():
        x = subprocess.call('ffmpeg -i /Users/y/PycharmProjects/ec500/in/' + q.get() + ' -b 2M -r 30 -s 1280x720 -c:a copy'+' /Users/y/PycharmProjects/ec500/out/30fps+2Mbps+720p_'+str(i)+'.mp4', shell=True)
        print(x)
        # y = subprocess.call('ffmpeg -i /Users/y/PycharmProjects/ec500/in/' + q.get() + ' -b 1M -r 30 -s 720x480 -c:a copy'+' /Users/y/PycharmProjects/ec500/out/30fps+1Mbps+480p_'+str(i)+'.mp4', shell=True)
        # print(y)
        i += 1
        q.task_done()
        q.join()
    print(str(i) +' videos have been transferred ')

convert_video('/Users/y/PycharmProjects/ec500/in')
