#!/usr/bin/env python

# ANALYSIS

# 1. Write a GUI program that:
#    Looks how you drew it in the back of the green notebook
#    - Contains widgets
#      - Buttons
#      - Labels
#      - Entry Box
#      - Box of Entries

# 2. Output to Monitor
#    - GUI Window that Contains Widgets as stated above


# 4. Processes
#    - Starts a timer to post to twitter
#    - Processes that need to be carried out when buttons are clicked.

#---------------------------------------------------------------------------

import sys
import tweepy
import threading
from random import *
import time 
from Tkinter import *
import tkMessageBox
from PIL import Image


CONSUMER_KEY = '#'
CONSUMER_SECRET = '#'
ACCESS_KEY = '#'
ACCESS_SECRET = '#'


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Global Variables
# - tweets = array of tweets to tweet
# - numberOfMinutesBetweenTweets = time buffer between tweets...(minimum 10)

tweets = []

numberOfMinutesBetweenTweets = 10

'''
The following section of code has been taken from:
http://stackoverflow.com/questions/4152969/genrate-timer-in-python
It is being used to put a time buffer between tweets 
to prevent overflow of tweets
'''
class TimerClass(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.event = threading.Event()

	def run(self):
		threading.Thread.__init__(self)
		self.event = threading.Event()
		while not self.event.is_set():
			#try:
				index = randint(0, len(tweets)-1)
				status = api.update_status(tweets[index])      	
				tweets[index] += "!"
				print (numberOfMinutesBetweenTweets)
				self.event.wait(numberOfMinutesBetweenTweets * 60)
			#except:
				#tkMessageBox.showwarning("ERROR", "You have caused an error. Please press 'Stop', then 'Clear' to clear the tweets, and try again")
				#self.event.set()
					

	def stop(self):
		self.event.set()

        


# The GUI class for the twitter bot. See above for information about
# widgets
class TwitterBotGUI:
	#define a constructor
	def __init__(self):
		self.mainWindow = Tk()
		self.mainWindow.wm_title("PROMOTION BOT")
		self.topFrame= Frame(self.mainWindow)
		self.tmr = TimerClass()
		
		self.entryFrame = Frame(self.mainWindow)
		self.timeEntryFrame = Frame(self.mainWindow)
		self.sButtonFrame = Frame(self.mainWindow)
		self.listBoxFrame = Frame(self.mainWindow)
		self.bottomFrame = Frame(self.mainWindow)

		#Background Image
		
		self.backgroundImage = PhotoImage(file = "servbot.gif")	
		self.backgroundLabel = Label(self.mainWindow, image = self.backgroundImage)
		
		#Labels
		self.titleLabel = Label(self.topFrame, text=('Promo Bot'))
		self.entryLabel = Label(self.entryFrame, text=('Enter text you would like to tweet: '))
		self.timeLabel = Label(self.timeEntryFrame, text = ('Amount of Minutes Between Tweets (At least 5, Default is 10): '))

		#Entry Box
		self.tweetEntry = Entry(self.entryFrame, width = 35)
		self.timeLimitEntry = Entry(self.timeEntryFrame, width = 2)

		#Buttons
		self.sumbitButton = Button(self.entryFrame, text=('Tweet This'), command = self.addToList)
		self.startButton = Button(self.sButtonFrame, text=('Start'), command = self.startButtonFunction)
		self.stopButton = Button(self.sButtonFrame, text=('Stop'), command = self.stopButtonFunction, state = DISABLED)
		self.clearButton = Button(self.bottomFrame, text=('Clear'), command = self.clearListBox)
		self.closeButton = Button(self.bottomFrame, text=('Close'), command = self.closeButtonFunction)
		self.minutesButton = Button(self.timeEntryFrame, text=('Minutes'), command = self.minutesButtonFunction)

		#ListBox
		self.listBox = Listbox(self.listBoxFrame, width = 50)


		#Packing

		
		self.topFrame.pack()
		self.entryFrame.pack()
		self.timeEntryFrame.pack()
		self.sButtonFrame.pack()
		self.backgroundLabel.pack()
		self.listBoxFrame.pack()
		self.bottomFrame.pack()

		self.titleLabel.pack()
		self.entryLabel.pack(side=('left'))
		self.sumbitButton.pack(side=('right'))
		self.tweetEntry.pack(side=('right'))
		self.timeLabel.pack(side=('left'))
		self.timeLimitEntry.pack(side=('left'))


		self.startButton.pack(side=('left'))
		self.stopButton.pack(side=('right'))
		self.minutesButton.pack(side=('right'))
		
		self.listBox.pack()

		self.clearButton.pack(side=('left'))
		self.closeButton.pack(side=('right'))



		mainloop()
	#Callback Methods
	def addToList(self):
		val = self.tweetEntry.get()
		#Append exclamation mark to the tweet (to prevent repeated tweets)
		tweets.append(val);
		#Clear the textbox so the user doesn't have to clear it themselves
		self.tweetEntry.delete(0, END)
		self.listBox.insert(END, val)

	def clearListBox(self):
		#Clear the box and clear the tweets array
		self.listBox.delete(0, END)
		del tweets[:]

	def stopButtonFunction(self):
		self.startButton.config(state = ACTIVE)
		self.stopButton.config(state = DISABLED)
		self.sumbitButton.config(state = ACTIVE)
		self.minutesButton.config(state = ACTIVE)
		self.tmr.stop()

	def startButtonFunction(self):
		if(len(tweets) == 0):
			tkMessageBox.showwarning("ERROR", "You have no tweets to tweet!")
			return

		self.stopButton.config(state = ACTIVE)
		self.startButton.config(state = DISABLED)
		self.sumbitButton.config(state = DISABLED)
		self.minutesButton.config(state = DISABLED)
		self.tmr.start()
		

	def closeButtonFunction(self):
		self.mainWindow.destroy()

	def minutesButtonFunction(self):
		global numberOfMinutesBetweenTweets
		numberOfMinutesBetweenTweets = int(self.timeLimitEntry.get())
		



def main():

	testVariable = TwitterBotGUI()


main()
