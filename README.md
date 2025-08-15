# Gobber: Voice Assistant Robot 
A voice assistant robot that listens to requests and responds, powered by Gemini and OpenAI Whisper, all with custom animations to give it a personality.

## Why?
I've been wanting to make this project for a while but never fully commited to it. Now I finally have the opportunity to. The project is inspired by voice assistants on mobile devices, like Siri, but with a physical body and animated face.

## Overview:
This robot uses a combination of hardware, software, and firmware:

### Hardware: 
Controlled by an ESP32-S3 that will be plugged into the computer, recieves input from the microphone, and outputs audio through the audio amp and speaker.
### Firmware: 
Basic code for the ESP32 as sort of a gate between the hardware and the Python software on the computer. Audio in, audio out.
### Software: 
Recieves mp3 files of input audio, translates it to text using OpenAI whisper, passes it into Gemini with context, then finally generates text-to-speech using ElevenLabs with a goofy voice.
### CAD: 
Very smooth, curvy, triangular shape. Round display centered on the front, with holes for USB-c, microphone, and speaker.
<br>

<img width="1051" height="950" alt="Screenshot 2025-07-31 185853" src="https://github.com/user-attachments/assets/b8ddd656-c2fc-4fae-9815-ac807235c0cb" />
<img width="990" height="1079" alt="Screenshot 2025-07-31 195330" src="https://github.com/user-attachments/assets/282c9ee6-6aba-4059-9938-6b4f43bbb64a" />

## Wiring Diagram:
<img width="1280" height="720" alt="wire diagram voice box (2)" src="https://github.com/user-attachments/assets/78431c7c-97ca-4379-861a-5b4573f17bc5" />


## BOM
| Item             | Description                          | Amount | Total Cost         |
|------------------|--------------------------------------|--------|---------------------|
| Round Display    | 1.28" TFT LCD GC9A01                 | 1      | $3.80               |
| Microphone Module| I2S INMP441 Microphone               | 1      | 0 (Already Have)    |
| Speaker Module   | 4 ohm 3 watt                         | 1      | 0 (Already Have)    |
| Audio Amp        | MAX98357A Audio Amplifier Module     | 1      | 0 (Already Have)    |
| ESP32 S3         | N16R8                                | 1      | $6.60               |
| USB-C Cable      | For power and programming            | 1      | 0 (Already Have)    |
| Jumper Wires     |                                      | ~20    | 0 (Already Have)    |
| Breadboard       | For prototyping                      | 1      | 0 (Already Have)    |
**Total:** **$10.40**          

[Sheet With Links](https://docs.google.com/spreadsheets/d/1rEzeNBBt6LBTQF6fnU12Dy_3lUBRjMwdXFT9IxuN5R0/edit?usp=sharing)

## Finished Build + Demo

Here's how the finished Gobber looks:

![20250807_200212](https://github.com/user-attachments/assets/8b94d14d-94f2-4141-b8c1-8881c712ef32)
![20250807_200219](https://github.com/user-attachments/assets/fe7ad15e-20eb-4828-9923-f1417954aa83)

And a video of it working:
[https://www.reddit.com/r/esp32/comments/1mkkhbk/made_my_own_voice_assistant_with_gemini/](https://www.reddit.com/r/esp32/comments/1mkkhbk/made_my_own_voice_assistant_with_gemini/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)
