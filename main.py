import os
from shutil import which

class FFVox:
    def __init__(self):
        self.raw_exp = []
        self.raw_pattern = []
        seld.raw_inst = []
        self.start = "ffmpeg "
        self.overwrite = True
        self.duration = -1
        self.end = "out.wav"
        self.main_str = (f"{self.start} "
        "-f lavfi -i \"aevalsrc=\' "
        "0.5*mod(t,1)*lt(mod(t,2),1)*((0.25)-mod(t,(0.25)))*(-1+random(0)*2)+"
        "(0.5)*gt(t,2)*lt(t,4)*sin(2*PI*t*330)+"
        "(0.3)*gt(t,3)*sin(2*PI*t*440)+"
        "(0.5)*gt(t,4)*sin(2*PI*t*220+(sin(2*PI*t*220)*0.5*((0.5)-mod(t,(0.5)))))+"
        "(0.25)*lt(t,1.75)*mod(t,1/330)*330-0.5\':"
        "d=5\" "
        f"{self.end}")
    def add_pattern(self, pattern: list):
        self.raw_pattern.append(pattern)
    def add_inst(self, inst: str):
        self.raw_inst.append(inst)
    def __eval(self):
        os.system(self.main_str)
    def render(self):
        self.__eval()
    def play(self):
        self.__eval()
        if which("termux-media-player"):
            os.system("termux-media-player play out.wav")
