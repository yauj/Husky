# x32-scripts
Custom scripts for X32

Run the following: `python3 __main__.py`

For Macs, just open `X32Helper.app`.

## Data Directory

Data directory contains files that are created and used by this program. The directory has the following types of files:

*Note that for both file formats, the first line is not read by the program.*

### osc

These contain osc commands in the following format:

```
[foh|iem] [command] [argument] [str|int|float]
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

## Dependencies:

- [python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [python-osc](https://pypi.org/project/python-osc/)
- [mido](https://mido.readthedocs.io/en/latest/installing.html)
- [PyQt6](https://pypi.org/project/PyQt6/)

GP Seattle Specific: IAC Driver needs to be enabled in 'Audio Midi Setup'

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