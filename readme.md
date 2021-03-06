## UPDATE: Sometimes the program does not work correctly when dealing with multiple audio sources.
The solution to this is probably to set the input and output devices explicitly.   
This may happen eg. in the client.py file, when the Microphone object is created.   
Also, the speech_recognition package does not provide what I would call a "correct"   
validation of the device index used as input (eg it allows other devices to be used),  
so it would be better if these checks were to happen manually on the client.   
Sample code to get an idea of this:

```
# import pyaudio, either directly or through the speech_recognition module.
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

mic = sr.Microphone(device_index=...)
```

## If you follow the instructions below, you will probably only need the `server.py`, `client.py` and `questions_answers_db` files.

### What this project is about
This project is an answer to the following university task:

You want to create your own Alexa in your computer. As a first step, your AI will be static, thus it will answer only to predefined questions. You want to test your design locally to your pc thus you will use sockets for the communication between the AI and the client. Design and implement two programs, one for the AI which will listen on a specific port for questions and a client which will connect to this port and then it will wait for input from the user.

<hr>
<br>

### All scripts were written and tested under:

Operating system: Linux, Ubuntu  
kernel version  : 5.13.0-21-generic  
Ubuntu Release  : 12.10  
Ubuntu Codename : impish  
Python version  : 3.9.7  
pip3 version    : 20.3.4

<hr>
<br>

### Speech Recognition and Text to Speech
Although not required I wanted to make the program in a way that  
the communication would happen through speech. Below are all the steps  
that I followed in order to achieve that. 

<br>



### 1. Install `pyttsx3`. Used for text-to-speech conversion.
```
pip3 install pyttsx3 --target . --upgrade
```

Folders that get created in our work folder:
- pyttsx3
- pyttsx3-2.90.dist-info

<hr><br>


### 2. Install the popular `speech_recognition` package. 
```
pip3 install SpeechRecognition --target . --upgrade
```
Folders that get created in our work folder:

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
You can try the above command. However, instead of running the above command, I built `portaudio` from source. The steps to do that were as follows:
 
1.  Download portaudio from http://files.portaudio.com/download.html
    At the time of writing this, the "pa_stable_v190700_20210406.tgz" file was recommended. It is included in this folder. I extracted the tgz file and cd into the `portaudio` folder that was created. Then I run those: 
    ```
    tar -zxvf pa_stable_v190700_20210406.tgz
    cd portaudio
    ./configure
    make
    sudo make install
    sudo ldconfig
    ```


    In case you want to undo that, these are the files that were installed on my system:
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

2.  go ahead and install pyaudio
    ```
    pip3 install --target . --upgrade PyAudio
    ```
    Files and folders that get created in our work folder:
    - portaudio 
    - _portaudio.cpython-39-x86_64-linux-gnu.so
    - pyaudio.py  
    - PyAudio-0.2.11.dist-info

<hr><br>


### 4. espeak library
After having done all of the above, I tried running a test script to see if everything was working. I could play wav files but not use input from the microphone. More specifically, this was the error when trying to use microphone as input:
```
OSError: libespeak.so.1: cannot open shared object file: No such file or directory
```

This happens because pyttsx3 uses the espeak driver by default. To install that one, I run this command:
```
sudo apt install libespeak-dev
```
Note: that espeak library is used to manage a Voice Object. If for example  
we would like to change to a Greek voice, we would have to tamper with  
the configuration of this Voice Object.

<hr>
<br>

### 5. How to run

Run `python3 server.py` and on a new terminal run `python3 client.py`. 
You can see all available questions by opening the `questions_answers_db` file.
	
