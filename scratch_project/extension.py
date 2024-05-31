from dataclasses import dataclass


@dataclass
class Extension:
    extension_id: str
    documentation_link: str

    def to_dict(self):
        return self.extension_id


pen = Extension(
    "pen",
    "https://en.scratch-wiki.info/wiki/Pen_Extension"
)
wedo2 = Extension(
    "wedo2",
    "https://en.scratch-wiki.info/wiki/LEGO_Education_WeDo_2.0_Extension"
)
music = Extension(
    "music",
    "https://en.scratch-wiki.info/wiki/Music_Extension"
)
microbit = Extension(
    "microbit",
    "https://en.scratch-wiki.info/wiki/Micro:bit_Extension"
)
text2speech = Extension(
    "text2speech",
    "https://en.scratch-wiki.info/wiki/Text_to_Speech_Extension"
)
translate = Extension(
    "translate",
    "https://en.scratch-wiki.info/wiki/Translate_Extension"
)
videoSensing = Extension(
    "videoSensing",
    "https://en.scratch-wiki.info/wiki/Video_Sensing_Extension"
)
ev3 = Extension(
    "ev3",
    "https://en.scratch-wiki.info/wiki/LEGO_MINDSTORMS_EV3_Extension"
)
makeymakey = Extension(
    "makeymakey",
    "https://en.scratch-wiki.info/wiki/Makey_Makey_Extension"
)
boost = Extension(
    "boost",              
    "https://en.scratch-wiki.info/wiki/LEGO_BOOST_Extension"
)
gdxfor = Extension(
    "gdxfor",
    "https://en.scratch-wiki.info/wiki/Go_Direct_Force_%26_Acceleration_Extension"
)
