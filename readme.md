# All scripts were written and tested under:

Operating system: Linux, Ubuntu  
kernel version  : 5.13.0-21-generic  
Ubuntu Release  : 12.10  
Ubuntu Codename : impish  
Python version  : 3.9.7  
pip3 version    : 20.3.4

<br>


# Task 3.
## I wanted to use speech recognition packages. To do that:
<br>

## All following pip3 commands will install the packages in the running folder. 
<br>


## 1. Install `pyttsx3`. Used for text-to-speech conversion.
```
pip3 install pyttsx3 --target . --upgrade
```

Folders that get created:
- pyttsx3
- pyttsx3-2.90.dist-info

<hr><br>


## 2. Install the popular `speech_recognition` package. 
```
pip3 install SpeechRecognition --target . --upgrade
```
Folders that get created:

- speech_recognition
- SpeechRecognition-3.8.1.dist-info

<hr><br>


### 3. Install pyaudio. (For Windows, this process is different)
If we try to install pyaudio with `pip3 install pyaudio`, most probably, we will see that the installation fails. 
(First error will be that `portaudio.h` file will is missing from the target system/environment)

This `portaudio.h` header is part of portaudio, an open-source cross-platform audio API. To install portaudio on linux, the simplest way would be to run a command like the following:
```
sudo apt-get install portaudio19-dev python3-pyaudio
```
You can try the above command. When I developed this however, instead of running the above command, I built `portaudio` from source. The steps to do that were as follows:

a) 
Download portaudio from http://files.portaudio.com/download.html
At the time of writing this, the "pa_stable_v190700_20210406.tgz" file was recommended. It is included in this folder. I extracted the tgz file and cd into the `portaudio` folder that was created. Then I run those: 
```
tar -zxvf pa_stable_v190700_20210406.tgz
cd portaudio
./configure
make
sudo make install
sudo ldconfig
```


These are the files that were installed on my system:
```
/usr/local/lib/libportaudio.a
/usr/local/lib/libportaudio.la
/usr/local/lib/libportaudio.so
/usr/local/lib/libportaudio.so.2
/usr/local/lib/libportaudio.so.2.0.0
/usr/local/include/portaudio.h
./lib/x86_64-linux-gnu/libportaudio.so.2.0.0
./lib/x86_64-linux-gnu/libportaudio.so.2
./lib/x86_64-linux-gnu/libportaudiocpp.so.0
./lib/x86_64-linux-gnu/libportaudiocpp.so.0.0.12
./local/lib/pkgconfig/portaudio-2.0.pc
./share/doc/libportaudio2
./share/doc/libportaudiocpp0
```

Then I went ahead and installed pyaudio
```
pip3 install --target . --upgrade PyAudio
```
Files and folders that got created:
- portaudio 
- _portaudio.cpython-39-x86_64-linux-gnu.so
- pyaudio.py  
- PyAudio-0.2.11.dist-info

<hr><br>


## 4. I thought I was done at this moment, but nope. Last step: library espeak
After having done all of the above, I tried running a test script to see if everything was working. I could play wav files but not use input from the microphone. More specifically, this was the error when trying to use microphone as input:
```
OSError: libespeak.so.1: cannot open shared object file: No such file or directory
```

This happens because pyttsx3 uses the espeak driver by default. To install that one, I run this command:
```
sudo apt install libespeak-dev
```
Note: that espeak library is used to manage the Voice Object in task3. I tried using a different voice (like greek e.g.) but could not do it.

## How to run

Run `python3 server.py` and on a new terminal run `python3 client.py`. 
You can see all available questions by opening the `questions_answers_db` file.
