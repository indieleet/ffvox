from ffvox import Tracker 
tracker = Tracker()
tracker.add_inst("0.5*mod(t,1)*lt(mod(t,2),1)*((0.25)-mod(t,(0.25)))*(-1+random(0)*2)")
tracker.duration = 3
tracker.play()
