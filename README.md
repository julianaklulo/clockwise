# Clockwise
Clockwise is your next intelligent alarm clock.

It wakes you up by saying out loud the weather conditions and your Google Calendar events for the day in a Bluetooth Speaker.

Powered by Intel Edison and using the Grove Starter Kit IoT Edition, this project was developed at Intel IoT Roadshow 2015 in November/2015 at São Paulo, Brazil.

## Components
* Intel Edison with Arduino Breakout Board
* Grove Base Shield
* Grove Push Button (x2)
* Bluetooth Speaker

## How to make it work
Step-by-step soon available at Instructables

## Attention
In order for this to work, you need to download and install some packages to decode mp3, for this you have to set up your own repository for Yocto Linux and bitbake the packages gst-plugins-ugly and gst-plugins-ugly-mad, since they aren't distributed in the official and unofficial repositories for Intel Edison because you can get in trouble in some places if you get caught distributing them.
