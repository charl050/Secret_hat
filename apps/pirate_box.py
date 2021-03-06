from lib.init import *
from lib import globals

import os
import time
import psutil
import subprocess



"""
This application allows to start or stop apache2 service, to share files between connected clients
"""

def main(color1, color2, speed):

    """
    Args :
        color1 (list or tuple) : rgb color code of titles
        color2 (list or tuple) : rgb color code of subtitles
        speed (float) : speed of the scrolling of message
    """

    passed()
    while globals.run:

        # Start or stop the service
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 0:
            show_message_break("1:Start/Stop", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                if os.system('systemctl is-active apache2') == 0:
                    os.system('service apache2 stop')
                    while globals.direction != 'middle':
                        show_message_break("Pirate box stopped", color2, speed)
                        get_joystick()
                    passed()
                else:
                    if os.system('service apache2 start') == 0:
                        globals.pirate_box_start_time = time.time()
                        while globals.direction != 'middle' :
                            show_message_break("Pirate box started", color2, speed)
                            get_joystick()
                        passed()
                        if os.system('systemctl is-active hostapd') == 0:
                            while globals.direction != 'middle' :
                                show_message_break("Please start AP in Settings/Wifi/Hotspot", color2, speed)
                                get_joystick()
                            passed()
                    else:
                        while globals.direction != 'middle':
                            show_message_break("Can't start apache2 service! Press OK", color2, speed)
                            get_joystick()
                        passed()

        passed(1)

        # Display informations (number of users connected and starting time)
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 1:
            show_message_break("2:Infos", color1, speed)
            get_joystick()
            if globals.direction == 'middle' :
                passed()
                try:                # Check if the service has started
                    pid = os.popen('pgrep apache2').read().split('\n')
                    pid.reverse()
                    pid = pid[1]

                    users = int(subprocess.Popen("netstat -ant | grep ESTABLISHED | grep :80 | wc -l", shell=True, stdout=subprocess.PIPE).stdout.read())

                    while globals.direction != 'middle':
                        show_message_break("Started:{} min".format(round((time.time()-globals.pirate_box_start_time)/60, 2)), color2, speed)
                        get_joystick()
                    passed()

                    while globals.direction != 'middle':
                        show_message_break("Users:{}".format(users), color2, speed)
                        get_joystick()
                    passed()

                except:
                    while globals.direction != 'middle' :
                        show_message_break("Piratebox not started", color2, speed)
                        get_joystick()
                    passed()


        passed(1)
    passed()
