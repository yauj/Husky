# Husky

Companion app for X32.

Run the following: `python3 main.py`

For Macs, run `./pyinstller.sh` to create `Husky.app` within the `dist` directory.

## config.py

This is the file that contains the config for your particular setup. These are the particular settings in the file:

### osc

These are the default IP Addresses for `foh` and `iem` mixers. Note that the port is fixed to connect to 10023, which is the X32 default OSC port.

### atemPort

This is the incoming port to [AtemOSC](http://www.atemosc.com). Currently, this only supports a local instance of AtemOSC.

### midi

These are the default MIDI ports to connect to for each particular category of midi commands. Note that `Husky` is a virtual MIDI port that is opened by this application that can be used by all programs on the computer running this app.

#### default

This is the name of the default port to connect to.

#### type

This is the type of midi call to make. Valid options currently are: `cc` and `note`.

#### defaultChannel

This is the default channel to send midi commands on. Should be a number between 1-16.

### serverMidi

These are the MIDI ports to listen to. MIDI commands sent from these sources are able to trigger cue and fader commands. Under `serverMidi` is a dictionary, where the keys are the default souces to listen to and the value of each key is a array of default commands to listen to. The options for each command is:

#### midi

Incoming midi to listen to. Specify `type` (either `Control Change` or `Note`),  the `channel` (number between 1 and 16) and `control` (number between 0 and 127) to listen to.

#### command

Command to trigger if the conditions for a incoming midi is met. Specify `type` (either `Cue` or `Fader`), `page` (page letter or `CURRENT`) and `index` (number between 1-10 for `Cue` and 1-4 for `Fader`). Additionally if `CURRENT` is selected for `page`, there are additional triggers of `Next Page` and `Prev Page` that can be specified in `index`.

### personal

This is a list of the typical personal that you want to save settings for. For each personal, you can specify `channels` and `iem_bus`. These are the target channel and in ear bus for the particular person. If you leave one blank, then it will not save down the particular settings for that person.

### cues

These are the fields related to the cue tab.

Specify `cuePages` to indicate how many pages of cues to have.

Specify `faderPages` to indicate how many pages of faders to have.

#### cueOptions

This contains a dictionary, where the keys are the default columns for the cue page. Under each key, is another dictionary, where the keys are the options for the column and the key is a array of `osc` or `midi` commands in the format specified below in the `osc` file format. A `RESET` option can be specified, which will be triggered when the reset button is clicked.

### faders

This is a list of default settings to load into the faders. The commands are in the following format:

```
[foh|iem] [command] [min float value] [max float value]
```

or for MIDI cues (note that fader only makes sense for control change commands)

```
midi [audio] [channel] [control]
```

On fader change, a corrosponding command will be fired. For OSC commands, this would send a float value between min and max arguement. For MIDI commands, this would send MIDI value equal to the slider position.

Additionally, the field `oscFeedback` can be specified, to specify certain feedback back to the X32 mixer user specified knobs. This is something that you want to explicitly specify if you configure your FOH X32 mixer to send midi commands to this app.

Additionally, specify the `defaultValue` of a fader, to force the fader to start at a certain position. This value should be a number between 0 and 127.

### talkback

Different values related to talkback.

#### destination

Which destination to use for IEM talkback enable/disable. One of either `A` or `B`.

#### channel

This is the channel that FOH talkback is being sent through. Applicable because FOH Talkback Channel is sent to IEM Mixer. Should be in a format similar to `/ch/01`.

#### link

Whether to link buttons on the FOH mixer with the mute of the talkback channel in the IEM mixer. Only applicable for 2 mixer application.

### selectLink

If configured, will send MIDI cc on select. Useful for shortcutting selecting channels in linked Ableton section.

#### targetDestination

Name of the target MIDI channel destination.

#### midiChannel

Channel to send to.

### luckyAutoMix

These are default params for the auto-mixer. This is not required, as there have been default parameters that have been hard coded. Parameters include:

#### bus

This is the default bus to use the auto mixer with. The way that this auto mixer works, is that it changes the bus sends for individual enabled channels. Because of this, it is required for the bus sends to be set as **Post Fader**.

#### postFader

This is a boolean value, specifying whether or not we want to base the auto mixer off the meter value on input, or on output. In practice, the output meter value is calculated using the input meter value, adding the fader position. *Note that the X32 auto mixer bases uses input meters for the auto mixer.*

#### threshold

This is the gate threshold. If mics meter volume are below this threshold, then all mics will be gated down to at least -10db. How this works is that `c = 0` if max meter value is below the threshold, so that all values will then translate to be between range -10db to -30db.

Be careful about adjusting threshold to be not equal to the minimum of 100, because latency issues will mean that if channel volume is ducked, it will take more time to respond.

#### m *and* c

The volume that a channel is auto mixed to depends on the following equation:

```
0.5 + arctan((Channel Volume - Max Channel Volume - c) / m) / 6
```

Effectively, `c in (-24, 0)` is the point at which the curve will hit -10db, and then start to concave back up, and `m in (1, 9)` is the slope of the curve. If you want a more aggressive automixer, then set `m` to be lower, and if you want it to be more smoothed out, set `m` to be higher.

Only exception to channels that won't follow the equation is the channel with the max meter volume, which will have unity send gain.

### resetCommands

This is a dictionary containing commands to be fired on reset call, where the key is the osc address and the value is the argument to be fired. The argument should be in the correct data format.

## Data Directory

Data directory contains files that are created and used by this program. The directory has the following types of files:

*Note that for both file formats, the first line is a header line used by the program.*

### osc

These contain osc commands in the following format:

```
[foh|iem] [command] [str|int|float] [value] [(optional, for floats only) fade time]
```

For float values only, you are also able to optionally provide a 5th arguement to specify how long you want to take to fade in the new value.

You are also able to fire MIDI cues, by putting commands in the following format:

```
midi [audio|video|light] [channel:1-16] [control:0-127] [value:0-127]
```

You are also able to open files using the following command:

```
open [filepath]
```

Additionally, you are also able to make changes to the "I'm Feeling Lucky" local auto mixer in the following format:

```
lucky [/ch/01, /ch/02, ...] [assignment: OFF, A, B, ...] [weight: -12.0 - 12.0] 
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
3. Send a MIDI cue, as configured in the `MIDI Input` page in the connection tab.

## Dependencies:

- [python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [pyinstaller](https://pypi.org/project/pyinstaller/)
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
sudo -H pip3 install --prefix=/usr/local pyinstaller
pip3 install -r requirements.txt
```

## X32 OSC Commands Reference File

[pdf](https://wiki.munichmakerlab.de/images/1/17/UNOFFICIAL_X32_OSC_REMOTE_PROTOCOL_%281%29.pdf)