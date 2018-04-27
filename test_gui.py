
#############################################
## Generate data
#############################################
from random import random, seed
from math import cos, sin, floor, sqrt, pi, ceil
import numpy as np
import time
seed(time.time())

def emoji_svg_file(emoji_filename):
	return 'emoji/'+emoji_filename+'.svg'

def emoji_png_file(emoji_filename):
	return 'png/'+emoji_filename+'.png'

def download_emoji_svg(emoji_filename):
	from urllib import request
	emoji_path = 'emoji/'+emoji_filename+'.svg'
	f = open(emoji_path, 'wb')
	f.write(request.urlopen('https://gitcdn.xyz/repo/googlei18n/noto-emoji/v2018-01-02-flag-update/svg/'+emoji_filename+'.svg').read())
	f.close()
	print('Downloaded: ' + emoji_filename)
	
def download_all_emoji(emoji_set):
	for key in emoji_set.keys():
		download_emoji_svg(emoji_set[key])
	
def convert_svg_to_png(emoji_set):
	import os
	for key in emoji_set.keys():
		filename = emoji_set[key]
	if os.path.isfile('png/'+filename+'.png'):
		return
	os.system('./tools/utilities/magick convert -density 384 -background none emoji/'+filename+'.svg png/'+filename+'.png')
	print('Converted ' + filename)

location = {
		'camping': 'emoji_u1f3d5',
		'beach': 'emoji_u1f3d6',
		'desert': 'emoji_u1f3dc',
		'park': 'emoji_u1f3de',
		'factory': 'emoji_u1f3ed',
		'hills': 'emoji_u1f304',
		'city': 'emoji_u1f307',
		'golf': 'emoji_u26f3',
		'night': 'emoji_u1f306'}

actor = {
		'man_walk': 'emoji_u1f6b6_1f3fe_200d_2642',
		'man_run': 'emoji_u1f3c3_1f3fb_200d_2642',
		'man_sport': 'emoji_u1f3cb_1f3fb_200d_2642',
		'man_police': 'emoji_u1f46e_1f3fd_200d_2642',
		'man_hello': 'emoji_u1f64b_1f3fe_200d_2642',
		'man_engineer': 'emoji_u1f468_1f3fc_200d_1f527',
		'man_turban': 'emoji_u1f473_1f3fe_200d_2642',
		'man_suit': 'emoji_u1f935_1f3fe',
		'man_clown': 'emoji_u1f939_1f3fb_200d_2642',
		'man_construction': 'emoji_u1f477_200d_2642',
		'man_doctor': 'emoji_u1f468_1f3ff_200d_2695',
		'women_bicycle': 'emoji_u1f6b4_1f3fb_200d_2640',
		'women_hijab': 'emoji_u1f9d5_1f3fc',
		'women_doctor': 'emoji_u1f469_1f3fc_200d_2695',
		'animal_camel': 'emoji_u1f42a',
		'animal_cat': 'emoji_u1f408',
		'animal_bird': 'emoji_u1f426',
		'animal_tree': 'emoji_u1f333',
		'animal_car': 'emoji_u1f697',
		'animal_bus': 'emoji_u1f68c'}

danger = {
		'danger1': 'emoji_u1f4a3',
		'danger2': 'emoji_u1f52b',
		'danger3': 'emoji_u1f52a',
		'danger4': 'emoji_u2622'}

def euclidean_distance(a, b):
	dx = a[0] - b[0]
	dy = a[1] - b[1]
	return sqrt(dx * dx + dy * dy)
	
# https://github.com/emulbreh/bridson
def poisson_disc_samples(width, height, r, k=5, distance=euclidean_distance, random=random):
	tau = 2 * pi
	cellsize = r / sqrt(2)

	grid_width = int(ceil(width / cellsize))
	grid_height = int(ceil(height / cellsize))
	grid = [None] * (grid_width * grid_height)

	def grid_coords(p):
		return int(floor(p[0] / cellsize)), int(floor(p[1] / cellsize))

	def fits(p, gx, gy):
		yrange = list(range(max(gy - 2, 0), min(gy + 3, grid_height)))
		for x in range(max(gx - 2, 0), min(gx + 3, grid_width)):
			for y in yrange:
				g = grid[x + y * grid_width]
				if g is None:
					continue
				if distance(p, g) <= r:
					return False
		return True

	p = width * random(), height * random()
	queue = [p]
	grid_x, grid_y = grid_coords(p)
	grid[grid_x + grid_y * grid_width] = p

	while queue:
		qi = int(random() * len(queue))
		qx, qy = queue[qi]
		queue[qi] = queue[-1]
		queue.pop()
		for _ in range(k):
			alpha = tau * random()
			d = r * sqrt(3 * random() + 1)
			px = qx + d * cos(alpha)
			py = qy + d * sin(alpha)
			if not (0 <= px < width and 0 <= py < height):
				continue
			p = (px, py)
			grid_x, grid_y = grid_coords(p)
			if not fits(p, grid_x, grid_y):
				continue
			queue.append(p)
			grid[grid_x + grid_y * grid_width] = p
	return [p for p in grid if p is not None]
	# Draw a gradient
def interpolate_color(minval, maxval, val, color_palette):
	max_index = len(color_palette)-1
	v = float(val-minval) / float(maxval-minval) * max_index
	i1, i2 = int(v), min(int(v)+1, max_index)
	(r1, g1, b1), (r2, g2, b2) = color_palette[i1], color_palette[i2]
	f = v - i1
	return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

def draw_vt_gradient(draw, rect, color_func, color_palette):
	(max_x, max_y) = rect
	minval, maxval = 1, len(color_palette)
	delta = maxval - minval
	for y in range(0, max_y+1):
		f = y / float(max_y)
	val = minval + f * delta
	color = color_func(minval, maxval, val, color_palette)
	draw.line([(0, y), (max_x, y)], fill=color)

# Create a sky graident image
def create_sky_gradient_image(size):
	from PIL import Image, ImageDraw
	BLUE, WHITE, WHITE = ((28, 146, 210), (255, 255, 255), (255, 255, 255))
	image = Image.new("RGB", size)
	draw = ImageDraw.Draw(image)
	draw_vt_gradient(draw, size, interpolate_color, [BLUE, WHITE, WHITE])
	return image

# Generate random locations filled with random actors
def generate_random_location(locations, actors, dangers, count, s = 256):
	import time
	t = time.time()

	from PIL import Image, ImageDraw, ImageFont
	import random		

	# Cache backgrounds
	cached_locations = []
	for key in locations.keys():
		bg = Image.open(emoji_png_file(locations[key]))
	cached_locations.append(bg)
	cached_locations.append(bg.transpose(Image.FLIP_LEFT_RIGHT))

	# Generate a background
	backgrounds = []
	for i in range(count):
		margin = int(s*0.1)
	location_img = cached_locations[random.randint(0, len(cached_locations)-1)]
	location_img = location_img.resize((s+margin,s+margin), Image.BILINEAR)
	img = create_sky_gradient_image((s,s))
	img.paste(location_img,(int(-margin/2),int(-margin/2)),location_img)
	
	backgrounds.append(img)
	
	# Cache actors
	cached_actors = []
	actor_size = int(s * 0.2)
	for key in actors.keys():
		fg = Image.open(emoji_png_file(actors[key])).resize((actor_size,actor_size), Image.BILINEAR)
		cached_actors.append(fg)
		#cached_actors.append(fg.transpose(Image.FLIP_LEFT_RIGHT))
	
	# Generate some nice random sampling coordinates
	samples = []
	for i in range(10):
		samples.append(poisson_disc_samples(s,s,int(s * 0.1)))
	
	# Add actors to the backgrounds
	imgs = []
	for bg in backgrounds:
		positions = samples[random.randint(0, len(samples)-1)]
	for p in positions:
		if p[1] < s * 0.4: continue
		actor_img = cached_actors[random.randint(0, len(cached_actors)-1)]
		bg.paste(actor_img, (int(p[0]-actor_size/2),int(p[1]-actor_size/2)), actor_img)
		imgs.append(bg)
	
	# Load and cache dangerous items
	cached_danger = []
	danger_size = int(actor_size*0.75)
	for key in dangers:
		d = Image.open(emoji_png_file(dangers[key])).resize((danger_size,danger_size), Image.BILINEAR)
		cached_danger.append(d)
	
	# Add a dangerous item
	masks = []
	for img in imgs:
		# Get a random location in the bottom half of the screen
		positions = samples[random.randint(0, len(samples)-1)]
		good_positions = []
		for p in positions:
			if p[1] > s * 0.4:
				good_positions.append(p)
		if len(good_positions) == 0: good_positions = positions
		p = good_positions[random.randint(0, len(good_positions)-1)]
		item = cached_danger[random.randint(0, len(cached_danger)-1)]
		
	img.paste(item, (int(p[0]-danger_size/2),int(p[1]-danger_size/2)), item)
	
	# Simulate CCTV footage by drawing some text
	d = ImageDraw.Draw(img)
	d.text((10,10), time.strftime("%Y-%m-%d %H:%M"), fill=(255,255,255,128))
	d.text((s-65,10), time.strftime("Camera 07"), fill=(255,255,255,128))
	
	
	mask = Image.new("L", (s,s))
	mask.paste((255), (int(p[0]-danger_size/2),int(p[1]-danger_size/2)), item)
	masks.append(mask)
	
	elapsed = time.time() - t
	print("("+str(len(imgs))+") Scenes created in (" + str(round(elapsed,3)) + " s).")

	return imgs, masks

def show_image(img, is_greyscale=False):
	import cv2
	img = np.array(img).copy()
	if not is_greyscale: img = img[:, :, ::-1]
	cv2.imshow('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

#############################################
## Load trained model
#############################################
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import numpy as np
from PIL import Image
import os, sys

if not os.path.isfile('model.h5'):
	model_url = 'https://s3-eu-west-1.amazonaws.com/deepemoji/Graphs/model.h5'
	# load trained model
	from urllib import request

	f = open('model.h5', 'wb')
	f.write(request.urlopen(model_url).read())
	f.close()
	print('Model downloaded from ['+model_url+']')

#loaded_model = load_model('model.h5')
#loaded_model.summary()
#############################################


#############################################
## GUI
#############################################

# GUI using Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QFrame, QPushButton, QFileDialog, QListWidget, QListWidgetItem, QDoubleSpinBox, QCheckBox
from PyQt5.QtGui import QPainter, QPixmap, QImage, QPen
from PyQt5.QtCore import Qt, QPoint, QTimer, QThread

class View(QWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.setMouseTracking(True)		
		self.x = 0
		self.y = 0
		self.prevX = 0
		self.prevY = 0
		
		self.viewSize = 512
		self.brushSize = 3
		self.isSmoothDrawing = True

		self.buffer = QImage(self.viewSize, self.viewSize, QImage.Format_ARGB32)		
		self.buffer.fill(Qt.white)
		self.undoBuffer = self.buffer.copy()
		self.guide = self.buffer.copy()
		
		self.setMinimumSize(self.viewSize,self.viewSize)
		self.setMaximumSize(self.viewSize,self.viewSize)
		
	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		
		qp.setOpacity(1.0)
		qp.drawImage(0,0,self.buffer)

class Widget(QWidget):	
	def __init__(self):
		super().__init__()		
		self.initUI()
		
	def initUI(self):			
		grid = QGridLayout()
		grid.setSpacing(10)

		# Add left view
		view1 = View(self)
		grid.addWidget(view1, 1, 0)
		self.view1 = view1
		
		# Add right view
		view2 = View(self)
		grid.addWidget(view2, 1, 1)		
		self.view2 = view2

		# Generate background button
		genSceneButton = QPushButton('Generate Scene...', self)
		genSceneButton.clicked.connect(self.genSceneButtonClicked)   
		grid.addWidget(genSceneButton, 3, 1)

		self.setWindowTitle('EmojiNet')
		self.setMouseTracking(True)	
		self.setLayout(grid)	

	def genSceneButtonClicked(self):
		global location, actor, danger
		imgs, mask = generate_random_location(location, actor, danger, 1, 512)

		from PIL.ImageQt import ImageQt
		self.view1.buffer = ImageQt(imgs[0])

app = QApplication(sys.argv)
w = Widget()
w.show()
app.exec_()