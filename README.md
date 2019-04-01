# pauses

Quick library to extract pause lengths from audio files. 

![](https://media.giphy.com/media/l0HlKrB02QY0f1mbm/giphy.gif)

## How to get started

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

## Technique #1 - thresholding 

The extract_pauselength.py script uses sys.argv[] convention to pass through variables in the terminal. For more information on this, check out this [StackOverflow post](https://stackoverflow.com/questions/4117530/sys-argv1-meaning-in-script).

### assumptions 

To simplify things a bit, I recorded a few files that I could use for reference (in ./data folder) - slow, moderate, moderate-fast, and fast speaking (reading the constitution of the US). 

I then used pydub to segment based on a threshold of 50 milleseconds segments and -32 dBFS (to allow for detection of fast speaking events) as a silence interval. This parameter likely needs to be tuned to the dataset and speaker power, etc. and is likely overfitted to my voice. Nonetheless, this gives a proof-of-concept implementation of how to segment speaking segments from non-speaking segments with a threshold. I then calculated pause length as total duration (seconds) over the counted number of segments (e.g. number of pauses) - to get a sec/pause.

### if you want to process all audio files in the ./data folder 

Run the script in the terminal with:

```
python3 extract_pauselength.py n y
```

### recording voice files and calculating pauses in real-time

If you want to record a file you can do this by: 

```
python3 extract_pauselength.py y n
```

After you record it it will display the pause length and create a .JSON file. 

### process audio files in ./data folder and record an audio file in real time together

If you want to both record a file (10 seconds) and process all the files in the ./data director you can run 

```
python3 extract_pauselength.py y y
```

## Technique #2 - machine learning classification 

Another technique that can be used is to train a machine learning model to detect pause lengths. In this case, I trained a quick machine learning model from 5-6 files separating the files into 20 millisecond windows and labeling each one as a 'pause' or a 'speech' event. I used the [train_audioTPOT.py script](https://github.com/jim-schwoebel/voicebook/blob/master/chapter_4_modeling/train_audioTPOT.py) found in the voicebook repository with the [librosa feature embedding](https://github.com/jim-schwoebel/voicebook/blob/master/chapter_3_featurization/librosa_features.py) (librosa_features.py). The model achieves around 91.22807017543859% accuracy with an optimized SVM model. 

To run this script, you must first put some files in the load_dir folder when you clone the repository (e.g. 'fast.wav'). 

Next, run the script:
```
python3 extract_pauselengths2.py
```

The audio files in ./load_dir are then spliced into 20 millisecond segments and classified as silence or speech events. What results is a file in the ./load_dir that corresponds with the speech file (e.g. fast.wav --> fast.json) with the following information:

```
{"filename": "fast.wav", "total_length": 1.0, "mean": 0.4, "std": 0.20000000000000007, "max_value": 0.6000000000000001, "min_pause": 0.2, "median": 0.4}
```

As you can see, you get a bit more information here. Note this was a proof-of-concept and likely needs to be augmented with other datasets for it to work robustly across speakers. 

## Limitations

Both scripts are limited to low-noise environments. If there is a lot of background noise in your file, I'd first suggest cleaning them and removing noise (e.g. with SoX) before using this script to calculate pause lengths.

## Additional reading
* [pydub](https://github.com/jiaaro/pydub)
* [sox](http://sox.sourceforge.net/)
* [FFmpeg](https://ffmpeg.org/)
