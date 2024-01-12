import os
from shutil import which

class Tracker:
    def __init__(self):
        self.raw_exp = []
        self.raw_pattern = []
        seld.raw_inst = []
        self.start = "ffmpeg "
        self.aeval_init = "-f lavfi -i \"aevalsrc=\' "
        self.overwrite = True
        self.duration = -1
        self.end = "out.wav"
          
    def add_pattern(self, pattern: list):
        self.raw_pattern.append(pattern)
    def add_inst(self, inst: str):
        self.raw_inst.append(inst)
    def __eval(self):
        overwrite_tag = ""
        if self.overwrite:
            overwrite_tag = "-y "
        expr_inst = "".join("+".join(self.raw_inst), "/' ")
        duration = 0
        if self.duration == -1:
            #TBD: duration = lenght of track
            pass
        elif self.duration > 0:
            duration = self.duration
        expr = (f"{self.start}"
                f"{overwrite_tag}"
                f"{self.aeval_init}"
            #"0.5*mod(t,1)*lt(mod(t,2),1)*((0.25)-mod(t,(0.25)))*(-1+random(0)*2)"
            f"expr_inst"
            "d={duration}\" "
            f"{self.end}")
        os.system(expr)
    def render(self):
        self.__eval()
    def play(self):
        self.__eval()
        if which("termux-media-player"):
            os.system("termux-media-player play out.wav")
