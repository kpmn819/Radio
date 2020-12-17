# Import the module and threading
from pyky040 import pyky040
import threading

# Define your callback
def my_callback(scale_position):
    print('Hello world! The scale position is {}'.format(scale_position))

# Init the encoder pins
my_encoder = pyky040.Encoder(CLK=17, DT=18, SW=26)

# Setup the options and callbacks (see documentation)
my_encoder.setup(scale_min=0, scale_max=100, step=1, chg_callback=my_callback)

# Create the thread
my_thread = threading.Thread(target=my_encoder.watch)

# Launch the thread
my_thread.start()

# Do other stuff
print('Other stuff...')
while True:
    print('Looped stuff...')
    sleep(1000)
# ... this is also where you can setup other encoders!

# Mess with the encoder...
# > Other stuff...
# > Looped stuff...
# > Hello world! The scale position is 1
# > Hello world! The scale position is 2
# > Hello world! The scale position is 3
# > Looped stuff...
# > Hello world! The scale position is 2