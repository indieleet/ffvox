from os import system
from shutil import which

class Tracker:
    def __init__(self):
        self.raw_exp = []
        self.raw_pattern = []
        self.raw_inst = []
        self.start = "ffmpeg "
        self.aeval_init = "-f lavfi -i \"aevalsrc=\' "
        self.overwrite = True
        self.duration = -1
        self.end = "out.wav"
          
    def add_pattern(self, pattern: list):
        """
        Pattern structure
        [[base_frequency, bese_lenght, base_velocity], 
        [instrument, frequency, length, velocity, effect**, effect_value**],
        [...],
        ...]
        Example:
        [440,
        [3/4, 2/3, 1/100, 0],
        [1, 1, 100, 0]]
        """
        self.raw_pattern.extend(pattern)
    def add_inst(self, inst: str):
        self.raw_inst.append(inst)
        return len(self.raw_inst) - 1
    def __eval(self):
        overwrite_tag = ""
        if self.overwrite:
            overwrite_tag = "-y "
        raw_expr = []
        freq = 1
        length = 1
        velocity = 1
        time_start = 0
        time_end = 0
        for n, line in enumerate(self.raw_pattern):
            if n == 0:
                freq = line[0]
                length = line[1]
                velocity = line[2]
                continue
            freq *= line[1]
            length *= line[2]
            velocity *= line[3]
            time_end += length
            raw_expr.append("".join([f"between(t, {time_start}, {time_end})*", self.raw_inst[line[0]]]))
            time_start = time_end
        expr_inst = "".join(["+".join(raw_expr), "\':"])
        duration = 0
        if self.duration == -1:
            #TBD: duration = lenght of track
            pass
        elif self.duration > 0:
            duration = self.duration
        expr = (f"{self.start}"
                f"{overwrite_tag}"
                f"{self.aeval_init}"
                f"{expr_inst}"
                f"d={duration}\" "
                f"{self.end}")
        system(expr)
    def render(self):
        self.__eval()
    def play(self):
        self.__eval()
        if which("termux-media-player"):
            system("termux-media-player play out.wav")
