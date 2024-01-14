from ffvox import Tracker 
tracker = Tracker()
tracker.add_inst("l/2-mod((t-start),(l/2))*gt(t-start,l/2)*(-1+random(0))")
tracker.add_inst("l/2-mod((t-start),(l/2))*v*sin(2*PI*t*freq+2*PI*t*f*0.5*(l/16-mod((t-start),(l/4))))")
tracker.add_pattern([[330, 1, 1],
[1, 1, 1, 1],
[1, 1, 1/2, 1],
[1, 1/2, 1, 1]])
synth_pattern = [[330, 1, 1],
[0, 1, 1, 1],
[0, 3/2, 1, 1/1000],
[0, 5/6, 3/4, 500],
[0, 2/3, 1, 2]]
synth_pattern.extend(synth_pattern.copy()[1:][::-1])
tracker.add_pattern(synth_pattern)
tracker.play()
