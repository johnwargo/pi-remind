Raspberry Pi Appointment Reminder
=================================
I often find myself missing appointments because I'm engrossed in my work or because I've switched to a different computer and can't hear the reminder ping on my work laptop. I created this project to give me a visual reminder, an obnoxious, silent countdown timer I can set on my desk to flash lights at me as a warning before my next meeting starts.

The project uses a network connected Raspberry Pi and a [Pimoroni Unicorn HAT](https://shop.pimoroni.com/collections/raspberry-pi/products/unicorn-phat) to display the reminder. The Pi will connect to Google Calendar and check periodically for upcoming appointments then display the following alerts:

* White @ 10 minutes
* Yellow @ 5 minutes
* Red @ 2 minutes

Required Components
==================
This project uses the following components:

+ Raspberry Pi - I used a [Raspberry Pi 2 Model B](https://www.raspberrypi.org/), but any Pi will work.
+ Power Supply - [CanaKit 5V 2.5A Raspberry Pi 3 Power Supply / Adapter / Charger (UL Listed)](http://www.amazon.com/CanaKit-Raspberry-Supply-Adapter-Charger/dp/B00MARDJZ4).
+ [Pimoroni Unicorn HAT](https://shop.pimoroni.com/products/unicorn-hat)
+ Raspberry Pi case - [Adafruit Raspberry Pi B+ / Pi 2 / Pi 3 Case - Smoke Base - w/ Clear Top](https://www.adafruit.com/products/2258)

Raspberry Pi Setup
==================
Attach the Pimoroni Unicorn HAT to the Raspberry Pi device
Put the Pi into a case
Plug it in
Optionally: assign a static IP address to the Pi.

Project Setup
==================
Before you begin, you must first setup an account with Google in order to be able to execute the Google Calendar APIs used in this project. So, go here and do some stuff:

Place your Google Calendar API `client_secret.json` file in the project folder. You'll need it to authorize the app to access your Google Calendar.

Installation
==================

Install the Unicorn HAT libraries following the instructions on the [Pimoroni web site](http://learn.pimoroni.com/tutorial/unicorn-hat/getting-started-with-unicorn-hat):
basically opening a terminal window and executing the following command:

    curl -sS get.pimoroni.com/unicornhat | bash

Install google's api client - https://developers.google.com/api-client-library/python/start/installation

    sudo pip install --upgrade google-api-python-client

The OAUTH and HTTP libraries should install automatically when the Google Calendar APIs install, but if not, you can install them using the following commands:

    sudo pip install httplib2

    sudo pip install oauth2client


***

You can find information on many different topics on my [personal blog](http://www.johnwargo.com). Learn about all of my publications at [John Wargo Books](http://www.johnwargobooks.com). 