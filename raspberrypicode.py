import RPi.GPIO as GPIO

import time

import CapturingPath



GPIO.setwarnings(False)


# Define GPIO For Driver motors


GPIO.setmode(GPIO.BOARD)


GPIO.setup(7, GPIO.OUT)

GPIO.setup(11, GPIO.OUT)

GPIO.setup(13, GPIO.OUT)

GPIO.setup(15, GPIO.OUT)



# Define GPIO for ultrasonic Right


GPIO_TRIGGER_RIGHT = 33

GPIO_ECHO_RIGHT = 35

GPIO.setup(GPIO_TRIGGER_RIGHT, GPIO.OUT)  # Trigger > Out

GPIO.setup(GPIO_ECHO_RIGHT, GPIO.IN)      # Echo < In





# Define GPIO for ultrasonic Left


GPIO_TRIGGER_LEFT = 38

GPIO_ECHO_LEFT = 40

GPIO.setup(GPIO_TRIGGER_LEFT, GPIO.OUT)  # Trigger > Out

GPIO.setup(GPIO_ECHO_LEFT, GPIO.IN)      # Echo < In







# Functions for driving


def goforward():

    cleargpios()

    GPIO.output(7,False)

    GPIO.output(13,False)


    GPIO.output(11, True)

    GPIO.output(15, True)

    print("forward")





def turnleft():

    cleargpios()

    GPIO.output(7,False)

    GPIO.output(13,False)


    GPIO.output(11, True)

    GPIO.output(15, False)

    time.sleep(0.8)

    GPIO.output(11, False)

    print("left")





def turnright():

    cleargpios()

    GPIO.output(7,False)

    GPIO.output(13,False)


    GPIO.output(15, True)

    GPIO.output(11, False)

    time.sleep(0.8)

    GPIO.output(15, False)

    print("right")



def gobackward():

    cleargpios()

    GPIO.output(11,False)

    GPIO.output(15,False)


    GPIO.output(7, True)

    GPIO.output(13, True)

    print("back")




def stopmotors():

    GPIO.output(15, False)

    GPIO.output(11, False)

    GPIO.output(7, False)

    GPIO.output(13, False)

    print("stop")





def rightobstacle():


    # Set trigger to False (Low)


    GPIO.output(GPIO_TRIGGER_RIGHT, False)


    # Allow module to settle


    time.sleep(0.2)


    # Send 10us pulse to trigger


    GPIO.output(GPIO_TRIGGER_RIGHT, True)



    time.sleep(0.00001)

    GPIO.output(GPIO_TRIGGER_RIGHT, False)

    start = time.time()


    while GPIO.input(GPIO_ECHO_RIGHT) == 0:

        start = time.time()


    while GPIO.input(GPIO_ECHO_RIGHT) == 1:

        stop = time.time()


    # Calculate pulse length


    elapsed = stop - start


    # Distance pulse travelled in that time is time


    # Multiplied by the speed of sound (cm/s)


    distance = elapsed * 34000 / 2  # Distance of both directions so divide by 2

    print "Right Distance : %.1f" % distance

    return distance






def leftobstacle():


    # Set trigger to False (Low)


    GPIO.output(GPIO_TRIGGER_LEFT, False)


    # Allow module to settle


    time.sleep(0.2)


    # Send 10us pulse to trigger


    GPIO.output(GPIO_TRIGGER_LEFT, True)

    time.sleep(0.00001)

    GPIO.output(GPIO_TRIGGER_LEFT, False)

    start = time.time()


    while GPIO.input(GPIO_ECHO_LEFT) == 0:

        start = time.time()


    while GPIO.input(GPIO_ECHO_LEFT) == 1:

        stop = time.time()


    # Calculate pulse length


    elapsed = stop - start


    # Distance pulse travelled in that time is time


    # Multiplied by the speed of sound (cm/s)


    distance = elapsed * 34000 / 2  # Distance of both directions so divide by 2

    print "Left Distance : %.1f" % distance

    return distance




# Check right obstacle and turn left if there is an obstacle


def checkanddriveright():


    while rightobstacle() < 20:

        stopmotors()

        turnleft()

    goforward()

    print("moveleft")






# Check left obstacle and turn right if there is an obstacle


def checkanddriveleft():


    while leftobstacle() < 20:

        stopmotors()

        turnright()

    goforward()

    print("moveright")






# Avoid obstacles and drive forward


def obstacleavoiddrive():


    goforward()

    start = time.time()


    # Drive 5 minutes


    while start:
 
        if rightobstacle() < 20:

            stopmotors()
 
           checkanddriveright()


        elif leftobstacle() < 20:

            stopmotors()

            checkanddriveleft()



# Clear GPIOs, it will stop motors
       

    cleargpios()







def cleargpios():


    print "clearing GPIO"

    GPIO.output(7, False)

    GPIO.output(11, False)

    GPIO.output(13, False)

    GPIO.output(15, False)

    GPIO.output(33, False)

    GPIO.output(38, False)

    print "All GPIOs CLEARED"







def main():


    # First clear GPIOs


    cleargpios()

    print "start driving: "

    # Start obstacle avoid driving

    obstacleavoiddrive()






if __name__ == "__main__":

    main()
