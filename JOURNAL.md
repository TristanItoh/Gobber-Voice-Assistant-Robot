---
title: "Gobber: Voice-Assistant Robot"
author: "Tristan Itoh"
description: "A robotic voice-assistant with an animated face and computer functions."
created_at: "2024-06-11"
---
### Total Time Spent: 14.5 Hours
### Total Build Time Spent: ~10 Hours
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

I've kind of forgot to journal after Undercity. But I haven't made much progress over that time anyways. I've been working on the CAD and BOM. To make it smooth and curvy I made the initial shape in Womp:
<img width="698" height="585" alt="Screenshot 2025-08-04 182659" src="https://github.com/user-attachments/assets/1923a179-45ba-41a0-bd12-91dedf9cf109" /><Br>
I made it into a pyramid using AI to make sure its a perfect shape, then adjusted the levels in Womp to make the curves between them look how I was hoping. After I got it into that nice curvy pyramid, I imported it into Tinkercad to do all the small stuff (like putting electronics in it). Both the CAD and BOM are pretty much finished, but I still need to tweak the CAD a little bit to fit the display properly, and then actually put models of all the electronics in it. I also finished the wiring diagram. I don't have much time so I also just gave up on more face animations. The one's I already made will work fine, but more would have been nice. The only exceptions were that I did make animations for opening mouth, talking, and closing mouth. I'm gonna do a quick dump of everything below, and continue after:<br>
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

Ok, so its literally the last day to submit. But I finished the CAD!! I took measurements of the electronic components I was using and remade then in CAD and placed them into my robot. I made sure they would all fit well, added small tolerances, and even added some slots in the bottom to put the esp32 and breadboard. Here are some design choices I made:
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

# Assembly:

## Day 7 - August 4

I'm going to split the assembly into a few parts just to make it less complex. 
1. Speaker
2. Microphone
3. Display
   
I'll slowly like implement them together so that it will eventually become the finished build. 
### Speaker
So we're starting with the speaker. I soldered the speaker to te audio amp, and the audio amp to the esp32 according to the wiring diagram. Afterwards, I plugged it into my computer to try to program it. Since i already got the code before to work where it can take create mp3s from Gemini and Elevenlabs, I basically had it set up already. The main thing I had to do was program the esp32 to work with it. After a little research, I discovered it's better to play audio as .wav rather than .mp3s, so I switched the Python code to do that. Then I dilly dallyd with chatgpt to try to get the esp32 code to work. For a little bit, I couldn't figure out why it wasn't playing anything. Then I finally realizing I was making such an obvious mistake. The pinout from chatgpt wasn't the same as mine. And not so surprisingly, after i switched the numbers, it actually started to work! At least sort of... It was trying to play the audio but it was like very slowed down and choppy. This was due to how the esp32 plays the audio as it receives the data through serial. And since it was receiving the data so slowly... you can probably connect the dots. 

I researched how I could make it faster, and the answer was pretty simple: just use wifi. This was a little shocking to me, because i was expecting plugging the esp32 into my computer and sending data to it like that would be the fastest, but i guess if you think about it, wifi is pretty fast. I removed all the serial stuff from my code and switched it to connect to my home wifi and send data that way. After I tested it with wifi, it actually worked, like surprisingly smooth. While it was playing the audio smoothly, though, it was pretty low quality. I tried to fix it in the code by configuring random wifi stuff, but it just wasn't a code issue. It was with the speaker itself. I kind of brainstormed how i could get a better speaker, and i finally settled on just breaking apart an old headset and taking the speaker from it. After I obtained the speaker, i took the old one off and soldered it on. When I tested it with the code again, it was actually perfect. Like it could not get much better. Tomorrow I'll start working on the microphone, maybe even combine the microphone with the speaker.

## Day 8 - August 5

### Microphone Part 1
So... the microphone is not going very smoothly. I guess just to go back to the very start, I attached the microphone to the esp32. While i was doing that, I had the case of the robot printing, so I can hopefully get it all together sometime soon. To test the microphone, I had chatgpt make some basic esp32 code that prints the audio level output of it. Oddly, it wasn't working at first. I double checked the pinout this time, and it was all correct. This time, the issue was different. The microphone was printing outputs, but they were ridiculously high and changing way too fast. There's no way it was correct. But kind of just fiddling with the electronics, I found out if I hold a wire(s) a certain way, it actually started to print reasonable output. It was an issue with the wiring. I'm pretty sure the breadboard I was using had something wrong. Instead, I just directly soldered all the wires together, and when I tested it again, it was actually giving good output. It was pretty cool, because I could see when I talk, the output would go to like 1000-1100 rather than the normal 400-500. It was definitely detecting audio. 

At this point, now that I know the microphone actually works, I switched the code to now instead start recording whatever you say after it gets loud enough, and then send the input back to Python. It worked fairly easily, so i switched it to where it transcribes whatever you say with Whisper to text, and looks for a certain wake word. Since Gobber isn't a real word, I think I used like pineapple or something as the temporary one lol. It technically worked, but it wasn't very good. A lot of times, it thinks I'm saying something else rather than pineapple. I asked AI how I can improve it, and it recommended this API called Porcupine. They had something specifically for detecting wake words, so I installed it into my project, got a key, and tested it. It was kind of like a two in one, because now I can also use it for custom words like Gobber. I had to get a special .ppn file generated from the website for "Gobber" so that it can detect it. After I added the ppn to my files and changed my code to use it, it worked ridiculously well. It actually worked like almost every time. By now, I kind of stopped coding because I was satisfied and it was getting late, but i was able to print both pieces of the shell of the robot. I put all of the electronics into it just to see how it was, and everything fit nicely.

## Day 9 - August 6

### Microphone Part 2
Back to work on the microphone. Now that I got the wake word detection working, I need it to actually get whatever you say after. I managed to do this by just having it start recording for 5 seconds, then sending that through wifi to the Python code. I was able to test it by just opening the prompt.mp3 file that is in the folder. It wasn't too hard to get working, and it was pretty good. Now the easy part came after. I just had to combine that with the existing Python code. I already had the whole system that would take in a wav and create a response wav out of it. All I had to do was just give it that new wav prompt the microphone is recording. But now to do this, I had to combine the microphone code with the speaker code that I combined with the Python. This caused significantly more trouble than I was hoping.. Like A LOT more. 

At first, the speaker just wasn't doing anything. I thought it was a problem with the electronics, but after testing them, it was all fine. I even converted my code back to the speaker only version, and the speaker worked completely fine. Honestly I had no clue what to do. I just fed it into chatgpt over and over again, and I mean it helped sort of, but not much. It fixed the code enough to where it would play a sound out of the microphone, but it was like half a second of audio, then a couple seconds later, another half second, and then after like a couple times it would just stop. It got so tiring trying to fix this. Like I probably spent more time trying to fix this than anything else. And with tomorrow being the last day to submit, I kind of just had to stop for today so I can finish my other project.

## Day 10 - August 7

### Microphone Part 3
I cracked the code!! Metaphorically and I guess literally as well. I remembered I had Cursor, so i just fed all the slop into Gemini 2.5 pro, and after a few revisions, it miraculously... sort of worked? It's actually playing the audio now, and it is clean. At this point, I ran out of Elevenlabs credits, even though I was trying to conserve them, so I just completely switched it to use gTTS. It's a little disappointing cause it doesn't have that goofy pirate voice anymore. And at the same time I just took away the pirate part of the prompt, so its just a normal voice assistant. The audio was nice, but there were still some problems. It would still do the previous problem sometimes, but just way less often. And pretty much everytime it wouldn't finish what it's saying, and cut itself off a little before the end. It's like the debugging was showing that it was disconnecting and reconnecting, but I don't know if that was really the reason. I couldn't look to close into it, because I just quite frankly didn't have much time left. Overall, I'd say the microphone/speaker flow is satisfactory now. I just need to move onto the display.

### Display
I started off by soldering the display to the esp32, again, according to the wiring diagram. It was already snapped into the robot's body so after I attached it, the robot was complete at least physically. It wasn't until I plugged it in, though, that I realized the screen was cracked. No idea if this happened before I got it, while it was sitting there before I used it, or while I was wiring it. The damage didn't look too bad, and the backlight was still turning on, so I moved forward with trying to get it to work. I created a new file for the esp32 code, installed the library for it, put an example piece of code for it in, and.. it did not work. I simplified the code to literally just show a color, and it still didn't work. Then I found the library had a built in example. I changed the pinout to match mine and it still didn't work. I double checked my wiring, and everything should have been correct. I even got my brother that is better with hardware to try getting it to work, and still no luck. So yeah... With the deadline coming up, I think it was like an hour away at the time, I just gave up on it. I polished the code for the speaker and microphone part a little more, refined the prompt, just did a lot of testing. I guess after a bit it just got to the final submission version. So I just recorded a quick demo, asking it "Say 10 random words" and went over how it works. And yeah, that is the end of the journey for now. I am not done with it though!
![20250807_200212](https://github.com/user-attachments/assets/379df01e-0c57-4217-8480-b06dc1e81a98)
![20250807_200219](https://github.com/user-attachments/assets/33878327-1635-4b34-a58b-8d1ba65f1acc)
