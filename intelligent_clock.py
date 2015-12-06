# coding: utf-8

from datetime import datetime, timedelta
import mraa
import pickle
import pywapi
import subprocess
import threading
import time
import unirest

import calendar_api

# initialize Buttons
stop_button = mraa.Gpio(4)
stop_button.dir(mraa.DIR_IN)
snooze_button = mraa.Gpio(3)
snooze_button.dir(mraa.DIR_IN)

# initialize global variables
snooze_time = 0


def generate_mp3(text, filename):
	response = unirest.post(
		"https://voicerss-text-to-speech.p.mashape.com/?key=bf473308587d4902b44e871e2ff6ce48",
		headers={
	      "X-Mashape-Key": "qBldwVHX3RmshYE6QarGAsRwoMBop1uOPOHjsncd1fF8YKh3b6",
	      "Content-Type": "application/x-www-form-urlencoded"
	    },
	    params={
	      "c": "mp3",
	      "f": "8khz_8bit_mono",
	      "hl": "pt-br",
	      "r": 0,
	      "src": text
	    }
	)
	with open(filename, 'wb') as output:
 		pickle.dump(response, output, pickle.HIGHEST_PROTOCOL)


def good_morning(): 
	greeting = u'Bom dia, agora são %s!' % time.strftime("%H:%M", time.localtime())
 
	weather_com = pywapi.get_weather_from_weather_com('BRXX0222','metric')
	
	conditions = weather_com['current_conditions']
	weather = u' O tempo hoje está %s e faz %s graus lá fora!' % (conditions['text'],
																  conditions['temperature'])
	forecasts = weather_com['forecasts']
	weather += u' A máxima para hoje é de %s graus e a mínima é de %s!' % (forecasts[0]['high'],
																		   forecasts[0]['low'])
	weather += u' A chance de chuva é de %s %!' % forecasts[0]['day']['chance_precip']

	calendar = u'Seus eventos para hoje são: %s' % str(calendar_api.get_events())

	# saving and reproducing
	report = greeting + weather + calendar
	generate_mp3(report, "report.mp3")
	subprocess.Popen(['gst-launch-1.0', 'filesrc', 'location=/home/root/clock/report.mp3',
					  '!', 'mad', '!', 'pulsesink']) 

def wake_up():
	stop_button_pressed = False
	snooze_button_pressed = False

	# play the alarm ringtone while the stop button is not pressed
	while stop_button_pressed == False:
		subprocess.Popen(['gst-launch-1.0', 'filesrc', 'location=/home/root/clock/wake.mp3',
						  '!', 'mad', '!', 'pulsesink']) 
		print("wake up playing")
		
		stop_button_pressed = stop_button.read()
		snooze_button_pressed = snooze_button.read()

		if snooze_button_pressed == True:
			print("snooze button pressed")
			stop_button_pressed = snooze()

		if stop_button_pressed == True:
			print("stop button pressed")
			good_morning()
	

def snooze():
	stop_button_pressed = stop_button.read()

	# set 1 minute snooze time
	snooze_time = datetime.utcnow() + timedelta(minutes = 1)
	print("snooze time: " + str(snooze_time))
	
	# checks if you want to end the snooze and play the report
	while stop_button_pressed == False:
		if (datetime.utcnow().hour == snooze_time.hour and 
		    datetime.utcnow().minute == snooze_time.minute and
			datetime.utcnow().second == snooze_time.second):
			return False
		stop_button_pressed = stop_button.read()

	return True


if __name__ == "__main__":
	while True:	
		# get today events and set the alarm time 
		calendar_api.get_events()
		alarm_time = calendar_api.alarm_time
		
		# print alarm_time and now time to debug
		print("alarm time: " + str(alarm_time))
		print("now: " + str(datetime.utcnow()))

		# checks if it's time to wake up
		if (datetime.utcnow().hour == alarm_time.hour and
			datetime.utcnow().minute == alarm_time.minute):
			# checks if it's 10 secs before or after, since it takes some time to execute the code
			# so it can miss the exactly second
			if (datetime.utcnow().second >= alarm_time.second - 10 and
				datetime.utcnow().second <= alarm_time.second + 10):
				wake_up()
