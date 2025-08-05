---
title: "Gobber: Voice-Assistant Robot"
author: "Tristan Itoh"
description: "A robotic voice-assistant with an animated face and computer functions."
created_at: "2024-06-11"
---
### Total Time Spent: 14.5 Hours
# Journal

## Day 1 - June 14
I've been wanting to make this project for a while but never fully commited to it. Now is the time. <br>

I started by deciding its functions. Most voice assistants, like Alexa, are basically just microphones and speakers that look stuff up. I want mine to use AI, have animated facial expressions, and have the ability to actually control stuff on my computer. All of this will not only make it fun to use, but actually give it useful abilities. For example, if you want to go to a website, it will open it for you.<br>

Most of my cad designs are usually pretty simple so I wanted to try something else for this. I want soemthing curvy and sleep. Kind of futuristic looking. After trying to make a design in Fusion360, realizing it sucks, and deleting it, I just drew what I want it to look like.

![speaker bot](https://github.com/user-attachments/assets/cdd61c4a-07e6-4ede-8184-26e941a65af8)

It's sort of like a pyramid made of of spheres, with curved walls between them, and a flat face. It will have a circular display with a blue led circle around the display. It's supposed to look unique and futuristic, but still practical. <br>

I used AI to brainstorm the parts I'll need for this. Here is what I decided:
- **ESP32 N16R8:** Main microcontroller, cheap, powerful, all pins I need
- **INMP441:** Microphone, I2S
- **MAX98357A:** Audio amplifier, I2S, works with speaker
- **Speaker:** IDK what it is, 4 ohm, 3W
- **GC9A01:** Display, round, 240x240, 1.28in

Then I planned out the wiring (sort of):
![wire diagram voice box](https://github.com/user-attachments/assets/1ede8be1-999b-496e-9583-1067299c3f0a)

And that's pretty much most of the planning done. All I need to do next:
- Create basic CAD model
- Complete wiring diagram
- Create some code
- Create face animations
### Total Session Time: 3 Hours

## Day 2 - June 16
I had some spare time, but didn't want to do anything big, so I made some animations for the face display!<br>
![look](https://github.com/user-attachments/assets/466af7c2-ba65-4422-b91c-47d8f9b18275)
![blink](https://github.com/user-attachments/assets/50b4fca7-f5b4-456d-83e2-485f1c379eeb)
![smile](https://github.com/user-attachments/assets/9b58a69f-6c5d-4c94-a00c-a0e9838cd946)<br>
Here are they. The gifs dont loop so you might have missed them. I'm not sure if im going to keep these animations in the future. Who knows, maybe i'll come up with a whole different style I'll want it to be in.<br>
![smile](https://github.com/user-attachments/assets/4df7413a-0db5-4f29-92ed-d085e339997b)
![look](https://github.com/user-attachments/assets/6197b0e1-8045-48bf-9956-d66add271f00)
![blink](https://github.com/user-attachments/assets/cc569052-dd62-488b-8548-2fd44cfd2efc)<br>
### Total Session Time: 1.5 Hours

## Day 3 and 4 - June 21/22
Alright now I've started working on the code. For now its just the computer side with the AI. I coded it fairly quickly, using Gemini, ElevenLabs, and OpenAI Whisper. I was using a diffent text to speech but it sounded kind of bad so I switched to the more realistic ElevenLabs. Only problem is the 10k characters a month limit. I'll break down what each thing does now:
- Gemini - AI LLM, get text from Whisper and put it through gemini + a default prompt included in all of them, telling it its role.
- OpenAI Whisper - Recieve mp3 files and convert them to text very accurately
- ElevenLabs - Convert gemini response to mp3 with realistic voice (currently a pirate)<br>
Then at the very end, save it to an mp3 file.<br>

So now that that part is out of the way, if i break down the to-do list more:
- Create basic CAD model
- Complete wiring diagram
- Create basic framwork for esp32 code
- Create rest of face animations

Oh yeah and i accidentally published the code with all the keys in it. tried to fix it with .env and gitignore but didnt work and gave up and just made it private...
### Total Session Time: 4 Hours

## Day 5 (Part 1) - July 30
It's been a while...<br>

I've kind of forgot to journal after Undercity. But I haven't made much progress over that time anyways. I've been working on the CAD and BOM. Both are pretty much finished, but I still need to tweak the CAD a little bit to fit the display properly, and then actually put models of all the electronics in it. I also finished the wiring diagram. I don't have much time so I also just gave up on more face animations. The one's I already made will work fine, but more would have been nice. The only exceptions were that I did make animations for opening mouth, talking, and closing mouth. I'm gonna do a quick dump of everything below, and continue after:<br>
<img width="1280" height="720" alt="wire diagram voice box (1)" src="https://github.com/user-attachments/assets/d227a3bd-3cae-4722-b931-08857496345e" />
![closeMouth](https://github.com/user-attachments/assets/6b78dafd-0615-43e8-9070-187b586e8477)
![openMouth](https://github.com/user-attachments/assets/d07998ca-b248-4012-ad98-396487e262b7)
![talk](https://github.com/user-attachments/assets/5a49ec37-dcd3-4fe5-8118-2d938bb1b883)
![talkloop](https://github.com/user-attachments/assets/72496ca6-d121-48d7-be71-285fe4da7b19)
<br>
**Now what's left:**
- Finish CAD
- Create basic framework for esp32 code

## Day 5 (Part 2) - July 30

Ok, ESP code is done. It's all AI generated but whatever, it's not like I can actually test it yet. Now just some final touches on the CAD.

### Total Session Time (Part 1 and 2): 4 Hours

## Day 6 - July 31

Ok, so its literally the last day to submit. But I finished the CAD!! Here are some design choices I made:
- Split into a top and bottom part with pegs that fit together
- Holes for the microphone and speaker, with that one circle design so its not complete holes
- More specific spots for stuff inside of it, initially I was planning to just randomly cram everything into it
- Hole for USB-c
- An antenna on top, no real reason, it just looks good
<br>
Now that the project is finally done, I just need to get the submission ready and post it!
<img width="878" height="957" alt="Screenshot 2025-07-31 183926" src="https://github.com/user-attachments/assets/4899ea7f-9881-49e8-a800-f6f7a52c6641" />
<img width="1245" height="629" alt="Screenshot 2025-08-04 182248" src="https://github.com/user-attachments/assets/151c78fe-5ea2-4387-bea5-3095bf167230" />

### Total Session Time: 2 Hours
