# x32-scripts
Custom scripts for X32

Modify `X32_IP_ADDRESS` in the config.py file to match the IP Address of your X32 mixer.

## busSaveLoad

Directory with scripts to save and load scenes, that contain sends on fader settings for a bus.

Modify `BUSES` in the constants.py file to match the buses you are targeting to save down.

Modify `CHANNELS` in the constants.py file to match the channels you are targeting to save down.

It is recommended that you run these scripts when you are in this directory.

### saveScene.py

Save down current settings for specified buses.

### loadScene.py

Loads up settings for specified buses.

# Dependencies:

- [python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [python-osc](https://pypi.org/project/python-osc/)

## For Mac run the following commands:

Install Homebrew: https://brew.sh

Then after completing the post completion steps of homebrew:

```
brew install git
brew install python
python3 -m ensurepip --upgrade
pip3 install python-osc
```

Then run scripts using the following `python3 <script name>`

# X32 OSC Commands Reference File

[pdf](https://wiki.munichmakerlab.de/images/1/17/UNOFFICIAL_X32_OSC_REMOTE_PROTOCOL_%281%29.pdf)