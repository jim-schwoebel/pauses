# pauses

Quick library to extract pause lengths from audio files. 

![](https://media.giphy.com/media/l0HlKrB02QY0f1mbm/giphy.gif)

## how to get started

I'm assuming you are running this on a Mac computer (this is the only operating system tested).

First, make sure you have installed Python3, FFmpeg, and SoX via [Homebrew](https://brew.sh/):

```
brew install python3 sox ffmpeg
```

Now, clone the repository and install all require dependencies:

```
git clone git@github.com:jim-schwoebel/pauses.git
cd pauses 
pip3 install -r requirements.txt
```

## use cases 
### if you want to calculate pauses in the ./data folder.
After this, you can run the script in the terminal with:
```
python3 extract_pauselength.py n y
```
### recording files and calculating pauses in real-time

If you want to record a file you can do this by: 
```
python3 extract_pauselength.py y n
```
After you record it it will display the pause length and create a .JSON file. 

### process audio files in ./data folder and record an audio file in real time together

If you want to both record a file (10 seconds) and process all the files in the ./data director you can run 

```python3 extract_pauselength.py y y```

This is just following the sys.argv[] convention to pass through variables in the terminal.

## how pauses are calculated 

To simplify things a bit, I recorded a few files that I could use for reference (in ./data folder) - slow, moderate, moderate-fast, and fast speaking (reading the constitution of the US). 

I then used pydub to segment based on a threshold of 50 milleseconds segments and -32 dBFS (to allow for detection of fast speaking events) as a silence interval. This parameter likely needs to be tuned to the dataset and speaker power, etc. and is likely overfitted to my voice. Nonetheless, this gives a proof-of-concept implementation of how to segment speaking segments from non-speaking segments with a threshold. I then calculated pause length as total duration (seconds) over the counted number of segments (e.g. number of pauses) - to get a sec/pause.

## additional reading
* [pydub](https://github.com/jiaaro/pydub)
* [sox](http://sox.sourceforge.net/)
* [FFmpeg](https://ffmpeg.org/)
