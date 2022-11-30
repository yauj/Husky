ALL_CHANNELS = [
    "/ch/01", "/ch/02", "/ch/03", "/ch/04", "/ch/05", "/ch/06", "/ch/07", "/ch/08",
    "/ch/09", "/ch/10", "/ch/11", "/ch/12", "/ch/13", "/ch/14", "/ch/15", "/ch/16",
    "/ch/17", "/ch/18", "/ch/19", "/ch/20", "/ch/21", "/ch/22", "/ch/23", "/ch/24",
    "/ch/25", "/ch/26", "/ch/27", "/ch/28", "/ch/29", "/ch/30", "/ch/31", "/ch/32",
    "/auxin/01", "/auxin/02", "/auxin/03", "/auxin/04", "/auxin/05", "/auxin/06", "/auxin/07", "/auxin/08",
    "/fxrtn/01", "/fxrtn/02", "/fxrtn/03", "/fxrtn/04", "/fxrtn/05", "/fxrtn/06", "/fxrtn/07", "/fxrtn/08"
]
COPY_CHANNELS = [
    "/ch/01", "/ch/02", "/ch/03", "/ch/04", "/ch/05", "/ch/06", "/ch/07", "/ch/08",
    "/ch/09", "/ch/10", "/ch/11", "/ch/12", "/ch/13", "/ch/14", "/ch/15", "/ch/16",
    "/ch/17", "/ch/18", "/ch/19", "/ch/20", "/ch/21", "/ch/22", "/ch/23", "/ch/24",
    "/ch/25", "/ch/26", "/ch/27", "/ch/28", "/ch/29", "/ch/31", "/ch/32"
]
AUX_CHANNELS = [
    "/auxin/01", "/auxin/02", "/auxin/03", "/auxin/04", "/auxin/05", "/auxin/06", "/auxin/07", "/auxin/08",
    "/fxrtn/01", "/fxrtn/02", "/fxrtn/03", "/fxrtn/04", "/fxrtn/05", "/fxrtn/06", "/fxrtn/07", "/fxrtn/08"
]
LINK_CHANNELS = [
    "1-2", "3-4", "5-6", "7-8", "9-10", "11-12", "13-14", "15-16",
    "17-18", "19-20", "21-22", "23-24", "25-26", "27-28", "29-30", "31-32"
]

ALL_BUSES = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16"]
ODD_BUSES = ["01", "03", "05", "07", "09", "11", "13", "15"]

SETTINGS = {
    "Label": ["/config/name", "/config/icon", "/config/color"],
    "HPF": ["/preamp/hpon", "/preamp/hpf"],
    "EQ": [
        "/eq/1/type", "/eq/1/f", "/eq/1/g", "/eq/1/q",
        "/eq/2/type", "/eq/2/f", "/eq/2/g", "/eq/2/q",
        "/eq/3/type", "/eq/3/f", "/eq/3/g", "/eq/3/q",
        "/eq/4/type", "/eq/4/f", "/eq/4/g", "/eq/4/q"
    ],
    "Dynamics": ["/dyn/thr", "/dyn/ratio", "/dyn/knee", "/dyn/mgain", "/dyn/attack", "/dyn/hold", "/dyn/release", "/dyn/mix"],
    "Pan and Mute": ["/mix/pan", "/mix/on"]
}

KEYS = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]