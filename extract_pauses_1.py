'''
================================================ 
          PAUSES REPOSITORY                     
================================================ 

repository name: pauses 
repository version: 1.0 
repository link: https://github.com/jim-schwoebel/pauses 
author: Jim Schwoebel 
author contact: js@neurolex.co 
description: 🎤 quick library to extract pause lengths from audio files. 
license category: opensource 
license: Apache 2.0 license 
organization name: NeuroLex Laboratories, Inc. 
location: Seattle, WA 
website: https://neurolex.ai 
release date: 2019-04-01 

This code (pauses) is hereby released under a Apache 2.0 license license. 

For more information, check out the license terms below. 

================================================ 
                LICENSE TERMS                      
================================================ 

Copyright 2019 NeuroLex Laboratories, Inc. 
Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at 

     http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and 
limitations under the License. 

================================================ 
                SERVICE STATEMENT                    
================================================ 

If you are using the code written for a larger project, we are 
happy to consult with you and help you with deployment. Our team 
has >10 world experts in Kafka distributed architectures, microservices 
built on top of Node.js / Python / Docker, and applying machine learning to 
model speech and text data. 

We have helped a wide variety of enterprises - small businesses, 
researchers, enterprises, and/or independent developers. 

If you would like to work with us let us know @ develop@neurolex.co. 

================================================ 
                DESCRIPTION                   
================================================ 

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
from pydub import AudioSegment
from pydub.silence import split_on_silence
import sounddevice as sd
import soundfile as sf 
import sys, datetime

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
	    # must be silent for at least 50 ms 
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

	# optionally, clean the audio from ambient background noise 
	# clean_audio(input_file, clean_file)

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

record=sys.argv[1]
folder=sys.argv[2]

print(record)
print(folder)

filelist=list()
if record == 'y':
	filename='test-%s.wav'%(str(datetime.datetime.now()))
	sync_record(filename, 10, 16000, 1)
	filelist.append(filename)
	if folder=='y':
		shutil.move(os.getcwd()+'/'+filename, './data/'+filename)
	else:
		pause_length = extract_pauselength(filename)
		data={'file': filename,
			  'average pause length (seconds)': pause_length,
			  }
		jsonfile=open(filename[0:-4]+'.json','w')
		json.dump(data,jsonfile)
		jsonfile.close()
		print(data)

if folder=='y':
	os.chdir('data')
	listdir=os.listdir()
	
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

