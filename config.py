config = {
    "osc": {
        "foh": "10.246.1.10",
        "iem": "10.246.1.15"
    },
    "atemPort": "3333",
    "midi": {
        "audio": {
            "default": "Husky",
            "type": "cc",
            "defaultChannel": 2
        },
        "video": {
            "default": "Network Session 1",
            "type": "note",
            "defaultChannel": 6
        },
        "light": {
            "default": "USB MIDI Interface",
            "type": "note",
            "defaultChannel": 15
        },
    },
    "serverMidi": {
        "X-USB": [
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 0},
                "command": {"type": "Cue", "page": "CURRENT", "index": "1"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 1},
                "command": {"type": "Cue", "page": "CURRENT", "index": "2"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 2},
                "command": {"type": "Cue", "page": "CURRENT", "index": "3"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 3},
                "command": {"type": "Cue", "page": "CURRENT", "index": "4"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 4},
                "command": {"type": "Cue", "page": "CURRENT", "index": "5"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 5},
                "command": {"type": "Cue", "page": "CURRENT", "index": "6"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 6},
                "command": {"type": "Cue", "page": "CURRENT", "index": "7"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 7},
                "command": {"type": "Cue", "page": "CURRENT", "index": "8"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 8},
                "command": {"type": "Cue", "page": "CURRENT", "index": "9"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 9},
                "command": {"type": "Cue", "page": "CURRENT", "index": "10"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 10},
                "command": {"type": "Cue", "page": "CURRENT", "index": "Prev Page"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 11},
                "command": {"type": "Cue", "page": "CURRENT", "index": "Next Page"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 12},
                "command": {"type": "Cue", "page": "a", "index": "1"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 13},
                "command": {"type": "Cue", "page": "a", "index": "2"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 14},
                "command": {"type": "Cue", "page": "a", "index": "3"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 15},
                "command": {"type": "Cue", "page": "a", "index": "4"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 16},
                "command": {"type": "Cue", "page": "b", "index": "1"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 17},
                "command": {"type": "Cue", "page": "b", "index": "2"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 18},
                "command": {"type": "Cue", "page": "b", "index": "3"}
            },
            {
                "midi": {"type": "Control Change", "channel": 1, "control": 19},
                "command": {"type": "Cue", "page": "b", "index": "4"}
            }
        ]
    },
    "personal": {
        "DPA": {
            "channels": ["01"]
        },
        "HH1": {
            "channels": ["02"]
        },
        "HH2": {
            "channels": ["03"]
        },
        "Vocals 1": {
            "channels": ["05", "09"],
            "iem_bus": "01"
        },
        "Vocals 2": {
            "channels": ["06"],
            "iem_bus": "03"
        },
        "Vocals 3": {
            "channels": ["07"],
            "iem_bus": "05"
        },
        "Keys": {
            "channels": ["10", "11", "12"],
            "iem_bus": "09"
        },
        "EG": {
            "channels": ["13"],
            "iem_bus": "11"
        },
        "EG2": {
            "channels": ["14"],
            "iem_bus": "07"
        },
        "Bass": {
            "channels": ["15"],
            "iem_bus": "13"
        },
        "Drums": {
            "iem_bus": "15"
        }
    },
    "cues": {
        "cuePages": 5,
        "faderPages": 5,
        "cueOptions": {
            "Key of Song": {
                "RESET": ["midi audio 2 100 127", "midi audio 2 101 0", "midi audio 2 102 0"],
                "C": ["midi audio 2 100 127", "midi audio 2 101 0", "midi audio 2 102 127"],
                "Db": ["midi audio 2 100 127", "midi audio 2 101 12", "midi audio 2 102 127"],
                "D": ["midi audio 2 100 127", "midi audio 2 101 23", "midi audio 2 102 127"],
                "Eb": ["midi audio 2 100 127", "midi audio 2 101 35", "midi audio 2 102 127"],
                "E": ["midi audio 2 100 127", "midi audio 2 101 46", "midi audio 2 102 127"],
                "F": ["midi audio 2 100 127", "midi audio 2 101 58", "midi audio 2 102 127"],
                "Gb": ["midi audio 2 100 127", "midi audio 2 101 69", "midi audio 2 102 127"],
                "G": ["midi audio 2 100 127", "midi audio 2 101 81", "midi audio 2 102 127"],
                "Ab": ["midi audio 2 100 127", "midi audio 2 101 92", "midi audio 2 102 127"],
                "A": ["midi audio 2 100 127", "midi audio 2 101 104", "midi audio 2 102 127"],
                "Bb": ["midi audio 2 100 127", "midi audio 2 101 115", "midi audio 2 102 127"],
                "B": ["midi audio 2 100 127", "midi audio 2 101 127", "midi audio 2 102 127"],
            },
            "Vocal Lead": {
                "RESET": [
                    "foh /ch/05/mix/01/on int 1", "/ch/05/mix/02/on int 1", "/ch/05/mix/03/on int 0",
                    "foh /ch/06/mix/01/on int 0", "/ch/06/mix/02/on int 0", "/ch/06/mix/03/on int 1",
                    "foh /ch/07/mix/01/on int 0", "/ch/07/mix/02/on int 0", "/ch/07/mix/03/on int 1",
                    "foh /ch/08/mix/01/on int 0", "/ch/08/mix/02/on int 0", "/ch/08/mix/03/on int 1",
                ],
                "1": [
                    "foh /ch/05/mix/01/on int 1", "/ch/05/mix/02/on int 1", "/ch/05/mix/03/on int 0",
                    "foh /ch/06/mix/01/on int 0", "/ch/06/mix/02/on int 0", "/ch/06/mix/03/on int 1",
                    "foh /ch/07/mix/01/on int 0", "/ch/07/mix/02/on int 0", "/ch/07/mix/03/on int 1",
                    "foh /ch/08/mix/01/on int 0", "/ch/08/mix/02/on int 0", "/ch/08/mix/03/on int 1",
                ],
                "2": [
                    "foh /ch/05/mix/01/on int 0", "/ch/05/mix/02/on int 0", "/ch/05/mix/03/on int 1",
                    "foh /ch/06/mix/01/on int 1", "/ch/06/mix/02/on int 1", "/ch/06/mix/03/on int 0",
                    "foh /ch/07/mix/01/on int 0", "/ch/07/mix/02/on int 0", "/ch/07/mix/03/on int 1",
                    "foh /ch/08/mix/01/on int 0", "/ch/08/mix/02/on int 0", "/ch/08/mix/03/on int 1",
                ],
                "3": [
                    "foh /ch/05/mix/01/on int 0", "/ch/05/mix/02/on int 0", "/ch/05/mix/03/on int 1",
                    "foh /ch/06/mix/01/on int 0", "/ch/06/mix/02/on int 0", "/ch/06/mix/03/on int 1",
                    "foh /ch/07/mix/01/on int 1", "/ch/07/mix/02/on int 1", "/ch/07/mix/03/on int 0",
                    "foh /ch/08/mix/01/on int 0", "/ch/08/mix/02/on int 0", "/ch/08/mix/03/on int 1",
                ],
                "4": [
                    "foh /ch/05/mix/01/on int 0", "/ch/05/mix/02/on int 0", "/ch/05/mix/03/on int 1",
                    "foh /ch/06/mix/01/on int 0", "/ch/06/mix/02/on int 0", "/ch/06/mix/03/on int 1",
                    "foh /ch/07/mix/01/on int 0", "/ch/07/mix/02/on int 0", "/ch/07/mix/03/on int 1",
                    "foh /ch/08/mix/01/on int 1", "/ch/08/mix/02/on int 1", "/ch/08/mix/03/on int 0",
                ],
            }
        },
        "faders": {
            "VOX EQ": {"oscFeedback": "/-stat/userpar/29/value", "commands": ["foh /ch/05/eq/1/g 0.2 0.5"]},
            "VOX Pan": {"oscFeedback": "/-stat/userpar/30/value", "commands": ["foh /ch/06/mix/pan 0.5 0.2", "foh /ch/07/mix/pan 0.5 0.8"]},
            "EG/Keys Pan": {"oscFeedback": "/-stat/userpar/31/value", "commands": ["foh /ch/13/mix/pan 0.5 0.2", "foh /ch/11/mix/pan 0.5 0.8"]},
            "Bass/Drums HPF": {"oscFeedback": "/-stat/userpar/32/value", "commands": ["foh /ch/20/preamp/hpf 0.3 0.0"]},
            "VOX Tracks": {"defaultValue": 63, "commands": ["midi audio 2 50"]},
            "EG/Keys Tracks": {"defaultValue": 63, "commands": ["midi audio 2 51"]},
            "Bass Tracks": {"defaultValue": 63, "commands": ["midi audio 2 52"]},
            "Drum Tracks": {"defaultValue": 63, "commands": ["midi audio 2 53"]},
            "Stream Lead VOX": {"commands": ["foh /bus/01/mix/03/level 0.5 1.0"]},
            "Stream Para Xpres": {"commands": ["foh /bus/02/mix/03/level 0.5 1.0"]},
            "Stream Bkgd VOX": {"commands": ["foh /bus/03/mix/03/level 0.5 1.0"]},
            "Stream Crowd Mics": {"commands": ["foh /ch/31/mix/13/level 0.5 1.0"]},
            "Stream Instruments": {"commands": ["foh /bus/05/mix/03/level 0.5 1.0"]},
            "Stream Drums": {"commands": ["foh /bus/07/mix/03/level 0.5 1.0"]},
            "Stream Wireless": {"commands": ["foh /bus/08/mix/03/level 0.5 1.0"]},
            "Stream FX": {"commands": ["foh /bus/09/mix/03/level 0.5 1.0"]},
            "Stream Podium": {"commands": ["atem /atem/audio/input/9/gain -10 10"]},
            "Stream ProPre": {"commands": ["atem /atem/audio/input/10/gain -10 10"]},
            "Stream MP3": {"commands": ["foh /auxin/05/mix/13/level 0.5 1.0"]},
            "Stream Overall": {"commands": ["atem /atem/audio/output/gain -60 10"]}
        },
    },
    "talkbackChannel": "/ch/30",
    "resetCommands": {
        "/ch/01/mix/fader": 0.75, "/ch/01/mix/pan": 0.5, "/ch/01/mix/on": 1,
        "/ch/02/mix/fader": 0.75, "/ch/02/mix/pan": 0.5, "/ch/02/mix/on": 1,
        "/ch/03/mix/fader": 0.75, "/ch/03/mix/pan": 0.5, "/ch/03/mix/on": 1,
        "/ch/04/mix/fader": 0.0, "/ch/04/mix/pan": 0.5,
        "/ch/05/mix/fader": 0.0, "/ch/05/mix/pan": 0.5,
        "/ch/06/mix/fader": 0.0, "/ch/06/mix/pan": 0.5,
        "/ch/07/mix/fader": 0.0, "/ch/07/mix/pan": 0.5,
        "/ch/08/mix/fader": 0.0, "/ch/08/mix/pan": 0.5,
        "/ch/09/mix/fader": 0.0, "/ch/09/mix/pan": 0.5,
        "/ch/10/mix/fader": 0.0, "/ch/10/mix/pan": 0.5,
        "/ch/11/mix/fader": 0.0, "/ch/11/mix/pan": 0.5,
        "/ch/12/mix/fader": 0.0, "/ch/12/mix/pan": 0.5,
        "/ch/13/mix/fader": 0.0, "/ch/13/mix/pan": 0.5,
        "/ch/14/mix/fader": 0.0, "/ch/14/mix/pan": 0.5,
        "/ch/15/mix/fader": 0.0, "/ch/15/mix/pan": 0.5,
        "/ch/16/mix/fader": 0.0, "/ch/16/mix/pan": 0.5,
        "/ch/17/mix/fader": 0.0, "/ch/17/mix/pan": 0.5,
        "/ch/18/mix/fader": 0.0, "/ch/18/mix/pan": 0.5,
        "/ch/19/mix/fader": 0.0, "/ch/19/mix/pan": 0.5,
        "/ch/20/mix/fader": 0.0, "/ch/20/mix/pan": 0.5,
        "/ch/21/mix/fader": 0.0, "/ch/21/mix/pan": 0.5,
        "/ch/22/mix/fader": 0.0, "/ch/22/mix/pan": 0.5,
        "/ch/23/mix/fader": 0.0, "/ch/23/mix/pan": 0.5,
        "/ch/24/mix/fader": 0.75, "/ch/24/mix/pan": 0.5, "/ch/24/mix/on": 1,
        "/ch/25/mix/fader": 0.0, "/ch/25/mix/pan": 0.5,
        "/ch/26/mix/fader": 0.0, "/ch/26/mix/pan": 0.5,
        "/ch/27/mix/fader": 0.0, "/ch/27/mix/pan": 0.0, "/ch/28/mix/pan": 1.0,
        "/ch/29/mix/fader": 0.0, "/ch/29/mix/pan": 0.5,
        "/ch/30/mix/fader": 0.0, "/ch/30/mix/pan": 0.5,
        "/ch/31/mix/fader": 0.75, "/ch/31/mix/pan": 0.0, "/ch/32/mix/pan": 1.0, "/ch/31/mix/on": 1,
        "/ch/31/mix/13/level": 0.75, "/ch/31/mix/13/pan": 0.0, "/ch/32/mix/13/pan": 1.0, "/ch/31/mix/13/on": 1,
        "/auxin/01/mix/fader": 0.5, "/auxin/01/mix/pan": 0.25, "/auxin/02/mix/pan": 0.75, "/auxin/01/mix/on": 1,
        "/auxin/03/mix/fader": 0.75, "/auxin/03/mix/pan": 0.25, "/auxin/04/mix/pan": 0.75, "/auxin/03/mix/on": 1,
        "/auxin/05/mix/fader": 0.75, "/auxin/05/mix/pan": 0.25, "/auxin/06/mix/pan": 0.75, "/auxin/05/mix/on": 1,
        "/auxin/05/mix/13/level": 0.75, "/auxin/05/mix/13/pan": 0.25, "/auxin/06/mix/13/pan": 0.75, "/auxin/05/mix/13/on": 1,
        "/fxrtn/01/mix/fader": 0.75, "/fxrtn/01/mix/pan": 0.0, "/fxrtn/02/mix/pan": 1.0, "/fxrtn/01/mix/on": 1,
        "/fxrtn/03/mix/fader": 0.75, "/fxrtn/03/mix/pan": 0.0, "/fxrtn/04/mix/pan": 1.0, "/fxrtn/03/mix/on": 1,
        "/fxrtn/05/mix/fader": 0.75, "/fxrtn/05/mix/pan": 0.0, "/fxrtn/06/mix/pan": 1.0, "/fxrtn/05/mix/on": 1,
        "/fxrtn/07/mix/fader": 0.75, "/fxrtn/07/mix/pan": 0.0, "/fxrtn/08/mix/pan": 1.0, "/fxrtn/07/mix/on": 1,
        "/bus/01/mix/fader": 0.75, "/bus/01/mix/pan": 0.5, "/bus/01/mix/on": 1,
        "/bus/01/mix/03/level": 0.75, "/bus/01/mix/03/pan": 0.5, "/bus/01/mix/03/on": 1,
        "/bus/02/mix/fader": 0.75, "/bus/02/mix/pan": 0.5, "/bus/02/mix/on": 1,
        "/bus/02/mix/03/level": 0.75, "/bus/02/mix/03/pan": 0.5, "/bus/02/mix/03/on": 1,
        "/bus/03/mix/fader": 0.75, "/bus/03/mix/pan": 0.0, "/bus/04/mix/pan": 1.0, "/bus/03/mix/on": 1,
        "/bus/03/mix/03/level": 0.75, "/bus/03/mix/03/pan": 0.0, "/bus/04/mix/03/pan": 1.0, "/bus/03/mix/03/on": 1,
        "/bus/05/mix/fader": 0.75, "/bus/05/mix/pan": 0.0, "/bus/06/mix/pan": 1.0, "/bus/05/mix/on": 1,
        "/bus/05/mix/03/level": 0.75, "/bus/05/mix/03/pan": 0.0, "/bus/06/mix/03/pan": 1.0, "/bus/05/mix/03/on": 1,
        "/bus/07/mix/fader": 0.75, "/bus/07/mix/pan": 0.5, "/bus/07/mix/on": 1,
        "/bus/07/mix/03/level": 0.75, "/bus/07/mix/03/pan": 0.5, "/bus/07/mix/03/on": 1,
        "/bus/08/mix/fader": 0.75, "/bus/08/mix/pan": 0.5, "/bus/08/mix/on": 1,
        "/bus/08/mix/03/level": 0.75, "/bus/08/mix/03/pan": 0.5, "/bus/08/mix/03/on": 1,
        "/bus/09/mix/fader": 0.75, "/bus/09/mix/pan": 0.0, "/bus/10/mix/pan": 1.0, "/bus/09/mix/on": 1,
        "/bus/09/mix/03/level": 0.75, "/bus/09/mix/03/pan": 0.0, "/bus/10/mix/03/pan": 1.0, "/bus/09/mix/03/on": 1,
        "/bus/11/mix/fader": 0.75, "/bus/11/mix/pan": 0.0, "/bus/12/mix/pan": 1.0, "/bus/11/mix/on": 1,
        "/bus/13/mix/fader": 0.75, "/bus/13/mix/pan": 0.0, "/bus/14/mix/pan": 1.0, "/bus/13/mix/on": 1,
        "/bus/13/mix/03/level": 0.75, "/bus/13/mix/03/pan": 0.0, "/bus/14/mix/03/pan": 1.0, "/bus/13/mix/03/on": 1,
        "/bus/15/mix/fader": 0.75, "/bus/15/mix/pan": 0.5, "/bus/15/mix/on": 1,
        "/bus/16/mix/fader": 0.75, "/bus/16/mix/pan": 0.5, "/bus/16/mix/on": 1,
        "/mtx/01/mix/fader": 0.75, "/mtx/01/mix/pan": 0.5, "/mtx/01/mix/on": 1,
        "/mtx/02/mix/fader": 0.75, "/mtx/02/mix/pan": 0.5, "/mtx/02/mix/on": 1,
        "/mtx/03/mix/fader": 0.75, "/mtx/03/mix/pan": 0.0, "/mtx/04/mix/pan": 1.0, "/mtx/03/mix/on": 1,
        "/main/st/mix/fader": 0.0, "/main/st/mix/on": 1,
        "/main/m/mix/fader": 0.75, "/main/m/mix/on": 1,
        "/dca/1/fader": 0.75, "/dca/1/on": 0,
        "/dca/2/fader": 0.75, "/dca/2/on": 0,
        "/dca/3/fader": 0.75, "/dca/3/on": 0,
        "/dca/4/fader": 0.75, "/dca/4/on": 0,
        "/dca/5/fader": 0.75, "/dca/5/on": 1,
        "/dca/6/fader": 0.75, "/dca/6/on": 1,
        "/dca/7/fader": 0.5, "/dca/7/on": 1,
        "/dca/8/fader": 0.0, "/dca/8/on": 1,
    }
}