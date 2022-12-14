ALL_CHANNELS = [
    "/ch/01", "/ch/02", "/ch/03", "/ch/04", "/ch/05", "/ch/06", "/ch/07", "/ch/08",
    "/ch/09", "/ch/10", "/ch/11", "/ch/12", "/ch/13", "/ch/14", "/ch/15", "/ch/16",
    "/ch/17", "/ch/18", "/ch/19", "/ch/20", "/ch/21", "/ch/22", "/ch/23", "/ch/24",
    "/ch/25", "/ch/26", "/ch/27", "/ch/28", "/ch/29", "/ch/30", "/ch/31", "/ch/32",
    "/auxin/01", "/auxin/02", "/auxin/03", "/auxin/04", "/auxin/05", "/auxin/06", "/auxin/07", "/auxin/08",
    "/fxrtn/01", "/fxrtn/02", "/fxrtn/03", "/fxrtn/04", "/fxrtn/05", "/fxrtn/06", "/fxrtn/07", "/fxrtn/08"
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

BANKS_32 = ["1-8", "9-16", "17-24", "25-32"]
BANKS_48 = ["1-8", "9-16", "17-24", "25-32", "33-40", "41-48"]
BANKS_16 = ["1-4", "5-8", "9-12", "13-16"]
ROUTING_IN = [
    "Local XLR In 1-8", "Local XLR In 9-16", "Local XLR In 17-24", "Local XLR In 25-32",
    "AES-A In 1-8", "AES-A In 9-16", "AES-A In 17-24", "AES-A In 25-32", "AES-A In 33-40", "AES-A In 41-48",
    "AES-B In 1-8", "AES-B In 9-16", "AES-B In 17-24", "AES-B In 25-32", "AES-B In 33-40", "AES-B In 41-48",
    "Card In 1-8", "Card In 9-16", "Card In 17-24", "Card In 25-32",
    "User In 1-8", "User In 9-16", "User In 17-24", "User In 25-32",
]
ROUTING_IN_AUX = [
    "Local AUX In 1-6",
    "Local XLR In 1-2", "Local XLR In 1-4", "Local XLR In 1-6",
    "AES-A In 1-2", "AES-A In 1-4", "AES-A In 1-6",
    "AES-B In 1-2", "AES-B In 1-4", "AES-B In 1-6",
    "Card In 1-2", "Card In 1-4", "Card In 1-6",
    "User In 1-2", "User In 1-4", "User In 1-6",
]
ROUTING_IN_USER = [
    "OFF",
    "Local XLR In 01", "Local XLR In 02", "Local XLR In 03", "Local XLR In 04", "Local XLR In 05", "Local XLR In 06", "Local XLR In 07", "Local XLR In 08",
    "Local XLR In 09", "Local XLR In 10", "Local XLR In 11", "Local XLR In 12", "Local XLR In 13", "Local XLR In 14", "Local XLR In 15", "Local XLR In 16",
    "Local XLR In 17", "Local XLR In 18", "Local XLR In 19", "Local XLR In 20", "Local XLR In 21", "Local XLR In 22", "Local XLR In 23", "Local XLR In 24",
    "Local XLR In 25", "Local XLR In 26", "Local XLR In 27", "Local XLR In 28", "Local XLR In 29", "Local XLR In 30", "Local XLR In 31", "Local XLR In 32",
    "AES-A In 01", "AES-A In 02", "AES-A In 03", "AES-A In 04", "AES-A In 05", "AES-A In 06", "AES-A In 07", "AES-A In 08",
    "AES-A In 09", "AES-A In 10", "AES-A In 11", "AES-A In 12", "AES-A In 13", "AES-A In 14", "AES-A In 15", "AES-A In 16",
    "AES-A In 17", "AES-A In 18", "AES-A In 19", "AES-A In 20", "AES-A In 21", "AES-A In 22", "AES-A In 23", "AES-A In 24",
    "AES-A In 25", "AES-A In 26", "AES-A In 27", "AES-A In 28", "AES-A In 29", "AES-A In 30", "AES-A In 31", "AES-A In 32",
    "AES-A In 33", "AES-A In 34", "AES-A In 35", "AES-A In 36", "AES-A In 37", "AES-A In 38", "AES-A In 39", "AES-A In 40",
    "AES-A In 41", "AES-A In 42", "AES-A In 43", "AES-A In 44", "AES-A In 45", "AES-A In 46", "AES-A In 47", "AES-A In 48",
    "AES-B In 01", "AES-B In 02", "AES-B In 03", "AES-B In 04", "AES-B In 05", "AES-B In 06", "AES-B In 07", "AES-B In 08",
    "AES-B In 09", "AES-B In 10", "AES-B In 11", "AES-B In 12", "AES-B In 13", "AES-B In 14", "AES-B In 15", "AES-B In 16",
    "AES-B In 17", "AES-B In 18", "AES-B In 19", "AES-B In 20", "AES-B In 21", "AES-B In 22", "AES-B In 23", "AES-B In 24",
    "AES-B In 25", "AES-B In 26", "AES-B In 27", "AES-B In 28", "AES-B In 29", "AES-B In 30", "AES-B In 31", "AES-B In 32",
    "AES-B In 33", "AES-B In 34", "AES-B In 35", "AES-B In 36", "AES-B In 37", "AES-B In 38", "AES-B In 39", "AES-B In 40",
    "AES-B In 41", "AES-B In 42", "AES-B In 43", "AES-B In 44", "AES-B In 45", "AES-B In 46", "AES-B In 47", "AES-B In 48",
    "Card In 01", "Card In 02", "Card In 03", "Card In 04", "Card In 05", "Card In 06", "Card In 07", "Card In 08",
    "Card In 09", "Card In 10", "Card In 11", "Card In 12", "Card In 13", "Card In 14", "Card In 15", "Card In 16",
    "Card In 17", "Card In 18", "Card In 19", "Card In 20", "Card In 21", "Card In 22", "Card In 23", "Card In 24",
    "Card In 25", "Card In 26", "Card In 27", "Card In 28", "Card In 29", "Card In 30", "Card In 31", "Card In 32",
    "Local AUX In 1", "Local AUX In 2", "Local AUX In 3", "Local AUX In 4", "Local AUX In 5", "Local AUX In 6", "Talkback Internal", "Talkback External",
]
ROUTING_OUT = [
    "Local XLR In 1-8", "Local XLR In 9-16", "Local XLR In 17-24", "Local XLR In 25-32",
    "AES-A In 1-8", "AES-A In 9-16", "AES-A In 17-24", "AES-A In 25-32", "AES-A In 33-40", "AES-A In 41-48",
    "AES-B In 1-8", "AES-B In 9-16", "AES-B In 17-24", "AES-B In 25-32", "AES-B In 33-40", "AES-B In 41-48",
    "Card In 1-8", "Card In 9-16", "Card In 17-24", "Card In 25-32",
    "Out Patch 1-8", "Out Patch 9-16",
    "P16 1-8", "P16 9-16",
    "AUX Channel 1-6/Monitor", "AUX In 1-6/Talkback",
    "User Out 1-8", "User Out 9-16", "User Out 17-24", "User Out 25-32", "User Out 33-40", "User Out 41-48",
    "User In 1-8", "User In 9-16", "User In 17-24", "User In 25-32",
]
ROUTING_OUT_LOCAL_A = [
    "Local XLR In 1-4", "Local XLR In 9-12", "Local XLR In 17-20", "Local XLR In 25-28",
    "AES-A In 1-4", "AES-A In 9-12", "AES-A In 17-20", "AES-A In 25-28", "AES-A In 33-36", "AES-A In 41-44",
    "AES-B In 1-4", "AES-B In 9-12", "AES-B In 17-20", "AES-B In 25-28", "AES-B In 33-36", "AES-B In 41-44",
    "Card In 1-4", "Card In 9-12", "Card In 17-20", "Card In 25-28",
    "Out Patch 1-4", "Out Patch 9-12",
    "P16 1-4", "P16 9-12",
    "AUX Channel 1-4", "AUX In 1-4",
    "User Out 1-4", "User Out 9-12", "User Out 17-20", "User Out 25-28", "User Out 33-36", "User Out 41-44",
    "User In 1-4", "User In 9-12", "User In 17-20", "User In 25-28",
]
ROUTING_OUT_LOCAL_B = [
    "Local XLR In 5-8", "Local XLR In 13-16", "Local XLR In 21-24", "Local XLR In 29-32",
    "AES-A In 5-8", "AES-A In 13-16", "AES-A In 21-24", "AES-A In 29-32", "AES-A In 37-40", "AES-A In 45-48",
    "AES-B In 5-8", "AES-B In 13-16", "AES-B In 21-24", "AES-B In 29-32", "AES-B In 37-40", "AES-B In 45-48",
    "Card In 5-8", "Card In 13-16", "Card In 21-24", "Card In 29-32",
    "Out Patch 5-8", "Out Patch 13-16",
    "P16 5-8", "P16 13-16",
    "AUX Channel 5-6/Monitor", "AUX In 5-6/Talkback",
    "User Out 5-8", "User Out 13-16", "User Out 21-24", "User Out 29-32", "User Out 37-40", "User Out 45-48",
    "User In 5-8", "User In 13-16", "User In 21-24", "User In 29-32",
]
ROUTING_OUT_DIGITAL = [
    "OFF", "Main L", "Main R", "Main M/C",
    "Bus 01", "Bus 02", "Bus 03", "Bus 04", "Bus 05", "Bus 06", "Bus 07", "Bus 08",
    "Bus 09", "Bus 10", "Bus 11", "Bus 12", "Bus 13", "Bus 14", "Bus 15", "Bus 16",
    "Matrix 01", "Matrix 02", "Matrix 03", "Matrix 04", "Matrix 05", "Matrix 06",
    "Channel 01", "Channel 02", "Channel 03", "Channel 04", "Channel 05", "Channel 06", "Channel 07", "Channel 08",
    "Channel 09", "Channel 10", "Channel 11", "Channel 12", "Channel 13", "Channel 14", "Channel 15", "Channel 16",
    "Channel 17", "Channel 18", "Channel 19", "Channel 20", "Channel 21", "Channel 22", "Channel 23", "Channel 24",
    "Channel 25", "Channel 26", "Channel 27", "Channel 28", "Channel 29", "Channel 30", "Channel 31", "Channel 32",
    "AUX Channel 1", "AUX Channel 2", "AUX Channel 3", "AUX Channel 4", "AUX Channel 5", "AUX Channel 6", "AUX Channel 7", "AUX Channel 8",
    "FX Return 1L", "FX Return 1R", "FX Return 2L", "FX Return 2R", "FX Return 3L", "FX Return 3R", "FX Return 4L", "FX Return 4R",
    "Monitor L", "Monitor R", "Talkback Out"
]
ROUTING_OUT_USER = [
    "OFF",
    "Local XLR In 01", "Local XLR In 02", "Local XLR In 03", "Local XLR In 04", "Local XLR In 05", "Local XLR In 06", "Local XLR In 07", "Local XLR In 08",
    "Local XLR In 09", "Local XLR In 10", "Local XLR In 11", "Local XLR In 12", "Local XLR In 13", "Local XLR In 14", "Local XLR In 15", "Local XLR In 16",
    "Local XLR In 17", "Local XLR In 18", "Local XLR In 19", "Local XLR In 20", "Local XLR In 21", "Local XLR In 22", "Local XLR In 23", "Local XLR In 24",
    "Local XLR In 25", "Local XLR In 26", "Local XLR In 27", "Local XLR In 28", "Local XLR In 29", "Local XLR In 30", "Local XLR In 31", "Local XLR In 32",
    "AES-A In 01", "AES-A In 02", "AES-A In 03", "AES-A In 04", "AES-A In 05", "AES-A In 06", "AES-A In 07", "AES-A In 08",
    "AES-A In 09", "AES-A In 10", "AES-A In 11", "AES-A In 12", "AES-A In 13", "AES-A In 14", "AES-A In 15", "AES-A In 16",
    "AES-A In 17", "AES-A In 18", "AES-A In 19", "AES-A In 20", "AES-A In 21", "AES-A In 22", "AES-A In 23", "AES-A In 24",
    "AES-A In 25", "AES-A In 26", "AES-A In 27", "AES-A In 28", "AES-A In 29", "AES-A In 30", "AES-A In 31", "AES-A In 32",
    "AES-A In 33", "AES-A In 34", "AES-A In 35", "AES-A In 36", "AES-A In 37", "AES-A In 38", "AES-A In 39", "AES-A In 40",
    "AES-A In 41", "AES-A In 42", "AES-A In 43", "AES-A In 44", "AES-A In 45", "AES-A In 46", "AES-A In 47", "AES-A In 48",
    "AES-B In 01", "AES-B In 02", "AES-B In 03", "AES-B In 04", "AES-B In 05", "AES-B In 06", "AES-B In 07", "AES-B In 08",
    "AES-B In 09", "AES-B In 10", "AES-B In 11", "AES-B In 12", "AES-B In 13", "AES-B In 14", "AES-B In 15", "AES-B In 16",
    "AES-B In 17", "AES-B In 18", "AES-B In 19", "AES-B In 20", "AES-B In 21", "AES-B In 22", "AES-B In 23", "AES-B In 24",
    "AES-B In 25", "AES-B In 26", "AES-B In 27", "AES-B In 28", "AES-B In 29", "AES-B In 30", "AES-B In 31", "AES-B In 32",
    "AES-B In 33", "AES-B In 34", "AES-B In 35", "AES-B In 36", "AES-B In 37", "AES-B In 38", "AES-B In 39", "AES-B In 40",
    "AES-B In 41", "AES-B In 42", "AES-B In 43", "AES-B In 44", "AES-B In 45", "AES-B In 46", "AES-B In 47", "AES-B In 48",
    "Card In 01", "Card In 02", "Card In 03", "Card In 04", "Card In 05", "Card In 06", "Card In 07", "Card In 08",
    "Card In 09", "Card In 10", "Card In 11", "Card In 12", "Card In 13", "Card In 14", "Card In 15", "Card In 16",
    "Card In 17", "Card In 18", "Card In 19", "Card In 20", "Card In 21", "Card In 22", "Card In 23", "Card In 24",
    "Card In 25", "Card In 26", "Card In 27", "Card In 28", "Card In 29", "Card In 30", "Card In 31", "Card In 32",
    "Local AUX In 1", "Local AUX In 2", "Local AUX In 3", "Local AUX In 4", "Local AUX In 5", "Local AUX In 6", "Talkback Internal", "Talkback External",
    "Out Patch 01", "Out Patch 02", "Out Patch 03", "Out Patch 04", "Out Patch 05", "Out Patch 06", "Out Patch 07", "Out Patch 08",
    "Out Patch 09", "Out Patch 10", "Out Patch 11", "Out Patch 12", "Out Patch 13", "Out Patch 14", "Out Patch 15", "Out Patch 16",
    "P16 01", "P16 02", "P16 03", "P16 04", "P16 05", "P16 06", "P16 07", "P16 08",
    "P16 09", "P16 10", "P16 11", "P16 12", "P16 13", "P16 14", "P16 15", "P16 16",
    "AUX Channel 1", "AUX Channel 2", "AUX Channel 3", "AUX Channel 4", "AUX Channel 5", "AUX Channel 6", "Monitor L", "Monitor R",
]

SETTINGS = {
    "Label": ["/config/icon", "/config/color"],
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