#!/usr/bin/python
# 
# 
# 
#
import sys, pygame
from pygame.locals import *
import time
import datetime
import subprocess
import os
import glob
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import random

# set up these global variables
enc_min = 0
enc_max = 512
enc_val = 256
enc_dir_up = True
enc_prev = 10




pygame.init()



#other
#os.system("mount /dev/sda1 /mnt/usbdrive") #setup for USB drive if used

def initialize_mpc():
    subprocess.call("mpc random off", shell=True)
    subprocess.call("mpc clear", shell=True)
    subprocess.call("mpc volume 100", shell=True)
    subprocess.call("mpc update ", shell=True)
    subprocess.call("mpc load playlist", shell=True)
# -------- end initialize_mpc ---------------

shuffle = False
play_list = '/var/lib/mpd/playlists/playlist.m3u'


# read number of items in a playlist file to limit prev / next
def fileitems(file_name):
    file_items = open(file_name, encoding='utf-8')
    i = 0
    for items in file_items:
        print(items)
        i = i + 1
    print('Playlist has: ',i,' stations')
    file_items.close()
    return(i)
            
    
        


class Port(): #Capatilize Classes
    ''' This is my generic Port class supports set_type(), read_port(), change_stat() '''
    def __init__(self,pnum,ptype,pstat):
        self.pnum = pnum #port number
        self.ptype = ptype #input or output
        self.pstat = pstat #true (high) false (low)
        
    def set_type(self):# sets port as input or output
        if self.ptype == "input":
            GPIO.setup(self.pnum, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        else:
            GPIO.setup(self.pnum,GPIO.OUT)
            GPIO.output(self.pnum, GPIO.HIGH)
            self.pstat = 1
        
    def read_port(self): # check an input port
        if self.ptype == "input":
            self.pstat = GPIO.input(self.pnum)
            
        else:
            pass
            
 
    def change_stat(self):# toggle an output port
        if self.ptype == "output":
            if self.pstat == 1:
                self.pstat = 0
                GPIO.output(self.pnum, GPIO.LOW)
            else:
                self.pstat = 1
                GPIO.output(self.pnum, GPIO.HIGH)
        else:
            pass    

    

#define action on pressing buttons
def button(number):
    print("You pressed button "),number
    if number == 0:    #specific script when exiting
        subprocess.call("mpc stop ", shell=True)
        time.sleep(3)
        sys.exit()

    if number == 1: 
        subprocess.call("mpc play ", shell=True)
        

    if number == 2:
        subprocess.call("mpc stop ", shell=True)
        

    if number == 8:
        subprocess.call("mpc clear ", shell=True)
        subprocess.call("mpc load playlist ", shell=True)


    if number == 4:
        subprocess.call("mpc prev ", shell=True)

        

    if number == 5:
        subprocess.call("mpc next ", shell=True)

        

    if number == 6:
        subprocess.call("mpc volume -5 ", shell=True)
        

    if number == 7:
        subprocess.call("mpc volume +5 ", shell=True)
        

    if number == 9:
        subprocess.call("mpc random ", shell=True)
        global shuffle
        shuffle = (1,0)[shuffle]
        

    if number == 3:
        subprocess.call("mpc clear ", shell=True)
        subprocess.call("mpc update ", shell=True)
        subprocess.call("mpc add /", shell=True) 
        global mp3
        mp3 = 1


def get_ports():
    clk.read_port()
    dt.read_port()



def tuner(enc_val):
    # check to see if it is approaching
    # the end stops are checked prior in enc_move
    # so we don't get called if on stop
    global playing
    prev_playing = playing

    play_true = []
    #print('tuner freq_list= ', len(freq_list))
    # go through the list
    for i in range(0, len(freq_list)):
        
        diff = abs(freq_list[i] - 15)
        diff = abs(freq_list[i] - enc_val)
        #print('pre diff exit, diff = ', diff, ' i=',i, ' encoder= ',enc_val)

        # check if close
        if diff > 16:
            # play_true is a list that shows which station is in range
            # there will only be one True at a time
            play_true.append(False)
            playing = False            
        else:
            play_true.append(True)
            
    print('play_true is ',play_true, ' diff is ',diff)
    # test the list for any True

    if True in play_true:
        playing = True
        # we found one
        # track both the prev_playing and playing
        # so to issue a play command once
        print('entering ',playing, ' prev ', prev_playing)

        
        if prev_playing != playing:
            station = str(play_true.index(True) + 1)
            subprocess.call("mpc play " + station, shell=True)
            print('play command issued ', play_true.index(True) + 1)
        # remember the station index goes from 1 not 0
        print('still playing')
    else:
        playing = False
        if prev_playing != playing:
            subprocess.call("mpc stop ", shell=True)
    return None        


def get_rnd():
    # returns a random number that stays cofortably in band by 15
    global enc_min
    global enc_max
    return random.randint(enc_min + 15, enc_max - 15)
    #return random.randint(100,200)



def create_freq(sta_count):
    # pulls up random numbers in the range specified and returns a list
    # that contains one frequecy for each station
    freq_list = []
    
    freq_list = [get_rnd()]
    print('freq_list is now ' , freq_list)
    for i in range (1,sta_count):
        # we will check the list later for conflicts
        temp = (get_rnd())
        print(i, ' stations rnd= ',temp)
        freq_list.append(temp)
    freq_list = sorted(freq_list)
    print('list= ',freq_list)
    return freq_list


def check_list(parsme):
    # run through the list and look for any two numbers closer than we want (15)
    good_list = True
    for i in range(0,len(parsme)):
        look_for = parsme[i]
        for x in range(i+1, len(parsme)):
            #print('i =',i,' x= ',x)
            #print(abs(parsme[i] - parsme[x]))
            if abs((parsme[i] - parsme[x])) < 15:
                good_list = False
    return good_list
    

    
# ----------------------------- Ports and variables ------------------------        

# find the number of station entries in the file
sta_count = fileitems(play_list)

# ----------------------------- His Code -------------------------------
enc_val = 10  # starting point for the running directional enc_val

# GPIO Ports
Enc_A = 13  # Encoder input A: input GPIO 23 (active high)
Enc_B = 19  # Encoder input B: input GPIO 24 (active high)


def init():
    '''
    Initializes a number of settings and prepares the environment
    before we start the main program.
    '''
    print("Rotary Encoder Test Program")

    GPIO.setwarnings(True)

    # Use the Raspberry Pi BCM pins
    #GPIO.setmode(GPIO.BCM)

    # define the Encoder switch inputs
    GPIO.setup(Enc_A, GPIO.IN) # pull-ups are too weak, they introduce noise
    GPIO.setup(Enc_B, GPIO.IN)

    # setup an event detection thread for the A encoder switch
    GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotation_decode, bouncetime=2) # bouncetime in mSec
    #
    return



    # Counter Code
def rotation_decode(Enc_A):
    global enc_val
    global enc_max
    global enc_min
    global enc_prev
    # use this to see if it moved
    enc_prev = enc_val
    

    time.sleep(0.002) # extra 2 mSec de-bounce time

    # read both of the switches
    Switch_A = GPIO.input(Enc_A)
    Switch_B = GPIO.input(Enc_B)

    if (Switch_A == 1) and (Switch_B == 0) : # A then B ->
        enc_val += 1
        print ("direction -> ", enc_val)
        # at this point, B may still need to go high, wait for it
        while Switch_B == 0:
            Switch_B = GPIO.input(Enc_B)
        # now wait for B to drop to end the click cycle
        while Switch_B == 1:
            Switch_B = GPIO.input(Enc_B)
        return

    elif (Switch_A == 1) and (Switch_B == 1): # B then A <-
        enc_val -= 1
        print ("direction <- ", enc_val)
         # A is already high, wait for A to drop to end the click cycle
        while Switch_A == 1:
            Switch_A = GPIO.input(Enc_A)
        return

    else: # discard all other combinations
        
        return


# ----------------------------- His Code End -----------------------------


# --------------------------- End Ports and variables -------------------


# ----------------------------Once per session setups --------------------
# Inital value
#prev_dt = dt.read_port()
#prev_clk =clk.read_port()
initialize_mpc()

# make a list of 'frequencies' and check for conflicts
# just need to run this little ditty once per session
freq_list = create_freq(sta_count)
while check_list(freq_list)== False:
    print('bad list')
    # keep trying until you get a good one
    freq_list = create_freq(sta_count)
    
    

print(check_list(freq_list))
enc_val = int(input('Seed Value '))

playing = False
# --------------------------- End setups ----------------------------


# =========================== Begin Main ===============================
def main():
    try:
        init()
        while 1:
            
            #press = input('Press a button: ')
            time.sleep(1)

            
            tuner(enc_val)
                

    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        GPIO.cleanup()    

if __name__ == '__main__':
    main()


