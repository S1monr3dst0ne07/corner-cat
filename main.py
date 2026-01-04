
import wave
import subprocess
import os
import random
import sys
import numpy as np
import cv2

audio = wave.open(sys.argv[1], 'rb') 

target_fps = 30
stills = 'stills'

samples_per_sec = audio.getframerate()
samples_per_frame = samples_per_sec // target_fps

#resample audio
abs_samples = []
while True:
    raw_sub_samples = audio.readframes(samples_per_frame)
    if len(raw_sub_samples) == 0: break
    abs_sub_samples = np.abs(np.frombuffer(raw_sub_samples, dtype="<h"))
    abs_samples.append(np.average(abs_sub_samples))

#normalize
samples = abs_samples / np.max(abs_samples)

#parse images
pics = [os.path.join(stills, x) for x in os.listdir(stills) if x.split('.')[1] == 'png']
downscale = 4
dsize = (1080 // downscale, 1920 // downscale)
data = [
        (
            cv2.resize(cv2.imread(x, cv2.IMREAD_UNCHANGED), dsize),
            x
        ) for x in pics]
base  = [pic for pic, path in data if 'base'  in path]
speak = [pic for pic, path in data if 'speak' in path]

get_base  = lambda: random.choice(base)
get_speak = lambda: random.choice(speak)


#rendering
pic = get_base()
cooldown = 0
old = False



p = subprocess.Popen(f"ffmpeg -y -framerate {target_fps} -f rawvideo -pix_fmt rgba -s {dsize[0]}x{dsize[1]} -i - -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -auto-alt-ref 0 output.webm".split(' '), stdin=subprocess.PIPE, stdout=sys.stdout)

print(p)

for i, sample in enumerate(samples):
    if cooldown > 0:  cooldown -= 1
    if abs(sample) > 0.1: cooldown = 5

    new = cooldown > 0
    if new != old: #edge detection
        pic = get_speak() if new else get_base()
            
    old = new

    p.stdin.write(pic.tobytes())
    p.stdin.flush()

    
        

