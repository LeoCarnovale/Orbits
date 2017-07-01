# Author: Leo Carnovale (leo.carnovale@gmail.com / l.carnovale@student.unsw.edu.au)
# Date  : April to May ish?
# Orbits 4T


from tkinter import *
from math import *
import turtle
import random
import time
import vector
import loadSystem
import particle as Pmodule

randomVector = vector.randomVector
vector = vector.vector

particleList = Pmodule.particleList
markerList   = Pmodule.markerList

marker   = Pmodule.marker
particle = Pmodule.particle

print("Starting Orbits4T")

LINUX = False # If true, then non alphanumeric key controls will be replaced with numbers

#############################################################################################################################
# args:																														#
# <key> : [<type>, <default value>, <requires parameter>, [<second default value>], [changed]]								#
# second default value is only necessary if <requires parameter> is true.													#
# if true, then the algorithm looks for a value after the key.																#
# if false, the algorithm still looks for a value after the key but if no value is given the second default value is used.	#
# The final value indicates if the argument has been supplied, to know if the user has specified a value					#
# 	 (Useful if the default varies depending on other arguments)															#
#																															#
########### PUT DEFAULTS HERE ###############################################################################################
args = {#   [<type>   \/	 <Req.Pmtr>  <Def.Pmtr>
"-?"  :  [None],
"-d"  :  	[float,	0.025,	True], # Delta time per step
"-n"  :  	[int,   20,		True], # Particle count
"-p"  :  	[int,   1,		True], # preset
"-sp" :  	[str,   False,	False,  True], # start paused
"-ss" :  	[str,   False,	False,  True], # staggered simulation
"-G"  :  	[float, 20,		True], # Gravitational constant
"-pd" :  	[str,   False,	False,  True], # Print data
"-sd" :  	[float, 2000,	True], # Default screen depth
"-ps" :  	[float, 0.01,	True], # Maximum pan speed
"-rs" :  	[float, 0.01,	True], # Rotational speed
"-mk" :  	[str,   False,	False,  True], # Show marker points
"-ep" :  	[int,   360,	True], # Number of points on each ellipse (Irrelevant if SMART_DRAW is on)
"-sf" :  	[float, 0.5,	True], # Rate at which the camera follows its target
"-ad" :  	[str,   False,	False,  True], # Always draw. Attempts to draw particles even if they are thought not to be on screen
"-vm" :  	[float, 150,	True], # Variable mass. Will be used in various places for each preset.
"-vv" :  	[float, False,	False,  1], # Draw velocity vectors
"-ds" :  	[str,	False,	False,  True], # Draw stars, ie, make the minimum size 1 pixel, regardless of distance.
"-sdp":  	[int,   5,		True], # Smart draw parameter, equivalent to the number of pixels per edge on a shape
"-me" :		[int,   400,	True], # Max number of edges drawn
"-ab" :  	[int,   False,	False,  20], # Make asteroid belt (Wouldn't recommend on presets other than 3..)
"-es" :  	[int,	False,	False,  5], # Make earth satellites
"-WB" :  	[str,   False,	False,	True], # Write buffer to file
"-flim": 	[float, False,	True], # Frame limit
"-df" :  	[str, "SolSystem.txt", True], # Path of the data file
"-test": 	[str,	 False, False, True], # Test mode
"-getStars": [float,  False,	False, 4], # Get stars from the datafile.
"-AA_OFF": [str, True, 	False, 	False]   # Turn off AutoAbort.
}

originalG = args["-G"][1]

if len(sys.argv) > 1:
	if ("-?" in sys.argv):
		# Enter help mode
		print("Welcome to Orbits4T!")

		print("""
This version contains 3 presets:
1)  Centre body with -n number of planets orbiting in random places. (Default 10)
2)  'Galaxy' kinda thing (Miserable failure, don't waste your time with this one)
3)  Our very own Solar System!
The third one is way better, don't even bother with the other two. They were just practice.

Arguments:
Key|Parameter type|Description
   | (if needed)  |
-d :    float       Delta time per step.
-n :    int         Particle count, where applicable.
-p :    int         Preset.
-sp:                Start paused.
-ss:                Staggered simulation (Hit enter in the terminal to trigger each step)
-G :    float       Gravitational constant.
-pd:                Print debugging data.
-sd:    float       Default screen depth.
-ps:    float       Maximum pan speed.
-rs:    float       Rotational speed.
-mk:                Show marker points (static X, Y, Z and Origin coloured particles)
-ep:    int         Number of points on each ellipse (Irrelevant if SMART_DRAW is on (which it is))
-sf:    float       Rate at which the camera follows its target.
-ad:                Always draw. Attempts to draw particles even if they are thought not to be on screen
-vm:    float       Variable mass. To be used in relevant places for some presets.
-vv:                Draw velocity and acceleration vectors. Note that while velocity vectors are to scale,
                        acceleration vectors are multiplied by 5 when being drawn. (Otherwise they are too short)
                        Give a number parameter to scale each vector.
-ds  :              Draw stars, ie, make the minimum size 1 pixel, regardless of distance.
-sdp :  int         Smart draw parameter, equivalent to the number of pixels per edge on a shape.
-me  :  int         Maximum edges, max number of edges drawn on each shape.
-ab  :  int         Make asteroid belt (Wouldn't recommend on presets other than 3..)
-es  :  int         Make earth satellites.
-WB  :              Write buffer to file.
-flim:  float       Frame limit.
-df  :  str         Path of the data file.
-test:              Enter test mode.*
-AA_OFF:            Turn off AutoAbort. (AutoAbort will kill the simulation if two consecutive frames
                        last longer than a second, it's only trying to help you not bring your
                        computer to a standstill, be careful if you choose to abandon it)
-? : Enter this help screen then exit

Using the program:
  - Use W, A, S, D to move forwards, left, backwards, and right respectively.
  - Use R, F to move up and down respectively.
  - Use the arrow keys to rotate the camera.
  - '[', ']' to decrease and increase delta time.
  - ',', '.' to decrease and increase the screen depth.
  - 'n', 'm' to start recording and playing the buffer. The simulation will be paused while recording.
  - Space to pause the simulation. (Movement is still allowed)
  - 'I' will set the simulation to run at real time (ish).
  - '\\' will reverse time.
  - Click any particle to set the camera to track that particle.
  - Right click any particle to fix the camera's rotation on that particle.
  - Cycle through targeted particles with Tab/shift-Tab. (Available only in preset 3)
        Once a particle is targeted, pressing T and Y will toggle pan and rotational
        tracking respectively.
  - Press 'G' to go to a selected target.
  - To stop tracking, click (and/or right click) on empty space or another particle.
  - To clear the target selection, press C
  - End the simulation with Esc.

*Test mode: There are some hard coded time, position and velocity snapshots for various
bodies in the simulation, with data taken from the same source as the start positions, but
anywhere between 92 minutes and a month later, and so show the correct positions and velocities
that those bodies should have. Test mode will use the delta time step given by the command line
argument (or the default) and nothing else. No graphics will be drawn, instead the program will
simply step its way through to each relevant time until each of the bodies with test data can
have their correct position and velocity compared with the correct values.""")
		exit()
	argv = sys.argv
	for arg in args:
		args[arg].append(False) # This last value keeps track of whether or not the argument has been specified by the user
	for i, arg in enumerate(argv):
		if arg in args:
			if (args[arg][-1]):
				print("%s supplied multiple times." % (arg))
			try:
				if args[arg][2]:
					if argv[i + 1] in args:
						raise IndexError # If the next arg is an arg keyword (eg -p, -d) then the parameter is missing
					args[arg][1] = args[arg][0](argv[i + 1])
				else: # No parameter needed, set it to args[arg][3]
					if (len(argv) > i + 1 and (argv[i + 1] not in args)):
						args[arg][1] = args[arg][0](argv[i + 1])
					else:
						args[arg][1] = args[arg][3]
				args[arg][-1] = True
			except ValueError:
				print("Wrong usage of {}".format(arg))
			except IndexError:
				print("Missing parameter for {}.".format(argv[i]))

		else:
			if (arg[0] == "-"):
				print("Unrecognised argument: '%s'" % (arg))

else:
	print("You haven't used any arguments.")
	print("Either you're being lazy or don't know how to use them.")
	print("For help, run '%s -?'" % (sys.argv[0]))
	time.sleep(1)
	print("Now onto a very lame default simulation...")
	time.sleep(1)

Delta			        = args["-d"][1]
PARTICLE_COUNT	        = args["-n"][1]
preset			        = args["-p"][1]
STAGGERED_SIM	        = args["-ss"][1]
START_PAUSED	        = args["-sp"][1]
particle.G		        = args["-G"][1]
PRINT_DATA		        = args["-pd"][1]
defaultScreenDepth	    = args["-sd"][1]
maxPan			        = args["-ps"][1]
rotSpeed		        = args["-rs"][1]
showMarkers		        = args["-mk"][1]
ellipsePoints	        = args["-ep"][1]
smoothFollow	        = args["-sf"][1]
DRAW_VEL_VECS	        = args["-vv"][1]
ALWAYS_DRAW		        = args["-ad"][1]
variableMass	        = args["-vm"][1]
DATA_FILE		        = args["-df"][1]
drawStars		        = args["-ds"][1]
makeAsteroids 	        = args["-ab"][1]
makeSatellites	        = args["-es"][1]
writeBuffer		        = args["-WB"][1]
FRAME_LIMIT 	        = args["-flim"][1]
getStars 		        = args["-getStars"][1]

TestMode 				= args["-test"][1]
AUTO_ABORT              = args["-AA_OFF"][1]      # I wouldn't change this unless you know the programs good to go

SMART_DRAW_PARAMETER = args["-sdp"][1]     # Approx number of pixels between each point

MAX_POINTS = args["-me"][1]  # Lazy way of limiting the number of points drawn to stop the program
                             # grinding to a halt everytime you get too close to a particle

particle.TestMode = TestMode

MAX_VISIBILE_MAG = 7

# Preset 3
AsteroidsStart 	 = 249.23 * 10**9 # Places the belt roughly between Mars and Jupiter.
AsteroidsEnd 	 = 740.52 * 10**9 # Couldn't find the actual boundaries (They're probably pretty fuzzy)
AsteroidsMinMass = 0.0001 * 10**15
AsteroidsMaxMass = 1	  * 10**23
AsteroidsDensity = 1500

# Preset 4
PRESET_4_MIN_RADIUS = 40
PRESET_4_MAX_RADIUS = 400

# Time lengths constants
MINUTE 	= 60
HOUR 	= 60 *	MINUTE
DAY  	= 24 *	HOUR
YEAR 	= 365 * DAY

# Distance constants
LIGHT_SPEED = 299792458
LIGHT_YEAR  = LIGHT_SPEED * YEAR
AU		= 149597870700
PARSEC  = 3.085677581e+16

# Misc settings
particle.ALL_IMMUNE = False
REAL_TIME           = False
particle.defaultDensity		= 1
particle.radiusLimit		= 1e+10       # Maximum size of particle
voidRadius          = 5000      # Maximum distance of particle from camera
CAMERA_UNTRACK_IF_DIE = True # If the tracked particle dies, the camera stops tracking it
SMART_DRAW = True               # Changes the number of points on each ellipse
FPS_AVG_COUNT = 15

# Camera constants
DEFAULT_ROTATE_FOLLOW_RATE = 0.04
AUTO_RATE_CONSTANT  = 10    # A mysterious constant which determines the autoRate speed, 100 works well.
FOLLOW_RATE_COEFF   = 0.1
FOLLOW_RATE_BASE    = 1
TRAVEL_STEPS_MIN	= 100   # Number of steps to spend flying to a target (at full speed, doesn't include speeding up or slowing down)

DEFAULT_ZERO_VEC = [0, 0, 0]
DEFAULT_UNIT_VEC = [1, 0, 0]


								# depending on its size
MIN_BOX_WIDTH = 50

if not AUTO_ABORT:
	print("Auto abort is off!")
	print("This should only be done on large simulations where a low frame is expected.")
	print("If you don't need it off, don't turn it off.")
	time.sleep(3)


if TestMode:
	if preset == 3:
		# Test data:
		testData = {# [[<Name>, <Time>, <Pos>, <vel>], ...]
			"ISS":
			[(2017 * YEAR + 92 * MINUTE), # 2017 years, 1 hour 32 minutes, ie 1 hour 32 mins after start, should be one orbit.
			vector([-2.652741416195131E+07,  1.451863591737731E+08, -2.246871177630126E+04]) * 1000, # Both given in km/s, convert to m/s
			vector([-2.268856357268088E+01, -8.202616782054283E+00, -1.309397555344641E+00]) * 1000],
			"Moon":
			[(2017 * YEAR + 92 * MINUTE),
			vector([-2.626413928789543E+07,  1.449000582187190E+08, -1.580188827935606E+04]) * 1000,
			vector([-2.906316391048909E+01, -4.878152316231304E+00, -8.298362677803639E-02]) * 1000],
			"Earth":
			[(2017 * YEAR + 92 * MINUTE),
			vector([-2.652775232714054E+07,  1.451886523109221E+08, -2.883530398781598E+04]) * 1000,
			vector([-2.977993074888063E+01, -5.581820507958473E+00,  1.472498187503835E-03]) * 1000],
			"Mercury":
			[(2017 * YEAR + 31 * DAY),
			vector([-3.491563712116394E+07, -5.847758798545337E+07, -1.603576528303239E+06]) * 1000,
			vector([3.195297711109924E+01, -2.269718543834500E+01, -4.787363119651942E+00]) * 1000],
			"Voyager2":
			[(2017 * YEAR + 31 * DAY),
			vector([4.678084657944870E+09, -1.291984823213759E+10, -9.959551510991798E+09]) * 1000,
			vector([4.245078194430032E+00, -9.418854886561272E+00, -1.138382248152680E+01]) * 1000]
		}
		if (not testData):
			print("No test data given to test with. Aborting.")
			exit()
		else:
			print("Testing positions and velocities for:", ", ".join([x for x in testData]))

	else:
		print("Testing not available for this preset (%d)." %(preset))

def setup():
	# a = particle(1, vector([25, 1, 0]))
	# camera.drawParticle(a)
	if showMarkers:
		O = marker(vector([0,   0, 0]), [1, 1, 1])
		X = marker(vector([100, 0, 0]), [1, 0, 0])
		Y = marker(vector([0, 100, 0]), [0, 1, 0])
		Z = marker(vector([0, 0, 100]), [0, 0, 1])

def roundList(list, places):
	return [round(x, places) for x in list]




def screenWidth():
	return turtle.window_width()

def screenHeight():
	return turtle.window_height()


def drawOval(x, y, major, minor, angle, fill = [0, 0, 0], box = False, mag = None):
	global ellipsePoints
	global drawStars
	if SMART_DRAW:
		perimApprox = 2*pi*sqrt((major**2 + minor**2) / 2)
		points = int(perimApprox / SMART_DRAW_PARAMETER)
	else:
		points = ellipsePoints
	points = min(points, MAX_POINTS)
	localX = major/2
	localY = 0
	screenX = localX * cos(angle) - localY * sin(angle)
	screenY = localY * cos(angle) + localX * sin(angle)
	if box:
		boxRadius = max(MIN_BOX_WIDTH, major * 1.4) / 2
		turtle.up()
		turtle.pencolor([1, 1, 1])
		turtle.goto(x - boxRadius, y - boxRadius)
		turtle.down()
		turtle.goto(x - boxRadius, y + boxRadius)
		turtle.goto(x + boxRadius, y + boxRadius)
		turtle.goto(x + boxRadius, y - boxRadius)
		turtle.goto(x - boxRadius, y - boxRadius)
		turtle.up()
	if (points > 3):
		turtle.up()
		turtle.goto(x + screenX, y + screenY)
		turtle.begin_fill()
		turtle.fillcolor(fill)
		onScreen = True
		Drawn = False
		for i in range(points):
			localX = major/2 * cos(2 * pi * i / points)
			localY = minor/2 * sin(2 * pi * i / points)
			screenX = localX * cos(angle) - localY * sin(angle)
			screenY = localY * cos(angle) + localX * sin(angle)
			turtle.goto(x + screenX, y + screenY)
		turtle.end_fill()
	if (drawStars):
		turtle.up()
		turtle.goto(x, y)
		flareWidth = 0
		if (mag == None):
			if (points < 2):
				turtle.dot(2)
			return True
		if (points <= 3):
			fill = [1, 1, 1]
			flareWidth = max(MAX_VISIBILE_MAG - mag, 0)
		else:
			flareWidth = max(MAX_VISIBILE_MAG - mag, 0) * 1.5

		# if (flareWidth > 1000): print(flareWidth)
		for r in range(int(flareWidth), 0, -1):
			rMag = (1 - (r / flareWidth))
			turtle.pencolor([x * rMag for x in fill])
			turtle.dot(r + minor)


	# else:
	# 	return False
	return True

def drawLine(pointA, pointB = None, fill = "black", width = 1):
	if (pointB == None):
		x1, y1 = (0, 0)
		x2, y2 = pointA
	else:
		x1, y1 = pointA
		x2, y2 = pointB

	turtle.pencolor(fill)
	turtle.up()
	turtle.goto(x1, y1)
	turtle.down()
	turtle.goto(x2, y2)
	turtle.up()

# These must be in descending order:
prefixes = {
	"! Parsecs":PARSEC,
	"! light years":LIGHT_YEAR,
	"P":1e15,
	"T":1e12,
	"G":1e9,
	"M":1e6,
	"k":1e3,
	"" :1e0,
	"m":1e-3,
	u"\u03BC":1e-6
}
# Returns a string of num reduced with the appropriate prefix
def numPrefix(num, unit, rounding=3):
	# unit is a string, ie 'm', 'g'
	global prefixes
	for p in prefixes:
		if (num > prefixes[p]):
			if (p and p[0] == "!"):
				result = str(round(num / prefixes[p], rounding)) + p[1:] + unit[1:]
			else:
				result = str(round(num / prefixes[p], rounding)) + p + unit
			return result
	return str(num) + unit

def timeString(seconds, rounding=3):
	if seconds < 60:
		return ("{}s".format(round(seconds, rounding)))

	minutes = seconds / 60
	minutes = int(minutes)
	if minutes < 60:
		return ("{}:{}s".format(int(minutes), round(seconds % 60, rounding)))

	hours = minutes / 60
	if hours < 24:
		return ("{}:{}:{}s".format(int(hours), int(minutes % 60), round(seconds % 60, rounding)))

	days = hours / 24
	if days < 365:
		return ("{} days, {}:{}:{}s".format(int(days), int(hours % 24), int(minutes % 60), round(seconds % 60, rounding)))

	years = days / 365
	return ("{} years, {} days, {}:{}:{}s".format(int(years), int(days % 365), int(hours % 24), int(minutes % 60), round(seconds % 60, rounding)))

class buffer:
	def __init__(self):
		# self.allshift = DEFAULT_ZERO_VEC
		# self.allrotate = DEFAULT_ZERO_VEC
		self.buffer = {}
		self.bufferMode = 0 # 0: Normal. 1: Recording, sim paused. 2: Playing.
		self.bufferLength = 0
		self.emptyBuffers = len(particleList)
		self.bufferCount = self.emptyBuffers
		for p in particleList:
			self.buffer[p] = []

	def __sizeof__(self):
		return (self.bufferLength * sys.getsizeof(self.buffer[particleList[0]]) * len(particleList))

	def addParticle(self, particle):
		self.buffer[p]    = [] * (bufferLength + 1)
		self.emptyBuffers += 1
		self.bufferCount  += 1

	def bufferModeString(self):
		if (self.bufferMode == 0):
			return "Normal"
		elif (self.bufferMode == 1):
			return "Recording"
		elif (self.bufferMode == 2):
			return "Playing"

	# def getBuffer(self, particle, index = -1, remove = None):
	#     if self.bufferLength > 0:
	#         result = self.buffer[particle][index]
	#         if remove != None: self.buffer[particle].pop(remove)
	#         return result
	#     else:
	#         return False

	def addBuffer(self, particle):#, colour = None):
		pos = particle.pos.getClone()
		rad = particle.radius
		colour = particle.colour
		vel = particle.vel.getClone()
		acc = particle.acc.getClone()
		self.bufferLength += 1
		if (not self.buffer[particle]):
			self.emptyBuffers -= 1
		if (DRAW_VEL_VECS):
			self.buffer[particle].append([pos, rad, colour, vel, acc])
		else:
			self.buffer[particle].append([pos, rad, colour])


	def playBuffer(self, particle, index = 0, remove = True):
		if (not self.buffer[particle]):
			self.emptyBuffers += 1
			# self.bufferMode = 0
			return False
		buff = self.buffer[particle][index]
		if remove:
			self.bufferLength -= 1
			self.buffer[particle].pop(index)
		return buff

	def processPosition(self, particle, defaultIndex = 0, playIndex = 0, playRemove = True):
		# A kind of autopilot, takes in a position and returns basically what the camera should see.
		if self.bufferMode == 2:
			if (self.emptyBuffers == self.bufferCount):
				self.bufferMode = 0
				return False
			# playing
			# print("Playing particle")
			play = self.playBuffer(particle, playIndex, playRemove)
			# if (play):
			return play

		elif self.bufferMode == 1:
			# recording. Don't let the particle move.
			# print("Recording. Keeping particle frozen.")
			self.addBuffer(particle)
			return self.buffer[particle][0]
		else:
			return False

def warpedDistance(particle):
	if particle == None:
		return None
	dist = (abs(particle.pos - camera.pos) - particle.radius)*(1 + tan(1/2 * camera.rot.relAngle(particle.pos - camera.pos)))
	return abs(dist)

class MainLoop:
	def __init__(self):
		# Records the movements to all particles
		self.Time = 0
		self.commonShiftPos = DEFAULT_ZERO_VEC
		self.commonShiftVel = DEFAULT_ZERO_VEC
		self.closestParticle = None

		self.pause = -1         # 1 for pause, -1 for not paused.
		self.Delta = 0

		self.clickTarget = []
		self.target = None
		self.FPS = 1
		self.frameWarning = False
		self.displayData = True
		self.DataDisplay = {
		#  	Title		 [<is a function>, object]
		}

	def Zero(self):
		self.commonShiftPos = DEFAULT_ZERO_VEC
		self.commonShiftVel = DEFAULT_ZERO_VEC
		self.commonRotate = DEFAULT_ZERO_VEC

	def setDelta(self, delta):
		for p in particleList:
			p.runLoop()
			p.vel -= self.Delta / 2 * p.acc
			p.vel += delta / 2 * p.acc
			p.acc *= 0
		self.Delta = delta

	def addData(self, name, data, isExpression=False, default=None):
		self.DataDisplay[name] = [isExpression, data, default]

	def addDataLine(self):
		self.DataDisplay["\n"] = None

	def showData(self):
		if not self.displayData: return False
		global planets
		# delta = self.Delta
		pauseString = "True"
		if self.Time != 0:
			time = ("-" if self.Time < 0 else "") + timeString(abs(self.Time))
		else:
			time = "00:00"
		if self.pause == -1: pauseString = "False"
		text = """Frame Rate: %s
Buffermode: %s (%d) --> (%.2lf Mb)
Particle Count: %d Delta: %f
Paused: %s         Time:  %s
Distance to closest particle: %s
		""" % (
			(("%.2f"%self.FPS) if self.FPS != 999 else "INFINITY!!"),
			Buffer.bufferModeString(),
			(0 if Buffer.bufferCount == 0 else Buffer.bufferLength / Buffer.bufferCount),
			sys.getsizeof(Buffer) / 1000000,
			len(particleList),
			self.Delta,
			pauseString,
			time,
			("---" if not self.closestParticle else numPrefix(abs(camera.pos - self.closestParticle.pos), "m"))
		)

		for data in self.DataDisplay:
			text += "\n"
			if self.DataDisplay[data] == None:
				continue
			text += data + ":\t"
			if (self.DataDisplay[data][0]):
				# print(self.DataDisplay[data][1])
				try:
					value = eval(self.DataDisplay[data][1])
				except Exception:
					value = self.DataDisplay[data][2]
			else:
				value = self.DataDisplay[data][1]
			text += str(value)

		width = screenWidth()
		height = screenHeight()
		textX = -width / 2 + 10
		textY = height / 2 - 15 * (len(text.split("\n")) - 1) # Origin of the text box is bottom left corner
		if (text[-1] != "\n"): textY -= 15
		turtle.goto(textX, textY)
		turtle.down()
		turtle.pencolor([1, 1, 1])
		turtle.write(text)

	def abort(self):
		global Running
		Running = False
		print("Auto Aborting!!!")

	def STEP(self, camera, draw = True):
		global FRAME_LIMIT
		global particleList
		global DRAW_VEL_VECS
		global panRate
		delta = self.Delta
		if (self.closestParticle != None):
			panAmount = (abs(self.closestParticle.pos - camera.pos) - self.closestParticle.radius) * maxPan#maxPan/(AUTO_RATE_CONSTANT)
			if (pan[-1]):
				panAmount = max(panAmount, maxPan)
		else:
			panAmount = maxPan
		panRate = panAmount

		if (rotate != [0, 0, 0]):
			camera.rotate(rotate, rotSpeed)
		frameStart = time.time()
		if self.pause == -1 and Buffer.bufferMode != 2: self.Time += delta

		doStep = (self.pause == -1 and Buffer.bufferMode != 2)
		camera.step((delta if doStep else 0), pan, panAmount)
		if (abs(camera.pos) > 1e5):
			self.commonShiftPos = -camera.pos
		for m in sorted(markerList, key = lambda x: abs(x.pos - camera.pos), reverse = True):
			camera.drawParticle(m)
		clickTarget = None
		if (self.clickTarget):
			clickTarget = self.clickTarget.pop(0)
			if (clickTarget[2] == 0):
				camera.panTrackSet()
			elif (clickTarget[2] == 1):
				camera.rotTrackSet()
		if camera.panTrack:
			camera.panFollow()
		if camera.rotTrack:
			camera.rotFollow()
		self.closestParticle = None

		# camera.pos += self.commonShiftPos
		for I, p  in enumerate(particleList):
			# if self.commonShiftPos:
			# 	p.pos += self.commonShiftPos
			if (I > 0 and (abs(p.pos - camera.pos) > abs(particleList[I - 1].pos - camera.pos))):
				# Swap the previous one with the current one
				particleList = particleList[:I - 1] + [particleList[I], particleList[I-1]] + particleList[I + 1:]

			pWarp = warpedDistance(p)
			if (self.closestParticle == None):
				self.closestParticle = p#abs(p.pos - camera.pos) - p.radius
			elif (pWarp and pWarp < warpedDistance(self.closestParticle)):
				self.closestParticle = p
			if (doStep):
				p.step(delta, camera)

			buff = Buffer.processPosition(p) # Returns something if it wants anything other than the actual particle to be drawn
			if not buff:
				drawResult = camera.drawParticle(p, box = (self.target == p and self.displayData))
			else:
				# Buff returned something, which means it wants the camera
				# to draw something other than the particle's actual position
				drawResult = camera.drawAt(buff[0], buff[1], buff[2], box = (self.target == p and self.displayData))

			if DRAW_VEL_VECS and drawResult:
				vecResult = camera.drawParticle([buff[0] + buff[3] * DRAW_VEL_VECS, 1, [0, 1, 0]], drawAt=True, point=True)
				accResult = camera.drawParticle([buff[0] + buff[4] * DRAW_VEL_VECS * 5, 1, [1, 0, 0]], drawAt=True, point=True)
				if vecResult:
					drawLine((vecResult[0], vecResult[1]), (drawResult[0], drawResult[1]), fill = [0, 1, 0])
				if accResult:
					drawLine((accResult[0], accResult[1]), (drawResult[0], drawResult[1]), fill = [1, 0, 0])

			if (clickTarget):
				if (drawResult):
					clickX   = clickTarget[0]
					clickY   = clickTarget[1]
					clickBut = clickTarget[2]
					drawX   = drawResult[0]
					drawY   = drawResult[1]
					drawRad = drawResult[2]
					# print("Distance from particle of mass %d: %.3lf" % (p.mass, abs(vector([clickX, clickY]) - vector([drawX, drawY]))))
					if (abs(vector([clickX, clickY]) - vector([drawX, drawY])) < drawRad):
						if (clickBut == 0):
							# Left click
							camera.panTrackSet(p)
						elif (clickBut == 1):
							# Right click
							camera.rotTrackSet(p)

		frameEnd = time.time()
		frameLength = frameEnd - frameStart
		if (frameLength == 0):
			FPS = 999
		else:
			FPS = 1 / frameLength
		if FRAME_LIMIT:
			if (FPS > FRAME_LIMIT):
				time.sleep(1/FRAME_LIMIT - 1/FPS)
				frameEnd = time.time()
				frameLength = frameEnd - frameStart
				if (frameLength == 0):
					FPS = 999
				else:
					FPS = 1 / frameLength
			elif (FPS == 999):
				time.sleep(1/FRAME_LIMIT)
				frameEnd = time.time()
				frameLength = frameEnd - frameStart
				if (frameLength == 0):
					FPS = 999
				else:
					FPS = 1 / frameLength
		self.FPS -= self.FPS / FPS_AVG_COUNT
		self.FPS += FPS / FPS_AVG_COUNT

		if (AUTO_ABORT):
			if (FPS < 1):
				if (self.frameWarning):
					self.abort()
				else:
					self.frameWarning = True
			else:
				self.frameWarning = False
		if self.displayData: self.showData()
		self.Zero()


class camera:
	# Main job: work out where a dot should go on the screen given the cameras position and rotation and the objects position.
	def __init__(self, pos = vector(DEFAULT_ZERO_VEC), rot = vector(DEFAULT_UNIT_VEC), vel = vector(DEFAULT_ZERO_VEC), screenDepth = defaultScreenDepth):
		self.pos = pos
		self.rot = rot.setMag(1)
		self.vel = vel
		# self.trackSeparate = vector([100, 0, 0])
		self.rotTrackOrigin = DEFAULT_UNIT_VEC
		self.screenDepth = screenDepth
		self.screenXaxis = vector([-self.rot[2], 0, self.rot[0]], unit=True)
		self.screenYaxis = vector([
			 -self.rot[0]    * self.rot[1],
			 (self.rot[0]**2 + self.rot[2]**2),
			 -self.rot[2]    * self.rot[1]
		], unit=True)
		self.panStart = self.pos # When flying to a position, the speed is based on the progress from start to finish.
		self.rotStart = self.rot # Similar to above but for rotation

	# total distance, maxSpeed, destination, at speed(0, 1 or 2), stopping distance, position of closest particle at start.
	# Stored so they aren't calculated each step.
	panInfo = [0, 0, vector([0, 0, 0]),
	 			0, 0, vector([0, 0, 0])]
	screenRadius = 0 #(screenWidth()**2 + screenHeight()**2)**(1/2)
	panTrack = None
	rotTrack = None
	panTrackLock = False # Once the pan or rotation tracking has sufficiently closed in on the target,
	rotTrackLock = False # don't allow any 'slippage', ie lock on firmly to the target
	moving = False # To go to a particle, just activate pan and rotational
				   # tracking on the target until they both have locked on
	absolutePan = vector([0, 0, 0])

	def setScreenDepth(self, value, increment=False):
		if increment:
			self.screenDepth += value
			difference = value
		else:
			difference = value - self.screenDepth
			self.screenDepth = value
		# self.pos -= self.rot * difference

	#   Checks if the camera is still moving to the particle or if it has arrived
	def checkMoving(self):
		if (self.moving):
			if not (self.panTrack or self.rotTrack):
				self.moving = False

	def goTo(self, particle):
		self.moving = True
		self.rotTrackSet(particle)
		# self.panTrackSet(particle)

	def rotate(self, direction, rate):
		# direction as a 2 element list [x, y]
		self.screenXaxis = self.screenXaxis.rotateAbout(self.screenYaxis, direction[0] * rate)
		self.screenYaxis = self.screenYaxis.rotateAbout(self.screenXaxis, direction[1] * rate)
		self.rot = self.screenYaxis.cross(self.screenXaxis)
		self.screenXaxis = self.screenXaxis.rotateAbout(self.rot,         direction[2] * rate)
		self.screenYaxis = self.screenYaxis.rotateAbout(self.rot,         direction[2] * rate)
		self.rot.setMag(1)

	# This executes a step for the camera, applying it's velocity to get a new position.
	# NB: The cameras velocity is in m/step, not m/s. To follow a target the velocity must be
	# 	converted from the particles m/s to m/step for the camera, simply by
	# 	multiplying the velocity in m/s by the time step (delta)
	def step(self, delta, pan=[0, 0, 0], panRate=1):
		self.screenRadius = (screenWidth()**2 + screenHeight()**2)**(1/2)
		panShift = (pan[0] * self.screenXaxis +
					pan[1] * self.screenYaxis +
					pan[2] * self.rot) * panRate

		if (panShift and self.panTrack and not self.panTrackLock):
			self.panTrackSet()

		self.vel = panShift
		if self.panTrack:
			self.vel += self.panTrack.vel * delta
			# self.trackSeparate += panShift
		self.vel += self.absolutePan
		self.pos += self.vel
		self.absolutePan *= 0

	def panTrackSet(self, target = None):
		# panInfo: [total distance, maxSpeed, destination, atSpeed (0, 1 or 2), stopping distance]. Stored so they aren't calculated each step.
		self.panTrack = target
		self.panTrackLock = False
		if target:
			minDist = target.pos
			for p in particleList:
				if (p == target): continue
				if (abs(p.pos - self.pos) < abs(minDist - self.pos)):
					minDist = p.pos
			self.panInfo[5] = minDist
			self.panStart = self.pos.getClone()
			if ((20 * target.radius) < abs(self.pos - target.pos)):
				destination = self.rot.mag(-20 * target.radius)
			else:
				destination = self.pos - target.pos
			self.panInfo[0] = abs(target.pos + destination - self.pos)
			travelSteps = max(2 * MainLoop.FPS, TRAVEL_STEPS_MIN) # No less than 100 steps
			self.panInfo[1] = self.panInfo[0] / travelSteps
			self.panInfo[2] = target.pos + destination
			self.panInfo[3] = 0 # at speed: 0 for accelerating, 1 for at speed, 2 for slowing down.
			self.panInfo[4] = (self.panInfo[1] / FOLLOW_RATE_COEFF)
		# print("Setting panTrack to %s from %s, mag %s" % (self.trackSeparate.string(2), "none" if not target else target.name, numPrefix(abs(self.trackSeparate), "m", 2)))
			# print("Travel steps: {}, Total distance: {}, maxSpeed: {}, stopping distance: {}".format(travelSteps, self.panInfo[0], self.panInfo[1], self.panInfo[4]))
		return target

	def rotTrackSet(self, target = None):
		# print("Setting rot")
		self.rotTrack = target
		if target:
			self.rotTrackLock = False
			self.rotStart = self.rot.getClone()
		return target

	# Not used, this can be removed
	def autoRate(self, rate, distance):
		newRate = dist * 0.5# * rate/(AUTO_RATE_CONSTANT)
		return newRate

	def zeroCameraPosVel(self):
		MainLoop.commonShiftPos = self.pos.negate()
		# MainLoop.commonShiftVel = self.vel.negate()

	# Returns values for use in drawParticle or False if particle not on screen
	def onScreen(self, particle):
		relPosition = particle.pos - self.pos
		if (relPosition.dot(self.rot) <= 0):
			return False
		if (particle.radius >= abs(relPosition)):
			return False
		if ("absmag" in particle.info):
			appMag = particle.info["absmag"] + 5 * log(abs(particle.pos - self.pos) / (10 * PARSEC), 10)
			if (appMag > MAX_VISIBILE_MAG):
				return False

		offset = atan(particle.radius/abs(relPosition))
		# centreAngle = atan()
		# if (abs(X) - majorAxis > screenWidth()/2 or abs(Y) - majorAxis > screenHeight()/2):
		# 	return False
		return True




	def drawParticle(self, particle, drawAt = False, point=False, box=False):
		# drawAt: if the desired particle isn't actually where we want to draw it, parse [pos, radius [, colour]] and set drawAt = True
		# if not self.onScreen(particle): return False
		self.rot.setMag(1)

		# screenAngleX = atan(( turtle.window_width() / 2 ) / self.screenDepth)
		# screenAngleY = atan(( turtle.window_height() / 2 ) / self.screenDepth)
		if drawAt:
			pos = particle[0]
			radius = particle[1]
			colour = particle[2]
		else:
			appMag = None
			if ("absmag" in particle.info):
				appMag = particle.info["absmag"] + 5 * log(abs(particle.pos - self.pos) / (10 * PARSEC), 10)
				particle.info["appmag"] = appMag
				if (appMag > MAX_VISIBILE_MAG):
					return False
			pos = particle.pos
			radius = particle.radius
			colour = particle.colour

		# Get relative position to camera's position.


		relPosition = pos - self.pos
		distance = abs(relPosition)
		if (relPosition.dot(self.rot) <= 0):
			# Only condition to exit draw if ALWAYS_DRAW is True
			return False
		if (distance < radius):
			# and this one
			return False
		ScreenParticleDistance = self.screenDepth * abs(relPosition) * abs(self.rot) / (relPosition.dot(self.rot))
		relPosOnScreen = relPosition * ScreenParticleDistance / abs(relPosition)
		relPosUnit = relPosition / abs(relPosition)
		relRotation = relPosUnit - self.rot
		x_r, y_r, z_r = self.rot.elements
		x_CSP, y_CSP, z_CSP = relPosOnScreen.elements
		x_CSC, y_CSC, z_CSC = self.rot.getClone().setMag(self.screenDepth).elements

		X = relPosOnScreen.dot(self.screenXaxis) / abs(self.screenXaxis)
		Y = relPosOnScreen.dot(self.screenYaxis) / abs(self.screenYaxis)

		# centreAngleX = acos((2 - abs(relRotation.lock([0, 2])) ** 2) / 2)
		# centreAngleY = acos((2 - abs(relRotation.lock([0, 1])) ** 2) / 2)
		# offset: angle either side of centre angle which is slightly distorted due to the 3d bulge of the sphere.
		offset = asin(radius/distance)
		centreAngle = acos(min(1, self.screenDepth / ScreenParticleDistance))
		minAngle = centreAngle - offset
		screenAngle = atan(self.screenRadius / self.screenDepth)
		if (minAngle > screenAngle):
			return False
		if (radius >= distance and not point):
			# prin += ("Inside particle, not drawing")
			# if PRINT_DATA: print(prin)
			return False
		if point:
			majorAxis, minorAxis = 1, 1
		else:
			majorAxis = 2 * (sqrt(X ** 2 + Y ** 2) - self.screenDepth * tan( atan(sqrt(X ** 2 + Y ** 2) / self.screenDepth ) - offset))
			minorAxis = 2 * self.screenDepth * tan(offset)
		if (not point and not ALWAYS_DRAW and (abs(X) - majorAxis > screenWidth()/2 or abs(Y) - majorAxis > screenHeight()/2)):
			# prin = prin + ("Outside of screen, x: " + str(X) + ", y: " + str(Y) + ", major axis: " + str(majorAxis))
			return False
		if X != 0:
			angle = atan(Y / X)
		elif X == 0 and Y == 0:
			angle = 0
		else:
			angle = pi/2
		drawOval(X, Y, majorAxis, minorAxis, angle, colour, box, mag=appMag)
		return [X, Y, majorAxis, minorAxis]

	def drawAt(self, posVector, radius, colour = None, box=False):
		return self.drawParticle([posVector, radius, colour], True, box=box)

	def panFollow(self):
		if self.panTrack == None: return False
		if self.panTrackLock: return True
		# Choose the follow rate so that the approach takes approx
		# 5 seconds whilst at max speed, dont worry about time accelerating
		panDest = self.panInfo[2]
		relPos = (panDest - self.pos)
		distTravelled = abs(self.pos - self.panStart)
		remDist = abs(relPos)
		if (self.panInfo[3]):
			# At speed, get ready to slow down.
			speed = self.panInfo[1]
			if (self.panInfo[3] == 2 or remDist <= self.panInfo[4]):
				# CLose enough to start slowing down.
				speed = FOLLOW_RATE_COEFF * remDist
				self.panInfo[3] = 2
		else:
			# Accelerating to max speed.
			speed = max(FOLLOW_RATE_COEFF * distTravelled**FOLLOW_RATE_BASE, 0.0001*abs(self.panInfo[5] - self.pos))
			if (speed >= self.panInfo[1]):
				self.panInfo[3] = 1
				speed = self.panInfo[1]

		if (self.panInfo[3] == 2 and speed <= 0.0001*abs(self.panTrack.pos - self.pos)):
			# Close enough to lock on
			speed = abs(relPos)
			self.panTrackLock = True
		vel = relPos.mag(speed)
		self.absolutePan = vel
		return True

	def rotFollow(self, followRate=DEFAULT_ROTATE_FOLLOW_RATE):
		if self.rotTrack == None: return False
		if self.rotTrackLock:
			followRate = 1

		relPos   = (self.rotTrack.pos - self.pos).mag(1)

		relAngle = relPos.relAngle(self.rot)
			# shift is equivalent to a portion of the arc from the current rotation to the end rotation.
		shift    = followRate * (relAngle + 0.01) if (relAngle > 0.01 and followRate != 1) else relAngle
			# shiftMag is shift modified so that adding it to rot results in a rotation of 'shift' through that arc
		shiftMag = sin(shift) / (cos(relAngle/2 - shift))
			# rotShift is simply a vector from the current rotation to the desired rotation of magnitude shiftMag
		rotShift = (relPos - self.rot).mag(shiftMag)

		self.rot += rotShift

		if not self.rotTrackLock and relAngle:
			self.lockRot()

		self.screenXaxis = self.rot.cross(self.screenYaxis)
		self.screenYaxis = self.screenXaxis.cross(self.rot)

		self.screenXaxis.setMag(1)
		self.screenYaxis.setMag(1)
		self.rot.setMag(1)
		return True

	def lockPan(self):
		if (self.moving):
			if self.rotTrack == None:
				self.panTrackSet()
				self.moving = False
		else:
			self.panTrackLock = True

	def lockRot(self):
		if (self.moving):
			self.rotTrackSet()
			if self.panTrack == None:
				self.moving = False
		else:
			self.rotTrackLock = True

markerList = []

autoRateValue = maxPan
pan = [0, 0, 0, False]
shiftL = False
rotate = [0, 0, 0]

def panRight():
	if pan[0] < 1:
		pan[0] += 1

def panLeft():
	if pan[0] > - 1:
		pan[0] -= 1

def panBack():
	if pan[2] > - 1:
		pan[2] -= 1

def panForward():
	if pan[2] < 1:
		pan[2] += 1

def panDown():
	if pan[1] > - 1:
		pan[1] -= 1

def panUp():
	if pan[1] < 1:
		pan[1] += 1

def panFast():
	global shiftL
	shiftL = True
	pan[3] = True

def panSlow():
	global shiftL
	shiftL = False
	pan[3] = False

def rotRight():
	if rotate[0] < 1:
		rotate[0] = rotate[0] + 1

def rotLeft():
	if rotate[0] > -1:
		rotate[0] = rotate[0] - 1

def rotDown():
	if rotate[1] < 1:
		rotate[1] += 1

def rotUp():
	if rotate[1] > -1:
		rotate[1] -= 1

def rotAntiClock():
	if rotate[2] < 1:
		rotate[2] += 1

def rotClockWise():
	if rotate[2] > -1:
		rotate[2] -= 1

def escape():
	global Running
	Running = False

def pause():
	MainLoop.pause *= -1
	if Buffer.bufferMode == 1:
		bufferPlay()

def leftClick(x, y):
	MainLoop.clickTarget.append([x, y, 0])    # 0 for left click, 1 for right

def rightClick(x, y):
	MainLoop.clickTarget.append([x, y, 1])    # 0 for left click, 1 for right

def upScreenDepth():
	camera.setScreenDepth(10, True)

def downScreenDepth():
	camera.setScreenDepth(-10, True)

def upMaxMag():
	global MAX_VISIBILE_MAG
	MAX_VISIBILE_MAG += 0.1

def downMaxMag():
	global MAX_VISIBILE_MAG
	MAX_VISIBILE_MAG -= 0.1

def upDelta():
	# global Delta
	MainLoop.setDelta(MainLoop.Delta * 1.2)

def downDelta():
	# global Delta
	MainLoop.setDelta(MainLoop.Delta * 1 / 1.2)

def revDelta():
	# global Delta
	MainLoop.setDelta(MainLoop.Delta * -1)

def toggleRealTime():
	global REAL_TIME
	REAL_TIME = False if REAL_TIME else True

def bufferRecord():
	Buffer.bufferMode = 1

def bufferPlay():
	if MainLoop.pause == 1:
		pause()
	Buffer.bufferMode = 2

def togglePanTrack():
	if MainLoop.target:
		if camera.panTrack:
			camera.panTrackSet()
		else:
			camera.panTrackSet(MainLoop.target)
	else:
		camera.panTrackSet()

def toggleRotTrack():
	if MainLoop.target:
		if camera.rotTrack:
			camera.rotTrackSet()
		else:
			camera.rotTrackSet(MainLoop.target)
	else:
		camera.rotTrackSet()

def goToTarget():
	if MainLoop.target:
		camera.goTo(MainLoop.target)

def toggleScreenData():
	# MainLoop.target = None
	MainLoop.displayData = False if MainLoop.displayData else True

def cycleTargets():
	global planetList
	global shiftL
	try:
		if not shiftL:
			if MainLoop.target:
				MainLoop.target = (planetList + [planetList[0]])[planetList.index(MainLoop.target) + 1]
			else:
				MainLoop.target = planetList[0]
		else:
			if MainLoop.target:
				MainLoop.target = planetList[planetList.index(MainLoop.target) - 1]
			else:
				MainLoop.target = planetList[-1]
	except NameError:
		return

def clearTarget():
	MainLoop.target = None



def search(term=None):
	global TestMode
	if TestMode: return False
	if term == None: term = turtle.textinput("Search for a body", "Enter a search term:")
	if not term:
		turtle.listen()
		return False
	bestBody = None
	for body in Pmodule.particleList:
		if not body.name: continue
		if term == body.name:
			MainLoop.target = body
			break
		else:
			if term.lower() in body.name.lower():
				if bestBody:
					if bestBody.name > body.name:
						bestBody = body
				else:
					bestBody = body
			# match = (sum([(1 if term[i].lower() == body.name[i].lower() else 0) for i in range(minLength)]) / minLength)
			# if (match > bestMatch):
			# 	bestMatch = match
			# 	bestBody = body
	# if bestMatch:
	# 	MainLoop.target = bestBody
	if bestBody:
		MainLoop.target = bestBody
		turtle.listen()
		return True
	else:
		turtle.listen()
		return False



DEFAULT_ZERO_VEC = vector(DEFAULT_ZERO_VEC)
DEFAULT_UNIT_VEC = vector(DEFAULT_UNIT_VEC)
MainLoop = MainLoop()

panRate = 0 # Will be used to store the pan rate of each step


camera = camera(pos = vector([0, 0, 0]))

setup()
Running = True


if preset == 1:
	# for i in range(10):
	# 	particle(50 + i*20, vector([50, 100 - 10*i, 0]))
	# Cloud of particles orbiting a big thing
	MainLoop.addData("Pan speed", "round(panRate, 2)", True)
	MainLoop.addData("Camera pan lock", "camera.panTrackLock", True)
	MainLoop.addData("Camera rot lock", "camera.rotTrackLock", True)
	particle(25000, vector([defaultScreenDepth, 0, 0]))
	for i in range(PARTICLE_COUNT):
		particle(variableMass, vector([150 + defaultScreenDepth, 0, 0]) + randomVector(3, 50, 400)).circularise(particleList[0])
elif preset == 2:
	# Galaxy kinda thing
	MainLoop.addData("Pan speed", "round(panRate, 2)", True)
	MainLoop.addData("Camera pan lock", "camera.panTrackLock", True)
	MainLoop.addData("Camera rot lock", "camera.rotTrackLock", True)

	minDist, maxDist = 25, 250
	COM = vector([0, 0, 0])     # Centre of mass
	particleMass = variableMass
	centreVec = vector([defaultScreenDepth, 0, 0])
	for i in range(PARTICLE_COUNT):
		randomVec = randomVector(3, minDist, maxDist, [1, 0, 1])
		randomVec = randomVec.setMag(maxDist * (abs(randomVec) / maxDist)**2)
		particle(particleMass, centreVec + randomVec + randomVector(3, 25))
		COM += particleList[-1].pos

	COM = COM / PARTICLE_COUNT
	# totalMass = PARTICLE_COUNT * particleMass
	for p in particleList:
		forceVec = vector([0, 0, 0])
		for p2 in particleList:
			if p2 == p: continue
			forceVec += (p.pos - p2.pos).setMag(particle.G * p.mass * p2.mass / (abs(p.pos - p2.pos)**2))
		velVec = forceVec.cross(vector([0, 1, 0]))
		velVec.setMag(sqrt(abs(forceVec.dot(p.pos - COM) / p.mass)))
		p.vel = velVec
		# p.circularise([totalMass / 2, COM], axis = vector([0, 1, 0]))
elif preset == 3:
	if (not args["-G"][-1]): Pmodule.G = 6.67408e-11

	if (not args["-sf"][-1]): smoothFollow = 0.04

	MainLoop.addData("Pan speed", "numPrefix(panRate, 'm/step', 2)", True)
	MainLoop.addData("Camera pan lock", "camera.panTrackLock and camera.panTrack.name", True)
	MainLoop.addData("Camera rot lock", "camera.rotTrackLock and camera.rotTrack.name", True)

	AUTO_RATE_CONSTANT = 1.0e9
	Pmodule.ALL_IMMUNE = True
	planetList = []
	planets = {}
	colours = {
		"Moon"		: [1,	1, 	 1],  # Photo realistic moon white
		"Earth"		: [0,   0.5, 1],  # Photo realistic ocean blue
		"Sun"		: [1,   1,   0],
		"Mercury"	: [1,   0.5, 0],
		"Venus"		: [1,   0.3, 0],
		"Mars"		: [1,   0,   0],
		"Jupiter"	: [1,   0.6, 0.2],
		"Saturn" 	: [1,   0.8, 0.5],
		"Uranus"	: [0.5, 0.5, 1],
		"Neptune"	: [0.2, 0.2, 1]
	}
	print("Loading planets...")
	Data = loadSystem.loadFile(DATA_FILE)
	MainLoop.addDataLine()
	MainLoop.addData("Track target", "MainLoop.target.name", True, "None")
	MainLoop.addData("Mass", "str(MainLoop.target.mass) + 'kg'", True, "---")
	MainLoop.addData("Radius", "numPrefix(round(MainLoop.target.radius, 2), 'm')", True, "---")
	MainLoop.addData("XYZ Velocity", "(MainLoop.target.vel.string(2)) + ', mag: ' + numPrefix(round(abs(MainLoop.target.vel), 5), 'm/s')", True, "---")
	MainLoop.addData("Distance to Target", "")
	MainLoop.addData("Centre", "numPrefix( round( abs( MainLoop.target.pos - camera.pos ), 2 ), 'm' )", True, "---")
	MainLoop.addData("Surface", "numPrefix( round( abs( MainLoop.target.pos - camera.pos ) - MainLoop.target.radius, 2 ), 'm' )", True, "---")
	MainLoop.addData("Speed of camera", "numPrefix(abs(camera.vel), 'm/step', 2)", True, "---")
	MainLoop.addData("Target speed relative to camera", "(numPrefix(abs(camera.panTrack.vel - camera.vel / MainLoop.Delta), 'm/s') if abs(camera.panTrack.vel - camera.vel / MainLoop.Delta) > 0.0001 else 0)", True, "---")
	MainLoop.addDataLine()

	bigVec = vector([0, 0, 0])
	for planet in Data:
		data = Data[planet]
		if (planet == "$VAR"):
			if ("TIME" in Data[planet]): MainLoop.Time = Data[planet]["TIME"]
			continue

		if data["$valid"]:
			pos = vector([data["X"], data["Y"], data["Z"]]) * 1000
			vel = vector([data["VX"], data["VY"], data["VZ"]]) * 1000
			mass = data["MASS"]
			density = data["DENSITY"]
			new = particle(mass, pos, vel, density=density, autoColour=False,
						colour=(colours[planet] if planet in colours else [0.5, 0.5, 0.5]),
						limitRadius=False, name=planet)
			new.info["appmag"] = 0
			if data["ABSMAG"]: new.info["absmag"] = data["ABSMAG"]
			planetList.append(new)
			planets[planet] = new
			bigVec += new.pos
	camera.pos = bigVec
	MainLoop.target = planets["Earth"]
	if "Phobos" in planets:
		planets["Phobos"].immune = False # Screw you phobos
	MainLoop.addData("Absolute Magnitude", "MainLoop.target.info['absmag']", True, "---")
	MainLoop.addData("Apparent Magnitude", "round(MainLoop.target.info['appmag'],2)", True, "---")

	if makeAsteroids:
		beltRadius = (AsteroidsEnd - AsteroidsStart) / 2
		beltCentre = (AsteroidsEnd + AsteroidsStart) / 2
		for i in range(makeAsteroids):
			pos = randomVector(3, beltCentre, fixComponents=[1, 1, 0])
			offset = randomVector(3, 0, beltRadius)
			offset *= (abs(offset) / beltRadius) ** 2
			offset.elements[2] *= 1/5
			density = AsteroidsDensity
			mass = random.random() * (AsteroidsMaxMass - AsteroidsMinMass) + AsteroidsMinMass
			new = particle(mass, planets["Sun"].pos + pos + offset, autoColour=False, colour = "grey", limitRadius=False)
			new.circularise(planets["Sun"], axis = vector([0, 0, -1]))

	earthVec = planets["Earth"].pos
	radius   = planets["Earth"].radius + 150000

	if makeSatellites:
		for i in range(makeSatellites):
			offset = randomVector(3, radius)
			particle(1000, earthVec + offset, autoColour = False, colour = "grey").circularise(planets["Earth"])

	if getStars:
		print("Loading stars...")
		MainLoop.addData("Maximum visible magnitude", "round(MAX_VISIBILE_MAG,2)", True)
		MainLoop.addData("Earth magnitude", "MainLoop.target.info['mag']", True, "---")
		MainLoop.addData("Hipparcos catalog id", "MainLoop.target.info['HIP id']", True, "---")
		STARS_DATA = loadSystem.loadFile("StarsData.txt", key=["$dist != 100000", "(\"$proper\" != \"None\") or ($mag < {})".format(getStars)])
		for STAR_key in STARS_DATA:
			if STAR_key == "$VAR" or STAR_key[0] in ["~", "!"]: continue
			STAR = STARS_DATA[STAR_key]
			X = STAR["x"]
			Y = STAR["y"]
			Z = STAR["z"]
			vX = STAR["vx"]
			vY = STAR["vy"]
			vZ = STAR["vz"]
			# print("Looking at star:", STAR["proper"], end = "")
			massIndex = random.random() * 10 + 30
			new = particle(10**(massIndex), vector([X, Y, Z]) * PARSEC,
				vector([vX, vY, vZ]) * PARSEC / YEAR, static=True,
				name=STAR["proper"], density=1e3)

			planetList.append(new)
			new.info["appmag"] = 0
			new.info["absmag"] = STAR["absmag"]
			new.info["mag"] = STAR["mag"]
			new.info["HIP id"] = "None" if not STAR["hip"] else int(STAR["hip"])
	if search("Acrux"): toggleRotTrack()
	search("Pluto")
	togglePanTrack()
	clearTarget()

elif preset == 4:
	# defaultDensity = 10
	Sun = particle(300000, vector([0, 0, 0]), density=10, name="Sun")
	for i in range(PARTICLE_COUNT):
		radius = i / (PARTICLE_COUNT - 1) * (PRESET_4_MAX_RADIUS - PRESET_4_MIN_RADIUS) + PRESET_4_MIN_RADIUS
		particle(variableMass, vector([radius, 0, 0]), density=10)
		particleList[-1].circularise(Sun, axis = vector([0, -1, 0]))
	camera.pos = vector([0, 0, radius])
	camera.rotTrackSet(Sun)

# if not TestMode:

if not TestMode:
	window = turtle.Screen()
	window.setup(width = 1.0, height = 1.0)
	turtle.bgcolor([0, 0, 0])

	turtle.tracer(0, 0)             # Makes the turtle's speed instantaneous
	turtle.hideturtle()

	turtle.onkeypress(panLeft, "a")
	turtle.onkeyrelease(panRight , "a")

	turtle.onkeypress(panRight, "d")
	turtle.onkeyrelease(panLeft , "d")

	turtle.onkeypress(panForward, "w")
	turtle.onkeyrelease(panBack , "w")

	turtle.onkeypress(panBack, "s")
	turtle.onkeyrelease(panForward , "s")

	turtle.onkeypress(panUp, "r")
	turtle.onkeyrelease(panDown , "r")

	turtle.onkeypress(panDown, "f")
	turtle.onkeyrelease(panUp , "f")

	turtle.onkeypress(panFast, "Shift_L")
	turtle.onkeyrelease(panSlow, "Shift_L")

	turtle.onkeypress(rotRight, "Right")
	turtle.onkeyrelease(rotLeft, "Right")

	turtle.onkeypress(rotLeft, "Left")
	turtle.onkeyrelease(rotRight, "Left")

	turtle.onkeypress(rotUp, "Up")
	turtle.onkeyrelease(rotDown, "Up")

	turtle.onkeypress(rotDown, "Down")
	turtle.onkeyrelease(rotUp, "Down")

	turtle.onkeypress(rotClockWise, "e")
	turtle.onkeyrelease(rotAntiClock, "e")

	turtle.onkeypress(rotAntiClock, "q")
	turtle.onkeyrelease(rotClockWise, "q")

	turtle.onkey(escape, "Escape")
	turtle.onkey(pause,  "space")


	turtle.onkey(cycleTargets, "Tab")
	turtle.onkey(togglePanTrack, "t")
	turtle.onkey(toggleRotTrack, "y")
	turtle.onkey(clearTarget,    "c")
	turtle.onkey(goToTarget,	 "g")
	turtle.onkey(toggleRealTime, "i")

	turtle.onkey(toggleScreenData, "h")

	turtle.onkeypress(upScreenDepth, "'")
	turtle.onkeypress(downScreenDepth, ";")

	turtle.onkeypress(upMaxMag, ".")
	turtle.onkeypress(downMaxMag, ",")

	turtle.onkey(upDelta, "]")
	turtle.onkey(downDelta, "[")
	turtle.onkey(revDelta, "\\")

	turtle.onscreenclick(leftClick, 1)
	turtle.onscreenclick(rightClick, 3)

	turtle.onkey(bufferRecord, "n")
	turtle.onkey(bufferPlay, "m")

	turtle.onkey(search, "/")

if TestMode:
	try:
		print("Running simulation with delta time step of %s/step" % (timeString(Delta)))
	# 	print("""	Note that with leapfrog arithmetic,
	# velocity and position are technically never both known at the same time,
	# but that shouldn't affect results significantly.""")
		Time = MainLoop.Time
		checkTimes = sorted([testData[x][0] for x in testData])
		# checkNames = [x for x in testData]
		flag = False
		# We know there is test data because otherwise the program would have exited by now
		startTime = Time
		stepCounter = 1
		startSim = time.time()
		# [print(x.name) for x in particleList]
		tempDelta = False
		progressStep = 1
		progressPoint = 0
		print("Progress :..", end = "")
		while checkTimes:
			progress = 100 * (Time - startTime) / (checkTimes[0] - startTime)
			if (progress >= progressPoint):
				print("\rProgress: %d%%" % (progressPoint), end = "")
				progressPoint += progressStep
			# print("\rProgress: %.2f%%" % (100 * (Time - startTime) / (checkTimes[-1] - startTime)), end = "")
			sys.stdout.flush()

			if Time >= checkTimes[0]:
				for p in particleList:
					if ((p.name in testData) and (False if not checkTimes else checkTimes[0] == testData[p.name][0])):
						# Check the data.
						targetData = testData[p.name]
						targetTime = targetData[0]
						targetPos  = targetData[1]
						targetVel  = targetData[2]
						print("\nAt time: %s, for %s:" %(timeString(Time), p.name))
						print("\tShould be at:    %s\twith vel: %s (mag: %s)" % (targetPos.string(2), targetVel.string(2), numPrefix(abs(targetVel), "m/s")))
						print("\tWas actually at: %s\twith vel: %s (mag: %s)" % (p.pos.string(2), p.vel.string(2), numPrefix(abs(p.vel), "m/s")))
						print("\tOffset by        %s (mag: %s) over %d steps of %lfs, average %s/step or %s" % (
							(p.pos - targetPos).string(2),
							numPrefix(abs(p.pos - targetPos), "m", 3),
							stepCounter, (Delta if not tempDelta else tempDelta),
							numPrefix(abs(p.pos - targetPos) / stepCounter, "m", 3),
							numPrefix(abs(p.pos - targetPos) / (stepCounter * Delta), "m/s", 3))
						)
						print()
						checkTimes.pop(0)
						progressPoint = 0
						# flag = len(checkTimes)
					p.step(Delta)
			else:
				if (tempDelta):
					Delta = tempDelta
					tempDelta = False
				if (Time + Delta > checkTimes[0]):
					tempDelta = Delta
					# print("Time + Delta = %lf, greater than %f, setting Delta to %f" % (Time + Delta, checkTimes[0], checkTimes[0] - Time))
					Delta = checkTimes[0] - Time
				for p in particleList:
					p.step(Delta)
			Time += Delta
			stepCounter += 1
			if stepCounter == 100:
				interval = time.time() - startSim
				# Covered 50 * Delta in interval seconds, ie (50*Delta simSeconds / interval realSeconds)
				simSpeed = 100*Delta / interval
				remainingTimeFirst = checkTimes[0] - Time
				if len(checkTimes) > 1:
					remainingTimeLast = checkTimes[-1] - Time
					remainingSimTimeFirst = remainingTimeFirst / simSpeed
					remainingSimTimeLast  = remainingTimeLast  / simSpeed
					print("\nEstimated remaining time for first data: %s, and for last: %s" % (timeString(round(remainingSimTimeFirst, 2)), timeString(round(remainingSimTimeLast, 2))))
				else:
					remaingSimTime = remainingTimeFirst / (simSpeed)
					print("\nEstimated remaining time: %s" % (timeString(round(remaingSimTime, 2))))
	except KeyboardInterrupt:
		print("\nStopping.")
		exit()
	exit()

Buffer = buffer()
turtle.listen()

frameStart = time.time()
MainLoop.setDelta(Delta)
if REAL_TIME:
	Delta = 0
if START_PAUSED:
	pause()
while Running:
	turtle.clear()
	if STAGGERED_SIM: input()
	MainLoop.STEP(camera)
	if REAL_TIME:
		Delta = time.time() - frameStart
		frameStart = time.time()
	turtle.update()
