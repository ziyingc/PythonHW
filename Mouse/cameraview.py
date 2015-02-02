from __future__ import print_function

import numpy as np
import xinput
import gnoomutils as gu
import sched, time
s = sched.scheduler(time.time, time.sleep)

readpath = "/home/kemerelab"
mice = xinput.find_mice(model="Mouse")
m = [mice[0]]

for mouse in m:
    xinput.set_owner(mouse) # Don't need this if using correct udev rule
    xinput.switch_mode(mouse)


if len(mice):
    s1, conn1, addr1, p1 = \
    gu.spawn_process("\0mouse0socket", 
                  ['%s/evread/readout' % readpath, '%d' % mice[0].evno, '0'])
    conn1.send(b'start')

    gu.recv_ready(conn1)

    conn1.setblocking(0)

else:
    print("No Mice")

print("Printout Start")
def readposition(sc):

    gu.keep_conn([conn1])
    
    if conn1 is not None:
        t1, dt1, x1, y1 = gu.read32(conn1)
        print(x1,y1)
    else:
        t1, dt1, x1, y1 = np.array([0,]), np.array([0,]), np.array([0,]), np.array([0,])
    print("next")
    sc.enter(0.1, 1, readposition, (sc,))

s.enter(0.1, 1, readposition, (s,))
s.run()
