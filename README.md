# x32-scripts
Custom scripts for X32

Run the following: `python3 __main__.py`

For Macs, just open `X32Helper.app`.

## config.py

This is the file that contains the config for your particular setup. These are the particular settings in the file:

### personal

This is a list of the typical personal that you want to save settings for. For each personal, you can specify `channels` and `iem_bus`. These are the target channel and in ear bus for the particular person. If you leave one blank, then it will not save down the particular settings for that person.

### osc

These are the default IP Addresses for `foh` and `iem` mixers. Note that the port is fixed to connect to 10023, which is the X32 default OSC port.

### serverMidi

This contains the name of the name of the default port to listen to, for incoming MIDI commands to this program.

### midi

These are the default MIDI ports to connect to for each particular category of midi commands. Note that `X32Helper` is a virtual MIDI port that is opened by this application that can be used by all programs on the computer running this app.

#### default

This is the name of the default port to connect to.

#### type

This is the type of midi call to make. Valid options currently are: `control_change` and `note`.

#### defaultChannel

This is the default channel to send midi commands on. Should be a number between 1-16.

### faders

This is a list of default settings to load into the faders. The commands are in the following format:

```
[foh|iem] [command] [min float argument] [max float argument]
```

or for MIDI cues (note that fader only makes sense for control change commands)

```
midi [audio] [channel] [control]
```

On fader change, a corrosponding command will be fired. For OSC commands, this would send a float value between min and max arguement. For MIDI commands, this would send MIDI value equal to the slider position.

### talkbackChannel

This is the channel that FOH talkback is being sent through. Applicable because FOH Talkback Channel is sent to IEM Mixer.

## resetCommands

Commands to be fired on reset call.

## Data Directory

Data directory contains files that are created and used by this program. The directory has the following types of files:

*Note that for both file formats, the first line is not read by the program.*

### osc

These contain osc commands in the following format:

```
[foh|iem] [command] [str|int|float] [argument]
```

You are also able to fire MIDI cues, by putting commands in the following format:

```
midi [audio|video|light] [channel:1-16] [control:0-127] [value:0-127]
```

### cue

This is a file to save down the cues to be files. It contains lines in the following format:

```
[key:A-G] [vocalLead:1-4] [snippet filename]
```

## Shortcuts

### Cues

There are 3 different options to fire cues:

1. Press the "Fire" button next to the cue
2. Use cmd+\<cue number\> to fire that numbered cue (Note that Cue 10 is fired by cmd+0. Also cmd+\<page name\> will change pages)
3. Send a MIDI cue to the X32Helper port, where channel=5, control=\<cue number - 1\> and value=127 (Also, control=10 moves to previous page, control=11 moves to next page and control=12 moves to page specified by \<value\>)

## Dependencies:

- [python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [python-osc](https://pypi.org/project/python-osc/)
- [mido](https://mido.readthedocs.io/en/latest/installing.html)
- [PyQt6](https://pypi.org/project/PyQt6/)

### For Mac run the following commands:

Install Homebrew: https://brew.sh

Then after completing the post completion steps of homebrew:

```
brew install git
brew install python
python3 -m ensurepip --upgrade
pip3 install python-osc
pip3 install mido
pip3 install python-rtmidi
pip3 install PyQt6
```

## X32 OSC Commands Reference File

[pdf](https://wiki.munichmakerlab.de/images/1/17/UNOFFICIAL_X32_OSC_REMOTE_PROTOCOL_%281%29.pdf)