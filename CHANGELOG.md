# Change Logs

### Format of versioning:

```
v[Major Version].[Minor Version].[Patch Version]
```

A **Major Version** iteration means some sort of backwards *incompatible* change has been made.

A **Minor Version** iteration means some sort of backwards *compatible* major feature has been added.

A **Patch Version** iteration means some sort of backwards *compatible* minor feature or bug fix has been made.

(See https://semver.org)

## v1.0.0 (2022-12-27)

First version of Husky!

## v1.1.0 (2023-03-05)

Add Preferences Menu, that allows you to modify the config object. This is a catch all preferences menu,
to be able to modify preferences for anything.

Also fundamentally changes the way that cache works, to save all defaults in the config.cache file.

## v1.2.0 (2023-03-21)

Add Channel Swap feature in Menu.

## v1.3.0 (2023-03-22)

Add "I'm feeling lucky" auto mixer.

## v2.0.0 (2023-03-30)

Add Talkback link, where FOH talkback buttons are linked with the mute/unmute of the talkback channel on the IEM mixer.

This is backwards incompatible change, as it changes the format of the config. Talkback config is now in the following format:

```
    "talkback": {
        "destination": "B",
        "channel": "/ch/30",
        "link": true
    },
```

Requires manual change in existing instances of Husky. Only really runs on 2 computers right now, so this change is managable.

## v2.1.0 (2023-04-08)

Add ability to use "st" (Main Out) or "mono" (Mono Out) as a iem_bus.

Also changing config to match next evolution of 45th loft.

## v2.2.0 (2023-04-13)

Add ability to open files from osc snippet files.