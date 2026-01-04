# Corner Cat
Corner cat is a simple characters-still talking overlay engine.
For a given audio file in Wave format, it generates a simple
WebM overlay video which can make recorded speak feel more animated.
It resamples input audio to match video frame rate, does speech edge detection
and chooses an appropriate image to match the speech.

## Usage
Base images for non-speech, in the form `base*.png` and speak image for speech,
in the form `speak*.png` are place in the `stills/` directory.
The asterisk `*` stands for any sequence of characters.
``` bash
python3 main.py input.wav
```
From this `output.webm` will be generated.
Note: This depends on FFmpeg.

