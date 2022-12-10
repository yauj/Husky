config = {
    "osc": {
        "foh": "10.246.1.10",
        "iem": "10.246.1.15"
    },
    "serverMidi": "X-USB",
    "midi": {
        "audio": "X32Helper",
        "video": "Network Session 1",
        "light": "USB MIDI Interface"
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
        "Bass": {
            "channels": ["15", "16"],
            "iem_bus": "13"
        },
        "Drums": {
            "iem_bus": "15"
        }
    },
    "settings": {
        "Vocal FX": ["/fxrtn/01/mix/fader", "/fxrtn/01/mix/on", "/fxrtn/03/mix/fader", "/fxrtn/03/mix/on"],
        "Instru Mutes": [
            "/ch/05/mix/on", "/ch/06/mix/on", "/ch/07/mix/on", "/ch/08/mix/on",
            "/ch/09/mix/on", "/ch/10/mix/on", "/ch/11/mix/on", "/ch/12/mix/on",
            "/ch/13/mix/on", "/ch/14/mix/on", "/ch/15/mix/on", "/ch/16/mix/on",
            "/ch/17/mix/on", "/ch/18/mix/on", "/ch/19/mix/on", "/ch/20/mix/on",
            "/ch/21/mix/on", "/ch/22/mix/on",
            "/ch/26/mix/on", "/ch/27/mix/on", "/ch/28/mix/on",
            "/dca/1/on", "/dca/2/on", "/dca/3/on", "/dca/4/on", "/dca/5/on"
        ]
    },
    "faders": {
        "VOX EQ": {"commands": ["foh /ch/05/eq/1/g 0.2 0.5"]},
        "VOX Pan": {"commands": ["foh /ch/06/mix/pan 0.5 0.2", "foh /ch/07/mix/pan 0.5 0.8"]},
        "EG/Keys Pan": {"commands": ["foh /ch/13/mix/pan 0.5 0.2", "foh /ch/11/mix/pan 0.5 0.8"]},
        "Bass/Drums HPF": {"commands": ["foh /ch/15/preamp/hpf 0.3 0.0", "foh /ch/18/preamp/hpf 0.3 0.0", "foh /ch/20/preamp/hpf 0.3 0.0"]},
        "VOX Tracks": {"defaultValue": 63, "commands": ["midi audio 2 50"]},
        "EG/Keys Tracks": {"defaultValue": 63, "commands": ["midi audio 2 51"]},
        "Bass Tracks": {"defaultValue": 63, "commands": ["midi audio 2 52"]},
        "Drum Tracks": {"defaultValue": 63, "commands": ["midi audio 2 53"]},
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