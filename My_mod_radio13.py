#!/usr/bin/python3
# 
# Version 4: removed commented debugging print statements
# added noise
# V-5: changed the way noise is controlled
# V-6: start adding code to run graphics
# V-7: move graphics initialization here
# V-8: eyeball is now correct added manual tuning buttons
# V-9: new encoder arrived and it sort of works, steps wrong when fast
# V-10 stable but jumps back and can't handle high speed
# V-11 simulates what it will do with EM402 chip
# V-12 removed button push original code. Changed testing module to blit_module
# V-13 moved port assignments up just after GPIO import
import sys, pygame
from pygame.locals import *
import pygame.mixer
import time
import datetime
import subprocess
import os
import glob
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
enc_val = 10  # starting point for the running directional enc_val

# GPIO Ports
Enc_A = 13  # Encoder input A: input GPIO 13 (active high)
Enc_B = 19  # Encoder input B: input GPIO 19 (active high)
Enc_pb = 16 # Encoder push button
import random
import blit_module

# set up these global variables
enc_min = 0
enc_max = 256
enc_val = 0
enc_dir_up = True
enc_prev = 10
enc_int = enc_max/2 # set mid scale for now
enc_int_min = 0
enc_div = 8 # guess
enc_int_max = enc_max * enc_div

angle = 0 # angle runs from -80 to +80 degrees
# vol_taper controls the program audio levels
vol_taper = [100,100,100,95,95,90,90,85,85,80,80,70,60,40,20]
# vol_noise is an inverse, sort of than vol_taper it is scaled in noise()
vol_noise = [0,0,40,50,60,70,80,85,90,90,95,95,100,100,100]
# this is a mapped list of the eyeball files

shuffle = False
play_list = '/var/lib/mpd/playlists/playlist.m3u'
# set up display
#pygame.init()
#screen_width=841
#screen_height=640
#bgColor = (255, 255, 255)
#size=(screen_width, screen_height)
#display = pygame.display.set_mode(size)
# files used by graphics
eye0_img = 'Eyeball0.png'
eye1_img = 'Eyeball1.png'
eye2_img = 'Eyeball2.png'
eye3_img = 'Eyeball3.png'
eye4_img = 'Eyeball4.png'
eye5_img = 'Eyeball5.png'
eye6_img = 'Eyeball6.png'
needle_img = 'Needle.png'
radio_img = 'Radio.png'
mask_img = 'Mask_Needle.png'
# load up the images
eye0 = pygame.image.load(eye0_img).convert_alpha()
eye1 = pygame.image.load(eye1_img).convert_alpha()
eye2 = pygame.image.load(eye2_img).convert_alpha()
eye3 = pygame.image.load(eye3_img).convert_alpha()
eye4 = pygame.image.load(eye4_img).convert_alpha()
eye5 = pygame.image.load(eye5_img).convert_alpha()
eye6 = pygame.image.load(eye6_img).convert_alpha()
eye_list = [eye0,eye0,eye1,eye1,eye2,eye2,eye3,eye3,
            eye4,eye4,eye5,eye5,eye5,eye6,eye6,eye6]
eye_now = eye_list[0] # seed this value for now
needle = pygame.image.load(needle_img).convert_alpha()
mask = pygame.image.load(mask_img).convert_alpha()
radio = pygame.image.load(radio_img).convert_alpha()

#BackGround = blit_module.Background(radio_img, [0,0])
#blit_module.display.blit(BackGround.image, BackGround.rect)
#  below is for debug only
#pygame.display.flip()    


# --------------------- Begin Functions and Methods --------------------------------------

def initialize_mpc():
    subprocess.call("mpc random off", shell=True)
    subprocess.call("mpc clear", shell=True)
    subprocess.call("mpc volume 100", shell=True)
    subprocess.call("mpc update ", shell=True)
    subprocess.call("mpc load playlist", shell=True)
# -------- end initialize_mpc ---------------

def get_blit(angle):
    # called by encoder code send it off to be blitted
    blit_module.blit_em(radio,needle,mask,eye_now,angle)
    #pass
    



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

    



def get_ports():
    clk.read_port()
    dt.read_port()



def tuner(enc_val,angle):
    # check to see if it is approaching
    # the end stops are checked prior in enc_move
    # so we don't get called if on stop
    global playing
    prev_playing = playing

    play_true = []
    
    get_blit(angle)
    #print('tuner has an angle of: ',angle)
    
    # go through the list
    for i in range(0, len(freq_list)):
        diff = abs(freq_list[i] - enc_val)

        # check if close
        if diff > 16:
            # play_true is a list that shows which station is in range
            # there will only be one True at a time
            play_true.append(False)
            playing = False
            
        else:
            play_true.append(True)
            diff_vol = diff
            
            
    print('Frequencies are ', freq_list, ' Current freq= ',enc_val)
    # test the list for any True

    if True in play_true:
        playing = True
        # we found one
        # track both the prev_playing and playing
        # so to issue a play command once
        #print('entering ',playing, ' prev ', prev_playing)

        
        if prev_playing != playing:
            station = str(play_true.index(True) + 1)
            subprocess.call("mpc play " + station, shell=True)
            print('play command issued ', play_true.index(True) + 1)
            
        # remember the station index goes from 1 not 0
        eye_now = tune_eye(diff)
        #print('still playing, diff is:', diff_vol)
        
        vol_control(diff_vol)
    else:
        playing = False
        if prev_playing == True:
            print('SENDING mpc STOP')
            subprocess.call("mpc stop ", shell=True)
    return None

def tune_needle(enc_val):
    # scale 256 to +- 80 degrees
    angle = int((enc_val * -.63) + 80)
    return angle
    

def tune_eye(diff):
    # called by tuner returns a blit object
    global eye_now
    if diff > 15:
        # wide open
        # remember it is the arry index not the eye#
        eye_now = eye_list[15]
    else:
        eye_now = eye_list[diff]
    #print('asking for eyeball: ',diff)
    return eye_now


def home_sta(port):
    # set home station for push button
    # 
    tune_sta(0)
    
    
def tune_sta(sta_num):
    # tune to a specific station
    global enc_val
    global enc_prev
    freq = int(freq_list[sta_num])
    print('home =',freq)
    enc_val = freq
    enc_prev = freq - 1
    station = str(sta_num + 1)
    # remember station index 1
    subprocess.call("mpc play " + station , shell=True)
    subprocess.call("mpc volume 100", shell=True)

def vol_control(diff_vol):
    
    # the closer to the station the higher the volume
    if diff_vol in range(0,15):
        # get the right file for the tuning eye
        eye_now = tune_eye(diff_vol)
        
        vol_val = str(vol_taper[diff_vol])
        subprocess.call("mpc volume " + vol_val, shell=True)
        noise(vol_val, diff_vol)
    return None

def noise(vol_val, diff_vol):
    noise_prev = noise_now
    noise_val = 100 - int(vol_val) # set the volume nomatter what
    
    if int(vol_val) != 100:
        # Pause the noise if station at full volume
        if noise_prev == False:
            # start playing noise
            
            pygame.mixer.music.unpause()
            # use the values in vol_noise to control noise level
            scale_vol = vol_noise[diff_vol] / 100
            #print('!!!!!!!! scale_vol ', str(scale_vol), ' diff_vol=',diff_vol)
            
            pygame.mixer.music.set_volume(scale_vol)
            
            
        noise_prev = False
    else:
        noise_prev = True
        # Pause play
        pygame.mixer.music.pause()
        print('Static stopped')


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
            
            if abs((parsme[i] - parsme[x])) < 20:
                good_list = False
    return good_list
    

    
# ----------------------------- Ports and variables ------------------------        

# find the number of station entries in the file
sta_count = fileitems(play_list)

# ----------------------------- Rotary Encoder Code -------------------------------



def init():
    '''
    Initializes a number of settings and prepares the environment
    before we start the main program.
    '''
    print("Rotary Encoder")

    GPIO.setwarnings(True)

    # Use the Raspberry Pi BCM pins
    GPIO.setmode(GPIO.BCM)

    # define the Encoder switch inputs
    GPIO.setup(Enc_A, GPIO.IN) # pull-ups are too weak, they introduce noise
    GPIO.setup(Enc_B, GPIO.IN)
    GPIO.setup(Enc_pb, GPIO.IN)

    # setup an event detection thread for the A encoder switch
    GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotation_decode)
    GPIO.add_event_detect(Enc_B, GPIO.RISING, callback=rotation_decode)
    GPIO.add_event_detect(Enc_pb, GPIO.RISING, callback=home_sta, bouncetime=2) 
    #
    return



# Counter Code ---------------------------------
def rotation_decode(enc_calling):
    global enc_val
    global enc_max
    global enc_min
    global enc_prev
    global enc_int
    global enc_int_min
    global enc_int_max
    global enc_div
    global angle
    # use this to see if it moved
    
    # EM402 chip will deliver pulses for cw / ccw on two ports
    # need to add code to use the port number coming in 
    #enc_prev = enc_val
    #time.sleep(0.002) # extra .002 Sec de-bounce time
    # read both of the switches
    if enc_calling == Enc_A:
        print('called by A')

        enc_int += 1
        if enc_int > enc_int_max:
            enc_int = enc_max
        enc_val = int(enc_int/enc_div)
        print ("direction -> ", enc_val, 'Internal= ',enc_int)
 
        if enc_prev != enc_val:
            enc_val += 1
            angle = tune_needle(enc_val)
            print('New Encoder Value: ',enc_val)
            #tuner(enc_val, angle)
        
            return

    if enc_calling == Enc_B:
        print('called by B')

        enc_int -= 1
        if enc_int < enc_int_min:
            enc_int = enc_min
        enc_val = int(enc_int/enc_div)
        print ("direction <- ", enc_val, 'Internal= ',enc_int)
 
        if enc_prev != enc_val:
            enc_val -= 1
            angle = tune_needle(enc_val)
            print('New Encoder Value: ',enc_val)
            #tuner(enc_val, angle)
        
            return





# ----------------------------- Rotary Code End -----------------------------


# --------------------------- End Ports and variables -------------------


# ----------------------------Once per session setups --------------------

# Start up mpc audio server
initialize_mpc()


# make a list of 'frequencies' and check for conflicts
# just need to run this little ditty once per session
freq_list = create_freq(sta_count)
while check_list(freq_list)== False:
    print('bad list')
    # keep trying until you get a good one
    freq_list = create_freq(sta_count)
    
    
# ------------- Noise Player Setup ------------------------
# route noise audio to headphone jack
subprocess.call("amixer cset numid=3 1", shell=True)
pygame.mixer.init()
pygame.mixer.music.load("/usr/share/sounds/alsa/white_noise.wav")
pygame.mixer.music.set_volume(1.0)
# -1 is for endless play
pygame.mixer.music.play(-1)
# Run it for a couple of seconds
time.sleep(2)
pygame.mixer.music.pause()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

noise_now = False
print(check_list(freq_list))
# For debuging will be removed to tune home station
enc_val = int(input('Seed Value '))
enc_int = enc_val * enc_div

playing = False
# --------------------------- End setups ----------------------------


# =========================== Begin Main ===============================
def main():
    try:
        init()
        while 1:
            
            #press = input('Press a button: ')
            time.sleep(.1)
            global enc_val
            global enc_max
            global enc_min
            global enc_prev
            global angle
            # put some end stops on
            if enc_val > enc_max:
                enc_val = enc_max
            if enc_val < enc_min:
                enc_val = enc_min
            if enc_val != enc_prev:
                # only call the blitter if there is a change
                tuner(enc_val, angle)
                print('----- BLIT -----')
                enc_prev = enc_val
            for event in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    enc_val = enc_val -2
                    angle = tune_needle(enc_val)
                    print('Angle value= ',angle)
                    tuner(enc_val, angle)
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    enc_val = enc_val +2
                    angle = tune_needle(enc_val)
                    print('Angle value= ',angle)
                    tuner(enc_val, angle)            
            
            #tuner(enc_val)
                

    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        GPIO.cleanup()    

if __name__ == '__main__':
    main()


