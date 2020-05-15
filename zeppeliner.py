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
font2 = pygame.font.SysFont("Courier", 13)
font3 = pygame.font.SysFont(None, 17)

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
	posX = 630
	posY = 372
	if seconds < 10:
		text = str(minutes) + ':0' + str(seconds)
	else:
		text = str(minutes) + ':' + str(seconds)
	timer = font2.render(text, True, text_color)
	timer_rect = timer.get_rect(center=(posX, posY))
	dis.blit(timer, timer_rect)

def display_progress_bar(time, length):
	progress = time/length
	posY = 370
	pygame.draw.rect(dis, (200,200,200), pygame.Rect(dis_width/2-200, posY, 400, 8))
	pygame.draw.rect(dis, text_color, pygame.Rect(dis_width/2-200, posY, 400*progress, 8))

def display_next_button(play_song):
	posX = 720
	posY = 362
	button_width = 80
	button_height = 22
	color1 = (100, 100, 100)
	color2 = (200, 200, 200)

	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if posX+button_width/2>mouse[0]>posX-button_width/2 and posY+button_height>mouse[1]>posY:
		pygame.draw.rect(dis, color1, pygame.Rect(posX - button_width/2, posY, button_width, button_height))
		if click[0] == 1:
			play_song = False
			os.system('pkill mpg123')
	else:
		pygame.draw.rect(dis, color2, pygame.Rect(posX - button_width/2, posY, button_width, button_height))

	next = font3.render("Next",True, text_color)
	next_rect = next.get_rect(center=(posX, posY + button_height/2))
	dis.blit(next, next_rect)
	return play_song

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
			os.system("mpg123 -q " + path + "'" + song + "'"+ "&")
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
		play_song = display_next_button(play_song)
		pygame.display.update()

play()
	