---
title: "Gobber: Voice-Assistant Robot"
author: "Tristan Itoh"
description: "A robotic voice-assistant with an animated face and computer functions."
created_at: "2024-06-11"
---
### Total Time Spent: Ongoing
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
