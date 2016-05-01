Raspberry Pi Appointment Reminder
=================================
I often find myself missing appointments because I'm engrossed in my work or because I've switched to a different computer and can't hear the reminder ping on my work laptop. I created this project to give me a visual reminder, an obnoxious, silent countdown timer I can set on my desk to flash lights at me as a warning before my next meeting starts.

The project uses a network connected Raspberry Pi and a [Pimoroni Unicorn HAT](https://shop.pimoroni.com/collections/raspberry-pi/products/unicorn-phat) to display the reminder. The Pi will connect to Google Calendar and check periodically for upcoming appointments then display the following alerts:

* White @ 10 minutes
* Yellow @ 5 minutes
* Red @ 2 minutes
* Flashing Red @ 0 minutes and beyond

User presses a button to silence the current alert. Long press to cancel reminder completely 

If there's no appointment on the calendar immediately before the next appointment, perhaps we can add a speaker or buzzer to the system and have it make an audible notification as well. Or, perhaps add a physical switch to enable/disable this feature.
  
Optionally, have the system send a text message reminder as well (using Twilio).

Installation
============

pip install http2lib

pip install oauth2client
 
Install google's api client - https://developers.google.com/api-client-library/python/start/installation



***

You can find information on many different topics on my [personal blog](http://www.johnwargo.com). Learn about all of my publications at [John Wargo Books](http://www.johnwargobooks.com). 