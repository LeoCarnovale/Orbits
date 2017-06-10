from vector import vector, randomVector
from math import *
import random

particleList = []
markerList   = []

defaultDensity = 1
radiusLimit    = 250

ALL_IMMUNE	   = False
voidRadius 	   = 5000
CAMERA_UNTRACK_IF_DIE = True

G = 1

TestMode = False

class particle:
	def __init__(
				self, mass, position, velocity=0, acceleration=0,
				density=defaultDensity, autoColour=True, colour=[0, 0, 1],
				limitRadius=True, name=None, static=False):
		self.mass = mass
		self.pos = position
		self.dim = len(position.elements)
		self.density = density
		self.limitRadius = limitRadius
		self.name = name
		self.static = static

		self.info = {}

		if velocity == 0:
			self.vel = vector([0 for i in range(self.dim)])
		else:
			self.vel = velocity
		if acceleration == 0:
			self.acc = vector([0 for i in range(self.dim)])
		else:
			self.acc = acceleration
		self.autoColour = autoColour
		self.setRadius()
		if not autoColour:
			self.setColour(colour)
		particleList.append(self)
		if self.pos.dim != self.vel.dim:
			print("This class is badly made! (non consistant dimensions):", self)
		# self.setColour()
		# self.colour = [self.radius/radiusLimit, 0, (radiusLimit - self.radius)/radiusLimit]


	alive = True
	respawn = True
	specialColour = False
	colour = [0, 0, 0]

	inbound = False
	immune = False

	newMass = False # the mass of the particle after it respawns
	# colour parameter only used if autoColour is off
	def setColour(self, colour=None):
		if self.autoColour:
			self.colour = [min(self.radius/radiusLimit, 1), 0, max(1, (radiusLimit - self.radius)/radiusLimit)]
		elif colour:
			self.colour = colour
		else:
			return False

	def setRadius(self):
		self.radius = (0.75 * (self.mass/self.density) / pi) ** (1/3)
		self.setColour()

	def calcAcc(self, other):
		force = (G * self.mass * other.mass) / (abs(self.pos - other.pos) ** 2)
		forceVector = other.pos.subtract(self.pos)
		# drawVector(forceVector.setMag(force/self.mass), self.pos)
		self.acc += (forceVector.setMag(force/self.mass))
		# print("calcAcc:", self.acc.elements)

	def checkCollision(self, other):
		if other.alive and (abs(self.pos.subtract(other.pos)) < self.radius + other.radius):
			self.contest(other)
			return True
		else:
			return False

	def runLoop(self):
		for p in particleList:
			if p != self and type(p) != marker and not p.static:
				if not self.checkCollision(p):
					self.calcAcc(p)


	def checkOutOfBounds(self, camera): #bounds=[turtle.window_width()/2, turtle.window_height()/2]):
		# self.vel.multiplyToMe(0)
		# return
		# global TestMode
		# print(ALL_IMMUNE)
		if self.immune or ALL_IMMUNE or TestMode: return False
		out = False
		if abs(self.pos.subtract(camera.pos)) > voidRadius:
			out = True
		# print("Checking")
		if out and not self.inbound:
			if self.respawn:
				self.respawn()
			else:
				self.die()
		elif not out and self.inbound:
			self.inbound = False


	def respawn(self):
		# print("Name:", self.name)
		# newMass --> determines the mass of the particle after respawning
		# bounds = [turtle.window_width()/2, turtle.window_height()/2]
		radius = voidRadius #sqrt(bounds[0] ** 2 + bounds[1] ** 2) # radius of circle encompassing corners of canvas
		self.pos = randomVector(3, radius * 0.99)
		self.vel = randomVector(3, 5, 15).subtract(self.pos.getClone().setMag(30))
		if not self.newMass: self.mass = random.random() * 2000 + 500
		if self.newMass: self.mass = self.newMass
		self.setRadius()
		# self.inbound = True
		# print("Respawning to: {}".format([self.pos.elements[0], self.pos.elements[1], self.pos.elements[2]]))

	def die(self, killer=None):
		# print(self,"Dying!")
		if self.respawn:
			# if CAMERA_UNTRACK_IF_DIE and camera.panTrack == self:
			# 	camera.panTrackSet(killer)
			self.respawn()
		else:
			if self in particleList:
				if camera.panTrack: camera.panTrackSet()
				if buffer != 0:
					BUFFER[self].append(False)
				particleList.remove(self)
			self.alive = False

	def contest(self, other):
		if self.mass >= other.mass:
			self.vel = (self.vel.multiply(self.mass).add(other.vel.multiply(other.mass))).multiply(1/(self.mass + other.mass))
			self.mass += other.mass
			# Using (mv)_1 + (mv)_2 = (m_1 + m_2)v:
			self.setRadius()
			other.die(self)
		else:
			other.vel = (self.vel.multiply(self.mass).add(other.vel.multiply(other.mass))).multiply(1/(self.mass + other.mass))
			other.mass += self.mass
			other.setRadius()
			self.die(other)

	def step(self, delta, camera, draw=True, drawVel=False, onlyDraw = False, bufferMode = 0):
		if self.static:
			self.pos += self.vel * delta# + self.acc * (delta**2 / 2)
			return False
		oldAcc = self.acc
		self.acc *= 0
		self.runLoop()
		if self.radius > radiusLimit and self.limitRadius:
			self.die()
			return False

		self.vel += (oldAcc + self.acc) * (delta / 2)
		# self.vel += self.acc * delta
		# self.pos += self.vel * delta
		self.checkOutOfBounds(camera)
		# if self.acc.getMag(): #print(self.acc.elements)

		return True

	def circularise(self, other, plane = None, axis=None):
		# If axis is supplied, the resulting orbit is in the direction of the
		# cross product of the displacement vector from the body to parent and the axis
		if other == self:
			return False
		if type(other) == list:
			# Can specify a mass at a position instead of a particle
			# Parse as [mass, position, vel=0]
			mass = other[0]
			position = other[1]
			if (len(other) > 2):
				otherVel = other[2]
			else:
				otherVel = vector([0, 0, 0])
		else:
			mass = other.mass
			position = other.pos
			otherVel = other.vel

		# if inclination == "r":
		#     inclination = random.random() * 360 - 180
		speed = sqrt(G * mass/abs(self.pos - position))
		vel = randomVector(3, 1)
		if (axis == None):
			vel.makeOrthogonal(position - self.pos)
			if plane: vel = vel.lock(plane)#[vel.elements[i] * plane[i] for i in range(len(vel.elements))]
		else:
			vel = axis.cross(position - self.pos)
		vel.setMag(speed)
		self.vel = vel + otherVel
		return True

		# if type(other) == particle:


class marker(particle):
	def __init__(self, position, colour, radius = 20):
		self.pos = position
		self.colour = colour
		self.radius = radius
		markerList.append(self)
	def set_colour(self, colour):
		self.colour = colour

	def step(self, delta):
		pass