#!/usr/bin/env python
'''
DEBUGGER_TEMPLATE.PY

RoboCup debugger template. Below is a simple skeleton program that will display and update a graphics window.
The graphics window will display updated text of the robot's current motion state.
Use any commented information or functions that when executed, add information to the graphics window.
Generally the information you will be displaying will be accessed through the robot's shared memory.
'''

# math and science libraries
import numpy as np
import scipy as sp
# import for shared memory access
import pyshm
import shm
# graphics and image libraries
import tkMessageBox, tkFont, tkSimpleDialog, tkFileDialog, sys, os, ImageTk
import Image as im
from Tkinter import *

class DebuggerTemplate:
        def __init__(self, naoTeam, naoID):
                # Pass in team and player IDs as according to webots
		# You can use these to gather specific player info
		# Or you could pass in only team ID and look at all players of that team
                self.naoTeam = naoTeam
                self.naoID = naoID

                # OPTIONAL: Convert to correct Webots role/number
		# nao 1 is the goalie; nice for display purposes
                if naoID is 1:
                        self.role = 'Goalie'
                else:
                        webots_num = int(naoID)-1
                        self.role = 'Player '+str(webots_num)

                # MUST HAVE: Creates root for all graphic transformations and display
                self.root = Tk()
		self.root.title("Debugger")
                
		'''
		CANVAS AND WINDOW SETUP
		'''
		# Make window scalable
		self.root.resizable()
		# Size and color of window
		self.width = 500
		self.height = 500
		self.color = "white"
		# Create canvas with white background
		self.canvas = Canvas(self.root, bg=self.color, width=self.width, height=self.height)

                '''
		# TO CREATE AN IMAGE BACKGROUND
                self.bg = im.open(bg_file)
		self.DispBg = ImageTk.PhotoImage(self.bg)
                # make width and height, size of image
                self.width, self.height = self.bg.size
                # Create canvas
                self.canvas = Canvas(self.root, width=self.width, height=self.height)
                # Add background to canvas
                self.bgID = self.canvas.create_image(0, 0, anchor=NW, image=self.DispBg)
		'''
		# Package the canvas
		self.canvas.pack()

		# If window is resized, update width
                self.canvas.bind("<Configure>", self.resize)
		
                self.setup()
                
                # Create event that is constantly renewed to get new data
                self.root.after(0, self.update)

                #Keeps running, handles all events
                self.root.mainloop()

	'''
	SETUP
	Here is a good place to put class variables
	that are not related to setup.
	Good example, SHARED MEMORY SEGMENT NAMES
	'''
        def setup(self):
                                
                # Get user's ID (MUST HAVE FOR MEMORY SEGMENTS)
                self.usr = str(os.getenv('USER'))
        
                # Make shared memory segment
		# This example accesses the world robot info
		# STRING FORMAT: finite_state_machine_name + nao_team_number + nao_ID + your_user_name
		self.wcmSegName = 'wcmRobot' + str(self.naoTeam) + str(self.naoID) + self.usr
		self.wcmRobot = shm.ShmWrapper(self.wcmSegName)             
                
                #initialize whatever other variables you may have
                self.position = ""
 

	'''
	UPDATE
	It is called constantly and will update the window with the more recent information from shared memory.
	Add your drawing functions here.
	'''
	def update(self):
               # CLEAR CANVAS
               # Must do before you put new info up!
               # May only want to delete select items, change from "ALL"
               self.canvas.delete(ALL)
		
	       # ADDING SHAPES
	       # canvas.create_oval(coordinates,fill=None,outline=some_color,width=5)
	       # canvas.create_line(coordinates, arrow=LAST) #can set the arrow to point FIRST/LAST
	       # canvas.delete(some_shape_variable)

	       # ADDING IMAGES
	       # img = PhotoImage(file = 'myImage.gif')
	       # Creates a canvas with height = 50, width = 10 and the image on the canvas
	       # canvas.create_image(50, 10, image = image1, anchor = NW)
    
	       # UPDATING SHARED MEMORY VARIABLES
	       self.position = self.wcmRobot.get_pose()
    
	       # ADDING TEXT
	       self.canvas.create_text(150, 150, text = str(self.position))
	       # more at: http://effbot.org/zone/editing-canvas-text-items.htm
               
	       # MUST: Reschedule update so it runs again
	       self.root.after(200, self.update)

	'''
	RESIZE
	It is a tk canvas event and is called whenever the main graphics
	window is scaled or resized.
	SEE: setup() "canvas.bind("<Configure>", resize)"
	'''
	def resize(self, event):
		# If window changes size, update width and height
		self.width = event.width
		self.height = event.height        

# Call an instance of this class
# Pass in command line args with sys.argv[#]
win = DebuggerTemplate(sys.argv[1], sys.argv[2])

