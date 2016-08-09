Raspberry Pi Appointment Reminder
=================================
I often find myself missing appointments because I'm engrossed in my work or because I've switched to a different computer and can't hear the reminder ping on my work laptop. I created this project to give me a visual reminder, an obnoxious, silent countdown timer I can set on my desk to flash lights at me as a warning before my next meeting starts.

The project uses a network connected Raspberry Pi and a [Pimoroni Unicorn HAT](https://shop.pimoroni.com/collections/raspberry-pi/products/unicorn-phat) to display the reminder. The Pi will connect to Google Calendar and check periodically for upcoming appointments then display the following alerts:

* White @ 10 minutes
* Yellow @ 5 minutes
* Multi-color swirl @ 2 minutes

For this project, the alert is simply all LEDs in the array lit with the same color for a period. If you're adventurous, you can change the code to use any of the sample patterns included with the [Unicorn HAT Sample Code](https://github.com/pimoroni/unicorn-hat/tree/master/python/examples).


Required Components
=================================
For this project, I used the following components:

+ Raspberry Pi - I used a [Raspberry Pi 2 Model B](https://www.raspberrypi.org/), but most any Pi will work. Check the Unicorn HAT documentation for supported Pi devices.
+ Power Supply - [CanaKit 5V 2.5A Raspberry Pi 3 Power Supply / Adapter / Charger (UL Listed)](http://www.amazon.com/CanaKit-Raspberry-Supply-Adapter-Charger/dp/B00MARDJZ4) from Amazon.
+ [Pimoroni Unicorn HAT](https://shop.pimoroni.com/products/unicorn-hat) from Adafruit.
+ Raspberry Pi case - [Adafruit Raspberry Pi B+ / Pi 2 / Pi 3 Case - Smoke Base - w/ Clear Top](https://www.adafruit.com/products/2258) from Adafruit.

The only required component is the Unicorn HAT as the code in this project is hand crafted for that device. Otherwise, pick whatever Raspberry Pi device, case and power supply that works best for you.


Raspberry Pi Setup
=================================
To setup the hardware, complete the following steps:

+ Mount the Pimoroni Unicorn HAT on the Raspberry Pi device
+ Place the Pi in a case
+ Power it up!

When the Pi is all ready to go, update the device's software using the following commands:

	sudo apt-get update
	sudo apt-get upgrade

The first command updates the local software repositories and the second command updates the Pi OS and associated files. There’s a set of scientific libraries that are used in some of the Unicorn HAT code in the project, so you will need to install them using the following command:

    sudo apt-get install python-numpy

Next, create a directory for the project's files. Open a terminal window and execute the following commands:

	mkdir pi_remind
	cd pi_remind

Finally, copy the project's Python source code to the new folder and extract the files using the following commands:

	wget https://github.com/johnwargo/pi_remind/archive/master.zip
	unzip -j master.zip

If all goes well, you should see the following files in the folder:

- `LICENSE`
- `pi_remind.desktop`
- `readme.md` (this file)
- `remind.py`
- `setup.py`
- `start_remind.sh`

Before you can use the project's software, you have to setup an account with Google in order to be able to execute the Google Calendar APIs used in this project. To setup your account, read the [Google Calendar API Python Quickstart](https://developers.google.com/google-apps/calendar/quickstart/python).

Download your Google Calendar API application's `client_secret.json` file in the project folder. Be sure to name the downloaded file using that file name. You'll need it to authorize the app to access your Google Calendar and that file name is hard coded into the Python app.

As part of that process, you'll install the [Google Calendar API Python files](https://developers.google.com/api-client-library/python/start/installation) along with date handling libraries using the following command:

    sudo pip install --upgrade google-api-python-client python-dateutil pytz

Install the Unicorn HAT libraries following the instructions on the [Pimoroni web site](http://learn.pimoroni.com/tutorial/unicorn-hat/getting-started-with-unicorn-hat):
basically opening a terminal window and executing the following command:

    curl -sS get.pimoroni.com/unicornhat | bash

With everything in place, execute the reminder app using the following command:

    sudo python ./remind.py

Before the app can access the calendar, you'll need to authorize the app to use the Google Calendar API for your calendar account. When you launch the app for the first time (using the command shown above) the browser will launch and walk you through the process. With that complete, PI Remind should start watching your calendar for events.

Note: if you ever change Google calendars (from a work to a personal calendar or from one work calendar profile to another) you'll need to whack the existing access token created during the initial startup or the Pi Reminder app. Instructions for deleting this token are available on [johnwargo.com](http://www.johnwargo.com/index.php/microcontrollers-single-board-computers/pi-reminder-%E2%80%93-delete-google-calendar-access-authorization-token.html).


Additional Files
---------------------------------
The project includes several files that are not directly related to the Pi Reminder capabilities: 

- `pi_remind.desktop`
- `setup.py`
- `start_remind.sh`

The `setup.py` file is a python setup script. Pi Reminder is my first Python app, so I created that file as I figured how all of this worked. You don't 'need' it, using the instructions included here, you'll be able to get the app running.

The `pi_remind.desktop` and `start_remind.sh` files implement two possible ways to automate the startup of the `pi_remind` app.  I looked around for the 'right' way to autostart a Python app on the Pi and didn't find one. These two files were just me hacking away at finding a good way to get this working. One way to start the app is to put the `pi_remind.desktop` file in the Pi's `~/.config/autostart` folder. The file is a text file, so be sure to update it with the target folder where you installed the Pi Reminder files. `start_remind.sh` is a shell script you can execute on startup to start Pi Remind.
  

Known Issues
=================================
Reminders are triggered for canceled events. If you have your Google Calendar configured to show deleted events, pi_remind will flash its lights for those events as well. I've tried setting `showDeleted` to `false` in the call to get the calendar entry list from Google, but it does not seem to have an effect (in my testing anyway).


Revision History
=================================
2016-08-09: Added code to set the status light after flashing the LEDs. Otherwise, within 10 minutes of an event, you wouldn't see the status light indicating that the app is running. 

2016-06-28: Added red LED option for current_activity_light when there's a failure connecting to Google. Added this for a visual indicator when errors occur and the user misses the red flash.
 
2016-06-27: Fixed the progress indicator LED so it cycles from left to right and so it leaves the light blue on success so you can tell at a glance that the Pi is still running the code.

2016-06-20: Reader John McCabe submitted a patch to fix an issue where events with empty descriptions were causing an error. If the app encounters an event without a summary, it sets the output to `No Title`.

2016-06-18: Reader John McCabe submitted a patch to update the code so it takes into account the local timezone when working with dates/times. In my original code, I hardcoded my time zone into UTC conversions and intended to document this so others could update it to match their current timezone. John implemented a better solution, using some Python Date/Time utilities to properly reflect current time zone into calculations.  


***

You can find information on many different topics on my [personal blog](http://www.johnwargo.com). Learn about all of my publications at [John Wargo Books](http://www.johnwargobooks.com). 