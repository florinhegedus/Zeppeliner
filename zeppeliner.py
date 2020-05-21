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
song_color = (253, 254, 255)
bg_color = (255, 255, 255)
font1 = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont("Courier", 13)
font3 = pygame.font.SysFont(None, 17)

color1 = (100, 100, 100)
color2 = (200, 200, 200)
COLOR_INACTIVE = (37, 38, 39)
COLOR_ACTIVE = (100, 100, 100)
FONT = pygame.font.Font(None, 17)

path = '/home/florin/Music/'
songs = [f for f in listdir(path) if isfile(join(path, f))]

class InputBox:

	def __init__(self, x, y, w, h, text=''):
		self.rect = pygame.Rect(x, y, w, h)
		self.color = COLOR_INACTIVE
		self.text = text
		self.txt_surface = FONT.render(text, True, text_color)
		self.active = False

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			#If the user clicked on the input_box rect
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False
			self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
		if event.type == pygame.KEYDOWN:
			if self.active:
				if event.key == pygame.K_RETURN:
					print (self.text)
				elif event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode
				self.txt_surface = FONT.render(self.text, True, text_color)

	def update(self):
		width = max(200, self.txt_surface.get_width() + 10)
		self.rect.w = width

	def draw(self, screen):
		screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 6))
		pygame.draw.rect(screen, self.color, self.rect, 2)

	def clear(self):
		self.text = ''
		self.txt_surface = FONT.render(self.text, True, text_color)


def song_length(path, song):
	audio = MP3(path + song)
	audio_info = audio.info
	length = int(audio_info.length)
	return length

def display_song(msg):
	mesg = font1.render(msg, True, song_color)
	mesg_rect = mesg.get_rect(center=(540, dis_height/2))
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
	pygame.draw.rect(dis, color2, pygame.Rect(dis_width/2-200, posY, 400, 8))
	pygame.draw.rect(dis, text_color, pygame.Rect(dis_width/2-200, posY, 400*progress, 8))

def display_next_button(play_song):
	posX = 720
	posY = 362
	button_width = 80
	button_height = 22

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

def display_albums(y1, y2, n1, n2):
	path = '/home/florin/Programs/Python/Zeppeliner/images/'
	images = [f for f in listdir(path) if isfile(join(path, f))]

	n1 = n1 % len(images)
	n2 = n2 % len(images)

	img1 = pygame.image.load(path + images[n1])
	img1 = pygame.transform.scale(img1, (260, 260))
	img2 = pygame.image.load(path + images[n2])
	img2 = pygame.transform.scale(img2, (260, 260))
	
	dis.blit(img1, (20, y1))
	dis.blit(img2, (20, y2))

	pygame.draw.rect(dis, bg_color, pygame.Rect(0, 0, 400, 54))
	pygame.draw.rect(dis, bg_color, pygame.Rect(0, 346, 400, 54))


def display_song_bg():
	pygame.draw.rect(dis, (10, 12, 14), pygame.Rect(0, 54, 800, 292))

def play():
	play = True
	play_song = False
	y1 = 64
	y2 = y1 + 276
	n1 = 0
	n2 = 1
	input_box1 = InputBox(580, 15, 60, 22)
	while play:
		dis.fill(bg_color)
		display_song_bg()
		display_albums(y1, y2, n1, n2)
		y1 -= 1
		y2 -= 1
		if y1 + 260 < 54:
			y1 += 260 + 292
			n1 += 2
		if y2 + 260 < 54:
			y2 += 260 + 292
			n2 += 2
		for event in pygame.event.get():
			input_box1.handle_event(event)
			if event.type==pygame.QUIT:
					play = False
					os.system('pkill mpg123')
			if input_box1.active == True:
				if event.type==pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						#change the song to the user input
						found = False
						for sng in songs:
							if input_box1.text.lower() in sng.lower():
								song = sng
								found = True
								break
						if found:
							os.system('pkill mpg123')
							input_box1.clear()
							length = song_length(path, song)
							if song.find("'") > -1:
								song_p = song[:song.find("'")] + "'\\'" + song[song.find("'"):]
							else:
								song_p = song
							os.system("mpg123 -q " + path + "'" + song_p + "'"+ "&")
							play_song = True
							song = song[:-4]
							start_time = pygame.time.get_ticks()
							last_time = -1
				
			if input_box1.active == False:
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
			if song.find("'") > -1:
				song_p = song[:song.find("'")] + "'\\'" + song[song.find("'"):]
			else:
				song_p = song
			os.system("mpg123 -q " + path + "'" + song_p + "'"+ "&")
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

		input_box1.update()
		input_box1.draw(dis)
		display_time(time)	
		display_progress_bar(time, length)	
		play_song = display_next_button(play_song)
		pygame.display.update()

play()
	