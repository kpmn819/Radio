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

def enc_move(callback_port):
    global enc_max
    global enc_min
    global enc_val
    global enc_dir_up
    global prev_clk
    global prev_dt
    # lets put in a delay
    #time.sleep(3)
    print('called')
    get_ports()


    #do the calculations
    if dt.pstat == prev_dt:
            
        prev_clk = clk.pstat
        prev_dt = dt.pstat
        print(enc_val,' Down')
        enc_dir_up = False
        enc_val = enc_val -1 # counter clockwise
    else:
        enc_val = enc_val +1 # clockwise
        prev_clk = clk.pstat
        prev_dt = dt.pstat
        print(enc_val,' Up')
        enc_dir_up = True
    # add end stops
    if enc_val >= enc_max:
        enc_val = enc_max
    if enc_val <= enc_min:
        enc_val = enc_min
        

    # call tuner here
    prev_enc_dir = enc_dir_up
    tuner(enc_val)

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
# set some variables and setup ports
# find the number of station entries in the file
sta_count = fileitems(play_list)



# rotary encoder
# Ports are implimented as a class
clk = Port(19,'input',1)
clk.set_type()
dt = Port(13,'input',1)
dt.set_type()
GPIO.add_event_detect(clk.pnum, GPIO.BOTH, callback = enc_move, bouncetime = 100)

# --------------------------- End Ports and variables -------------------


# ----------------------------Once per session setups --------------------
# Inital value
prev_dt = dt.read_port()
prev_clk =clk.read_port()
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
        while 1:
            
            #press = input('Press a button: ')
            press = 1
            num = int(press)
            #button(num)
                #for event in pygame.event.get():# NEED BUTTON FUNCTIONS FOR THESE RIGHT NOW REPLACE LATER WITH ANALOG CONTROL
                        #if event.type == pygame.MOUSEBUTTONDOWN:
                                #print "screen pressed" #for debugging purposes
                                #pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
                                #print pos #for checking
                                #pygame.draw.circle(screen, red, pos, 2, 0) #for debugging purposes - adds a small dot where the screen is pressed
                                #on_click()
    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        GPIO.cleanup()    
#ensure there is always a safe way to end the program if the touch screen fails

            

        
    
time.sleep(0.2)


#################### EVERTHING HAS NOW BEEN DEFINED ###########################

#set size of the screen
#size = width, height = 640, 480
#screen = pygame.display.set_mode((size),pygame.FULLSCREEN)
#station_name()
#  #refresh the menu interface 
main() #check for key presses and start emergency exit


