# Clockwise - Intel IoT Roadshow 2015
Clockwise is your next intelligent alarm clock.

It wakes you up by saying out loud the weather conditions and your Google Calendar events for the day in a Bluetooth Speaker.

![Clockwise picture](http://julianaklulo.github.io/images/clockwise.jpg)

Powered by Intel Edison and using the Grove Starter Kit IoT Edition, this project was developed at Intel IoT Roadshow 2015 in November/2015 at São Paulo, Brazil.

## Components
* Intel Edison with Arduino Breakout Board
* Grove Base Shield
* Grove Push Button (x2)
* Bluetooth Speaker

## Under the Hood
The base of this project is a python script: using APIs, like pywapi (API for weather report in python), Google Calendar API (to fetch the events), and VoiceRSS (text-to-speech REST API), to gather useful information and say it out loud in a Bluetooth speaker, so you can make your daily plans without even getting out of bed! This can be helpful for blind or disabled people, and future versions of this project may be gesture controlled (using Intel Real Sense), instead of having actual buttons.

## How it Works
You set an event in your Google Calendar called 'Alarm' to happen everyday at the time you want Clockwise to wake you up. When the time comes, a ringtone, chosen by you, will start playing in a Bluetooth speaker, and you can press a Grove button to stop it, or the other one to snooze it. If you snooze, it will wait a couple minutes and after that it'll start ringing again. When you finally press stop, a report, consisting of some weather informations (local temperature, maximum and minimum temperature for the day, local forecast, and chance of rain), and the events for the day, set in your Google Calendar account, will be spoken in the Bluetooth speaker, so you won't miss anything from your agenda!

## Demonstration
Video demonstration (in pt-br) available at [Intel's YouTube Channel](https://www.youtube.com/watch?v=BQpnZ6N41Jw).

## Instructions
Step-by-step instructions available at [Instructables](http://www.instructables.com/id/Clockwise-an-Intelligent-Alarm-Clock-Powered-by-In/).

## Attention
In order for this to work, you need to download and install some packages to decode mp3, for this you have to set up your own repository for Yocto Linux and bitbake the packages gst-plugins-ugly and gst-plugins-ugly-mad, since they aren't distributed in the official and unofficial repositories for Intel Edison because you can get in trouble in some places if you get caught distributing them.
