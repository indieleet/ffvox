from os import system
from shutil import which
import re

class Tracker:
    def __init__(self, volume: float = 1,
                 duration: float = -1, 
                 overwrite: bool = True,
                 name: str = "out",
                 form :str = "wav"):
        self.raw_exp = []
        self.raw_pattern = []
        self.raw_inst = []
        self.start = "ffmpeg "
        self.aeval_init = "-f lavfi -i \"aevalsrc=\'"
        self.overwrite = overwrite
        self.duration = duration
        self.volume = volume
        self.name = name
        self.form = form
        self.v_mode = "rel"
        self.f_mode = "rel"
        self.l_mode = "rel"
          
    def add_pattern(self, pattern: list) -> int:
        """
        Pattern structure
        [[base_frequency, base_length, base_velocity], 
        [instrument, frequency, length, velocity, effect**, effect_value**],
        [...],
        ...]
        Example:
        [[440, 1, 1]
        [3/4, 2/3, 1/100, 0],
        [1, 1, 100, 0]]
        """
        self.raw_pattern.append(pattern)
        return len(self.raw_pattern) - 1
    def add_inst(self, inst: str) -> int:
        """
        FFMpeg aevalsrc that support additional keywords:
        f|freq|frequency
        l|len|length
        v|vel|velocity
        ts|start
        te|end
        """
        self.raw_inst.append(inst)
        return len(self.raw_inst) - 1
    def __re_insert(self, freq, length, velocity, time_start, time_end, line): 
        current_inst = re.sub(r"(?<!\w)(f|freq|frequency)(?!\w)", str(freq), self.raw_inst[line[0]])
        current_inst = re.sub(r"(?<!\w)(l|len|length)(?!\w)", str(length), current_inst)
        current_inst = re.sub(r"(?<!\w)(v|vel|velocity)(?!\w)", str(velocity), current_inst)
        current_inst = re.sub(r"(?<!\w)(ts|start)(?!\w)", str(time_start), current_inst)
        current_inst = re.sub(r"(?<!\w)(te|end)(?!\w)", str(time_end), current_inst)
        self.raw_exp.append("".join(["(", f"between(t, {time_start}, {time_end})*", current_inst, ")"]))
    def __eval(self) -> str:
        overwrite_tag = ""
        if self.overwrite:
            overwrite_tag = "-y "
        pattern_length = []  
        for current_pattern in self.raw_pattern:
            freq = 1
            length = 1
            velocity = 1
            time_start = 0
            time_end = 0
            for n, line in enumerate(current_pattern):
                if n == 0:
                    freq = line[0]
                    length = line[1]
                    velocity = line[2]
                    continue
                voice_life = True
                if len(line) > 1:
                    if self.f_mode[0] == "c":
                        freq = line[1]
                    else:
                        freq *= line[1]
                if len(line) > 2:
                    if self.l_mode[0] == "c":
                        length = line[2]
                    else:
                        length *= line[2]
                time_end += length
                if len(line) > 3:
                    if self.v_mode[0] == "c":
                        velocity = line[3]
                    else:    
                        velocity *= line[3]
                if len(line) > 4:
                    for i in range((len(line) - 4)//2):
                        note_fx = line[i+4]
                        note_fx_param = line[i+5]
                        if note_fx == 1:
                            self.__re_insert(freq*note_fx_param, length, velocity, time_start, time_end, line)

                if voice_life == True:
                    self.__re_insert(freq, length, velocity, time_start, time_end, line)
                time_start = time_end
            pattern_length.append(time_end)
        expr_inst = "".join(["+".join(self.raw_exp), "\':"])
        duration = 0
        if self.duration > 0:
            duration = self.duration
        elif self.duration == -1:
            duration = max(pattern_length)
        expr = (f"{self.start}"
                f"{overwrite_tag}"
                f"{self.aeval_init}"
                f"{expr_inst}"
                f"d={duration}\" "
                f"-filter:a volume={self.volume} "
                f"{self.name}.{self.form}")
        return expr
    def render(self):
        system(self.__eval())
    def play(self):
        self.render()
        if which("ffplay"):
            system("ffplay out.wav")
        elif which("termux-media-player"):
            system("termux-media-player play out.wav")
