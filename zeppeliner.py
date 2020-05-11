import random
import os
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()
dis_width=800
dis_height=400
dis=pygame.display.set_mode((dis_width,dis_height))
pygame.display.update()
pygame.display.set_caption("Zeppeliner")
text_color = (0, 0, 0)
bg_color = (255, 255, 255)

path = '/home/florin/Music/'
songs = [f for f in listdir(path) if isfile(join(path, f))]

def display_song(msg, color):
	font = pygame.font.SysFont(None, 25)
	mesg = font.render(msg, True, color)
	mesg_rect = mesg.get_rect(center=(dis_width/2, dis_height/2))
	dis.blit(mesg, mesg_rect)

def play():
	play = True
	play_song = False
	while play:
		dis.fill(bg_color)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				play = False
				os.system('pkill mpg123')
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_q:
					play = False
					os.system('pkill mpg123')
				if event.key==pygame.K_n:
					play_song = False
					os.system('pkill mpg123')
		if not play_song:
			song = random.choice(songs)
			song_path = path + "'" + song + "'"
			os.system('mpg123 ' + song_path + '&')
			song = song[:-4]
			play_song = True
		if play_song:
			display_song(song, text_color)
		pygame.display.update()

play()
	