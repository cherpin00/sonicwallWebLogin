import time
import os
from tkinter import *
from tkinter import messagebox
from multiprocessing import Process
from selenium.common.exceptions import WebDriverException
import configparser
import io

from functions import HEADLESS, USERNAME, get_driver, login_and_set_time, logout

class App:
	def __init__(self):
	# creating Tk window
		get_driver()

		self.root = Tk()

		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

		self.durration = 1
		self.isConnected=False
		self.root.after(int((1 * 1000 * 60) / 2), self.task)
		
		# setting geometry of tk window
		self.root.geometry("300x250")

		# Using title() to display a message in
		# the dialogue box of the message in the
		# title bar.
		self.root.title("Time Counter")

		# Declaration of variables
		# self.hour=StringVar()
		# self.minute=StringVar()
		# self.second=StringVar()
		self.status = StringVar()

		# setting the default value as 0
		# self.hour.set("00")
		# self.minute.set("00")
		# self.second.set("00")
		self.status.set("Not connected")

		self.statusLabel = Label(self.root, textvariable=self.status)
		self.statusLabel.pack()

		self.userLabel = Label(self.root, text=USERNAME)
		self.userLabel.pack()
		# Use of Entry class to take input from the user
		# self.hourEntry= Entry(self.root, width=3, font=("Arial",18,""),
		# 				textvariable=self.hour)
		# self.hourEntry.place(x=80,y=20)

		# self.minuteEntry= Entry(self.root, width=3, font=("Arial",18,""),
		# 				textvariable=self.minute)
		# self.minuteEntry.place(x=130,y=20)

		# self.secondEntry= Entry(self.root, width=3, font=("Arial",18,""),
		# 				textvariable=self.second)
		# self.secondEntry.place(x=180,y=20)

			# button widget
		self.connectButton = Button(self.root, text='Connect', bd='5',
				command=self.connect)
		self.connectButton.place(x = 70,y = 120)
		
		self.disconnectButton = Button(self.root, text='Disconnect', bd='5',
				command=self.disconnect)
		self.disconnectButton.place(x = 140,y = 120)
	# def submit():
	# 	try:
	# 		# the input provided by the user is
	# 		# stored in here :temp
	# 		temp = int(hour.get())*3600 + int(minute.get())*60 + int(second.get())
	# 	except:
	# 		print("Please input the right value")
	# 	while temp >-1:
			
	# 		# divmod(firstvalue = temp//60, secondvalue = temp%60)
	# 		mins,secs = divmod(temp,60)

	# 		# Converting the input entered in mins or secs to hours,
	# 		# mins ,secs(input = 110 min --> 120*60 = 6600 => 1hr :
	# 		# 50min: 0sec)
	# 		hours=0
	# 		if mins >60:
				
	# 			# divmod(firstvalue = temp//60, secondvalue
	# 			# = temp%60)
	# 			hours, mins = divmod(mins, 60)
			
	# 		# using format () method to store the value up to
	# 		# two decimal places
	# 		hour.set("{0:2d}".format(hours))
	# 		minute.set("{0:2d}".format(mins))
	# 		second.set("{0:2d}".format(secs))

	# 		# updating the GUI window after decrementing the
	# 		# temp value every time
	# 		root.update()
	# 		time.sleep(1)

	# 		# when temp value = 0; then a messagebox pop's up
	# 		# with a message:"Time's up"
	# 		if (temp == 0):
	# 			messagebox.showinfo("Time Countdown", "Time's up ")
			
	# 		# after every one sec the value of temp will be decremented
	# 		# by one
	# 		temp -= 1

	def connect(self):
		# self.connectProcess = Process(target=block_connect)
		# self.connectProcess.start()
		login_and_set_time(str(self.durration))
		self.isConnected = True
		self.status.set("Connected")

	def disconnect(self):
		# self.connectProcess.terminate()
		self.isConnected = False
		self.status.set("Not connected")
		logout()

	def start(self):
		# infinite loop which is required to
		# run tkinter program infinitely
		# until an interrupt occurs
		self.root.mainloop()

	def task(self):
		if self.isConnected:
			login_and_set_time(str(self.durration))
		self.root.after(int((1 * 1000 * 60) / 2), self.task)
	
	def on_closing(self):
		# logout()
		try:
			print("Logging out...")
			logout()
		except WebDriverException:
			print("WARNING: Failed to logout.  Chrome was not open.")
		print("Closing...")
		self.root.destroy()
		pass
			

def main():
	global USERNAME, HEADLESS
	configFile = "config.ini"
	if os.path.exists(configFile):
		configStr = '[DEFAULT]\n' + open(configFile, 'r').read()
		configFP = io.StringIO(configStr)
		config = configparser.RawConfigParser()
		config.read_file(configFP)
		USERNAME = config["DEFAULT"].get("user", USERNAME)
		HEADLESS = config["DEFAULT"].get("HEADLESS", HEADLESS)
	print("Username is", USERNAME)
	print("Headless is", HEADLESS)
	app = App()
	app.start()

if __name__ == "__main__":
	main()