from ffvox import Tracker 
tracker = Tracker()
tracker.volume = 0.25
tracker.add_inst("(mod((t-start),(l/8))/(l/8))*gt(t-start,l/2)*(-1+random(0))")
tracker.add_inst("(mod((t-ts),(l/2))/(l/2))*v*sin(2*PI*t*freq+2*PI*t*f*0.1*(mod((t-start),(l/16))/(l/16)))")
tracker.add_pattern([[730, 1, 1],
[0, 1, 1, 1],
[0, 1, 1/2, 1],
[0, 1/2, 1, 1],
[0, 3, 3, 1],
[0, 1, 1/2, 1],
[0, 1/2, 1, 1]])
synth_pattern = [[530, 3, 1],
[1, 1, 1, 1, 1, 3, 1, 5, 1, 7, 1, 11],
[1, 2/2, 1, 1/2],
[1, 2/6, 3/4, 1/2],
[1, 2/3, 1, 2],
[1, 5/6, 3/4, 1/2],
[1, 2/3, 1, 2],
[1, 5/8, 1, 1],
[1, 5/8, 1, 1],
[1, 1, 1/3, 1],
[1, 1, 1, 1]]
synth_pattern.extend(synth_pattern.copy()[1:][::-1])
tracker.add_pattern(synth_pattern)
tracker.play()
