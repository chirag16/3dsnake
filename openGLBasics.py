import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random

red = (1, 0, 0)
green = (0, 1, 0)
blue = (0, 0, 1)
white = (1, 1, 1)
sky = (0, 1, 1)
yellow = (1, 1, 0)
black = (0, 0, 0)
gray = (0.5, 0.5, 0.5)
pink = (1, 0, 1)

whiteUB = (255, 255, 255)

def cube(coords, block_size, color = [white], fill = True):
	vertices = ((coords[0] + block_size / 2, coords[1] + block_size / 2, coords[2] + block_size / 2),
				(coords[0] + block_size / 2, coords[1] - block_size / 2, coords[2] + block_size / 2),
				(coords[0] - block_size / 2, coords[1] - block_size / 2, coords[2] + block_size / 2),
				(coords[0] - block_size / 2, coords[1] + block_size / 2, coords[2] + block_size / 2),
				(coords[0] - block_size / 2, coords[1] + block_size / 2, coords[2] - block_size / 2),
				(coords[0] + block_size / 2, coords[1] + block_size / 2, coords[2] - block_size / 2),
				(coords[0] + block_size / 2, coords[1] - block_size / 2, coords[2] - block_size / 2),
				(coords[0] - block_size / 2, coords[1] - block_size / 2, coords[2] - block_size / 2))

	edges = ((0,1),
			(1,2),
			(2,3),
			(3,0),
			(5,6),
			(6,7),
			(7,4),
			(4,5),
			(0,5),
			(1,6),
			(2,7),
			(3,4))

	surfaces = ((0, 1, 2, 3),
				(4, 5, 6, 7),
				(0, 1, 6, 5),
				(2, 1, 6, 7),
				(7, 2, 3, 4),
				(3, 4, 5, 0))
	if not fill:
		glBegin(GL_LINES)
		glColor3fv(black)
		for edge in edges:
			for vertex in edge:
				glVertex3fv(vertices[vertex])
		glEnd()
	else:	
		i = 0
		colors = color
		glBegin(GL_QUADS)
		for surface in surfaces:
			for vertex in surface:
				glColor3fv(colors[i % len(colors)])
				i += 1
				glVertex3fv(vertices[vertex])
		glEnd()

def apple(coords, block_size = 0.25):
	cube(coords, block_size, color = [red, pink])

def snake(snakelist, snakelen, block_size = 0.25):
	if len(snakelist) > snakelen:
		del snakelist[0]

	for xyz in snakelist:
		cube(xyz, block_size, [sky, yellow])

def main():
	# PyGame Initialization
	pygame.init()

	# Game Display
	display_height = 800
	display_width = 800
	pygame.display.set_mode((display_width, display_height), DOUBLEBUF|OPENGL)
	clock = pygame.time.Clock()
	FPS = 15

	block_size = 0.25
	arena_size = 25 * block_size
	x_change, y_change, z_change = 0, 0, 0
	x, y, z = 0, 0, 0
	score = 0
	x_enable = y_enable = z_enable = True

	snakelen = 1
	snakelist = [(x, y, z)]

	apple_x = round((random.randrange( - (arena_size - block_size) / 2, (arena_size - block_size) / 2)) / block_size) * block_size
	apple_y = round((random.randrange( - (arena_size - block_size) / 2, (arena_size - block_size) / 2)) / block_size) * block_size
	apple_z = round((random.randrange( - (arena_size - block_size) / 2, (arena_size - block_size) / 2)) / block_size) * block_size
	apple((apple_x, apple_y, apple_z), block_size)

	# OpenGL Params
	gluPerspective(45, (display_width / display_height), 0.1, 50.0)

	glTranslatef(0.0, 0.0, -2 * arena_size)

	# Main Loop
	game_over = False
	while not game_over:
		# Event Handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					quit()
				elif event.key == pygame.K_RIGHT and x_enable:
					x_change, y_change, z_change = block_size, 0, 0
					x_enable, y_enable, z_enable = False, True, True
				elif event.key == pygame.K_LEFT and x_enable:
					x_change, y_change, z_change = -block_size, 0, 0
					x_enable, y_enable, z_enable = False, True, True
				elif event.key == pygame.K_UP and y_enable:
					x_change, y_change, z_change = 0, block_size, 0
					x_enable, y_enable, z_enable = True, False, True
				elif event.key == pygame.K_DOWN and y_enable:
					x_change, y_change, z_change = 0, -block_size, 0
					x_enable, y_enable, z_enable = True, False, True
				elif event.key == pygame.K_w and z_enable:
					x_change, y_change, z_change = 0, 0, -block_size
					x_enable, y_enable, z_enable = True, True, False
				elif event.key == pygame.K_s and z_enable:
					x_change, y_change, z_change = 0, 0, block_size
					x_enable, y_enable, z_enable = True, True, False
				elif event.key == pygame.K_PLUS: # Cheat Code :p
					snakelen += 1
					score += 1

		# Game Logic
		x += x_change
		y += y_change
		z += z_change

		snakelist.append((x, y, z))

		# Hit Boundaries
		if abs(x) >= abs((arena_size - block_size) / 2) or abs(y) >= abs((arena_size - block_size) / 2) or abs(z) >= abs((arena_size - block_size) / 2):
			game_over = True

		# Got Apple
		if x == apple_x and y == apple_y and z == apple_z:
			apple_x = round((random.randrange( - (arena_size - block_size) / 2, (arena_size - block_size) / 2)) / block_size) * block_size
			apple_y = round((random.randrange( - (arena_size - block_size) / 2, (arena_size - block_size) / 2)) / block_size) * block_size
			apple_z = round((random.randrange( - (arena_size - block_size) / 2, (arena_size - block_size) / 2)) / block_size) * block_size
			snakelen += 1
			score += 1

		for i in range(0, len(snakelist)):
			for j in range(i + 1, len(snakelist)):
				if snakelist[i][0] == snakelist[j][0] and snakelist[i][1] == snakelist[j][1] and snakelist[i][2] == snakelist[j][2]:
					game_over = True 

		# Rendering
		glRotatef(0.1, 0, 1, 0)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		print score
		cube((0, 0, 0), arena_size, color = [gray, white])
		cube((0, 0, 0), arena_size, fill = False)

		apple((apple_x, apple_y, apple_z), block_size)
		snake(snakelist, snakelen)
		pygame.display.flip()
		clock.tick(FPS)

if __name__ == "__main__":
	main()