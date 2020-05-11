import random
import os
import pygame
from os import listdir
from os.path import isfile, join
from mutagen.mp3 import MP3

pygame.init()
dis_width=800
dis_height=400
dis=pygame.display.set_mode((dis_width,dis_height))
pygame.display.update()
pygame.display.set_caption("Zeppeliner")
text_color = (0, 0, 0)
bg_color = (255, 255, 255)
font1 = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont("Courier", 15)

path = '/home/florin/Music/'
songs = [f for f in listdir(path) if isfile(join(path, f))]

def song_length(path, song):
	audio = MP3(path + song)
	audio_info = audio.info
	length = int(audio_info.length)
	return length

def display_song(msg):
	mesg = font1.render(msg, True, text_color)
	mesg_rect = mesg.get_rect(center=(dis_width/2, dis_height/2))
	dis.blit(mesg, mesg_rect)

def display_time(time):
	seconds = int(time%60)
	minutes = int(time/60)
	if seconds < 10:
		text = str(minutes) + ':0' + str(seconds)
	else:
		text = str(minutes) + ':' + str(seconds)
	timer = font2.render(text, True, text_color)
	timer_rect = timer.get_rect(center=(630, dis_height/2 + 150))
	dis.blit(timer, timer_rect)

def display_progress_bar(time, length):
	progress = time/length
	pygame.draw.rect(dis, (0,250,154), pygame.Rect(200, dis_height/2+147, 400, 8))
	pygame.draw.rect(dis, text_color, pygame.Rect(200, dis_height/2+147, 400*progress, 8))

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
			length = song_length(path, song)
			os.system("mpg123 " + path + "'" + song + "'"+ "&")
			song = song[:-4]
			play_song = True
			start_time = pygame.time.get_ticks()
			last_time = -1
		if play_song:
			display_song(song)
			time = int((pygame.time.get_ticks() - start_time)/1000)
			if time != last_time:
				last_time = time
			if time >= length:
				play_song = False
				os.system('pkill mpg123')
		display_time(time)	
		display_progress_bar(time, length)	
		pygame.display.update()

play()
	