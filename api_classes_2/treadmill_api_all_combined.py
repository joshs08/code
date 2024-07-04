#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:38:21 2024

@author: colin
"""
import evdev 
from selectors import DefaultSelector, EVENT_READ
import time


# use this function
def process_data_user(self, data):
    # check if state changed to imaging_on
    imaging = [state.name == "imaging_on" for state in data["states"]]
    if imaging == [True]:
        self.set_variable("treadmill_begun", True)
        tt = time.time()
        self.print_message("Time is {}".format(tt))#prints with timestamp
        
        
        length = 1000000
        duration = 10
        # instantiate arrays to hold x and y deltas and timestamps for each mouse
        g502ax = []
        g502ay = []
        g502bx = []
        g502by = []
        
        # append to arrays
        def add_event (d, delta, t):
            d.append ([delta,t])
        
        
        # Print all devices and select the mouse device    
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        
        for device in devices:
            print(device.path, device.name, device.phys)
            print (device.name.lower())
            if ('gaming mouse' in device.name.lower()) and ('keyboard' not in device.name.lower()):
                #we keep each mouse in the same USB port and thus as a or b. 
                #NB use top two USB ports at rear
                if '14.0-7' in device.phys:
                    g502a = device
                    patha = device.path
                    print ("a found")
                elif '14.0-8' in device.phys:
                    g502b = device
                    pathb = device.path
                    print ("b found")
            # elif ('wired multimedia keyboard' in device.name.lower()) and ('mouse' not in device.name.lower()) and ('control' not in device.name.lower()):
            #     keyboard = device
            #     print ("keyboard found")
        
        # "selectors" method of reading from devices simultaneously (see evdev tutorial)
        selector = DefaultSelector()
        selector.register(g502a, EVENT_READ)
        selector.register(g502b, EVENT_READ)
        
        #to not move cursor
        # try:
        #     g502a.grab()
        #     g502b.grab()
        # except:
        #     print ("mice already grabbed")
        #     g502a.ungrab()
        #     g502b.ungrab()
        #     g502a.grab()
        #     g502b.grab()
            
        # currenttime = time.time()
        # elapsedtime = currenttime-starttime
        
        while True:
            for key, mask in selector.select():
                device = key.fileobj
                for event in device.read():
                    # currenttime = time.time()
                    # elapsedtime = currenttime-starttime
                    #separate events by mouse 
                    if device.path == patha:
                        #separate x and y events
                        if event.code == evdev.ecodes.REL_X:
                            # synchronisation events (which the mice output when x and y movements coincide) 
                            # have the same event code as rel_x (i.e. 0). event.value is delta
                            if event.value != 0:
                                add_event(g502ax, event.value, event.timestamp())
                                #print(f"X full: {evdev.categorize(event)}")