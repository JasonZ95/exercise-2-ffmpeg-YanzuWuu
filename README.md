# python-CI-template
Python CI template for EC500 Software Engineering

Main method:
==
I use a queue to stpre all the mp4 files stored in the path, and then use two async functions to transefer the video into 480p and 720p seperately, with ffmpeg command ofcourse. Finally use a task array to run the functions.

As for the test file, I store the media metadata and compare its origin and 720/480 version as the judgement factor.

Transfer result:
==

![ex2_result](ex2_result.png)

Process evaluation:
==

![CPU](CPU.png)

My computer's CPU is 2.2 GHz Intel Core i7 with a 16 GB 2400 MHz DDR4 memory. And it costs 2.28% cpu to transfer 2 videos into two versions, totally 4 processes. So each transfer may take (16*2.28%)/4=0.0912GB. And average time each process takes is about 3.5 seconds.

So we can assume that I can transfer (1/2.28%)*4=175.4, which is 175 processes in maximum at one time.
