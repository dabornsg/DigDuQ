## DigDuQ - Testing out Q-Learning with Dig-Dug
This repository will hold everything needed to run an OpenAI's Gym environment that interfaces with a Windows FCEUX emulator running Dig-Dug for NES (unsurprisingly). If you want more details about the project (or less depending on how you view it), check out [this page](https://dabornsg.github.io/) and search for "digdug" by tags.

## Dependencies
You'll need to have the following packages installed on your Python PATH for this to work:
- OpenAI's Gym
- Numpy
- pynput
- Pillow (PIL)

Also bear in mind this will only work for Windows machines, using the FCEUX emulator. You'll need to adapt it to make it run elsewhere, but if you know what you're doing it shouldn't prove to be difficult.

## Running the environment
Before you hit run on the notebook, make sure to have an instance of FCEUX 2.6.4 running on the background, with a Dig-Dug ROM loaded in and paused (as in, paused within the emulator, a red pause icon should appear on the bottom right if it's set up correctly). Also, make sure to have a save state put preferably on the first few frames of the first level, and set your keys ```f, p and k``` to ```button a or b, load save state and FrameAdvance```, respectively.

After that's set up, run the first block in the notebook, and when "Waiting for pipe connection..." prints out, load ```DigDuQ-Interface.lua``` on the emulator and hit start. If everything was done correctly, you should be seeing the emulator in action.

## To Do:
Currently, only the base environment has been written. I'm still creating the Q-Learning agent and all that cool stuff.