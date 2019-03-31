'''
extract_pauselength.

A rather elaborate script to clean an audio file and extract a pause length.

Relies on SoX, FFMPEG, and assumes an OSX computer.

To run the script, you must first install all libraries with 
pip3 install -r requirements.txt

Then, you must have homebrew and install ffmpeg and sox with
`brew install ffmpeg`
`brew install sox`

Then you can create a data folder and put everything in there. 
'''

import os, pocketsphinx, librosa, re, json, shutil
import speech_recognition as sr_audio
from pydub import AudioSegment
from pydub.silence import split_on_silence
import sounddevice as sd
import soundfile as sf 

# transcribe with pocketsphinx (open-source)
# def transcribe_google(file):
#     r=sr_audio.Recognizer()
#     with sr_audio.AudioFile(file) as source:
#         audio = r.record(source) 
#     transcript=r.recognize_google()
#     print('google transcript: '+transcript)
    
#     return transcript 

def sync_record(filename, duration, fs, channels):
    print('recording')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, fs)
    print('done recording')

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def remove_silence(input_file, silence_file):
	sound_file = AudioSegment.from_wav(input_file)
	audio_chunks = split_on_silence(sound_file, 
	    # must be silent for at least 100 ms 
	    min_silence_len=50,

	    # consider it silent if quieter than -16 dBFS
	    silence_thresh=-32
	)

	curdir=os.getcwd()
	os.mkdir(input_file[0:-4])
	os.chdir(input_file[0:-4])

	for i, chunk in enumerate(audio_chunks):

	    out_file = "{0}.wav".format(i)
	    print("exporting")
	    print(out_file)
	    chunk.export(out_file, format="wav")

	listdir=os.listdir()
	dirlist = sorted_aphanumeric(listdir)

	# now combine all of these files 
	playlist = [AudioSegment.from_wav(wav_file) for wav_file in dirlist]

	combined = AudioSegment.empty()
	for song in playlist:
	    combined += song

	os.chdir(curdir)
	combined.export(silence_file, format="wav")

	# os.system('sox %s %s'%(input_file, silence_file)+"silence 1 0.1 1% -1 0.1 1%")

	return int(len(dirlist))

def clean_audio(input_file, clean_file):
	# create a noise background from first .50 seconds 
	noise_file=input_file[0:-4]+'_noise.wav'
	# Create noise file from input audio's initial 0.5s 
	os.system('sox %s %s trim 0 0.100'%(input_file, noise_file))
	# Generate a noise profile in sox
	os.system('sox %s -n noiseprof noise.prof'%(noise_file))
	# clean noise from audio 
	os.system('sox %s %s noisered noise.prof 0.21'%(input_file, clean_file))
	# remove temp files 
	os.remove(noise_file)
	os.remove('noise.prof')
	return clean_file
	

def extract_pauselength(input_file):
	# get transcript 
	silence_file=input_file[0:-4]+'_silence'+input_file[-4:]
	clean_file=input_file[0:-4]+'_cleaned'+input_file[-4:]

	# clean the audio from ambient background noise 
	# clean_audio(input_file, clean_file)
	# transcript=transcribe_google(input_file)

	# remove silence 
	pause_number=remove_silence(input_file, silence_file)
	
	# now get duration of silenced vs. unsilenced file 
	y, sr = librosa.load(input_file)
	duration=librosa.get_duration(y=y, sr=sr)

	# delete temp files and folders (optional)
	shutil.rmtree(input_file[0:-4])
	os.remove(silence_file)

	# os.remove(clean_file)

	# now calculate pause lengths by number of files in the remove_silence script 
	try:
		pause_length=duration/pause_number
	except:
		pause_length='error'
	
	return pause_length


os.chdir('data')

if input('Would you like to record an audio file? "y" for yes "n" for no.').lower().replace(' ','') == 'y':
	sync_record('test.wav', 10, 16000, 1)

listdir=os.listdir()
filelist=list()

for i in range(len(listdir)):
	if listdir[i][-4:] in ['.wav', '.mp3', '.m4a']:
		if listdir[i][-4:] != '.wav':
			wavfile=listdir[i][0:-4]+'.wav'
			os.system('ffmpeg -i %s %s'%(listdir[i], wavfile))
			os.remove(listdir[i])
			filelist.append(wavfile)
		else:
			filelist.append(listdir[i])

print(filelist)

for i in range(len(filelist)):
	pause_length = extract_pauselength(filelist[i])
	data={'file': filelist[i],
		  'average pause length (seconds)': pause_length,
		  }
	jsonfile=open(filelist[i][0:-4]+'.json','w')
	json.dump(data,jsonfile)
	jsonfile.close()
	print(data)