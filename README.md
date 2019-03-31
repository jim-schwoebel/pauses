# pauses

Quick library to extract pause lengths from audio files. 

## how to get started

I have a readme in the doc, but I'd suggest if you use this to use a mac computer and install all dependencies by going into the folder (in terminal) and then type:

```
git clone git@github.com:jim-schwoebel/pauses.git
cd pauses 
pip3 install -r requirements.txt
```
## if you want to calculated pauses in the ./data folder.
After this, you can run the script in the terminal with:
```
python3 extract_pauselength.py n y
```
## recording files and calculating pauses in real-time

If you want to record a file you can do this by: 
```
python3 extract_pauselength.py y n
```
After you record it it will display the pause length and create a .JSON file. 

## process audio files in ./data folder and record an audio file

If you want to both record a file (10 seconds) and process all the files in the ./data director you can run 

```python3 extract_pauselength.py y y```

This is just following the sys.argv[] convention to pass through variables in the terminal.

## how pauses are calculated 

To simplify things a bit, I recorded a few files (attached) that I could use for reference - slow, moderate, moderate-fast, and fast speaking (reading the constitution of the US). 

I then used pydub to segment based on a threshold of 50 milleseconds segments and -32 dBFS (to allow for detection of fast speaking events) as a silence interval. This parameter likely needs to be tuned to the dataset and speaker power, etc. and is likely overfitted to my voice. Nonetheless, this gives a proof-of-concept implementation of how to segment speaking segments from non-speaking segments with a threshold. I then calculated pause length as total duration (seconds) over the counted number of segments (e.g. number of pauses) - to get a sec/pause.

