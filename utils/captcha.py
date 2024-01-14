from PIL import Image, ImageDraw, ImageFilter
import random, os, io, base64, numpy as np

icon_size = 48 # РАЗМЕР ИЗОБРАЖЕНИЙ
icon_spacing = 8 # РАССТОЯНИЕ МЕЖДУ ИКОНКАМИ
margin = 12 # ОШИБКА ПРИ ВЫБОРЕ ИЗОБРАЖЕНИЯ

# ПОЛУЧЕНИЕ ВСЕХ ИЗОБРАЖЕНИЙ ИЗ ПАПКИ /png
images_list = os.listdir('png')
images_list = [file for file in images_list if file.endswith('.png')]

def get_random_images(length: int):
	if len(images_list) < length:
		return 'error: incorrect length'

	return random.sample(images_list, length)

def apply_random_color(img):
	random_red = np.random.randint(256)
	random_green = np.random.randint(256)
	random_blue = np.random.randint(256)

	img = img.convert('RGBA')

	data = img.load()

	for y in range(img.size[1]):
		for x in range(img.size[0]):
			alpha = data[x, y][3]
			if alpha:
				data[x, y] = (random_red, random_green, random_blue, alpha)

	return img

def gen_gradient_bg(width, height):
	image = Image.new('RGB', (width, height))
	draw = ImageDraw.Draw(image)

	colors = [
		(np.random.randint(256), np.random.randint(256), np.random.randint(256))
		for _ in range(2, 7)
	]

	for i, color in enumerate(colors):
		start_y = int(i*(height/(len(colors))))
		end_y = int((i+1)*(height/len(colors)))
		draw.rectangle([(0, start_y), (width, end_y)], fill=color)

	image = image.filter(ImageFilter.GaussianBlur(radius=np.random.randint(5, 15)))

	draw = ImageDraw.Draw(image)

	'''for _ in range(np.random.randint(5, 10)):
		length = np.random.randint(50, 200)
		angle = np.random.randint(0, 360)
		x = np.random.randint(0, width)
		y = np.random.randint(0, height)
		draw.line(
			[(x, y), (x+int(length*np.cos(np.radians(angle))), y+int(length*np.sin(np.radians(angle))))],
			fill = (np.random.randint(256), np.random.randint(256), np.random.randint(256)),
			width = np.random.randint(2, 24)
		)'''
	
	# Генерация точек в рандомных местах с рандомным цветом
	for _ in range(np.random.randint(10, 60)):
		x = np.random.randint(0, width)
		y = np.random.randint(0, height)
		color = (np.random.randint(256), np.random.randint(256), np.random.randint(256))
		draw.point((x, y), fill=color)

	for _ in range(np.random.randint(0, 5)):
		x_start = np.random.randint(0, width)
		x_end = np.random.randint(0, width)
		y_start = np.random.randint(0, height)
		y_end = np.random.randint(0, height)
		color = (np.random.randint(256), np.random.randint(256), np.random.randint(256))
		draw.line([(x_start, x_end), (y_start, y_end)], fill=color, width=np.random.randint(1, 3))

	return image

async def gen_captcha_img():
	bg = gen_gradient_bg(400, 200)
	bg_w, bg_h = bg.size

	icon_locations = []

	random_count = random.randrange(3, 6)

	indexes = get_random_images(random_count)

	for idx, el in enumerate(indexes):
		icon = Image.open(f'./png/{el}', 'r')

		offset_w = random.randint(24, bg_w - icon_size - 24)
		offset_h = random.randint(24, bg_h - icon_size - 24)
		rotation_angle = random.randint(0, 360)

		# ПРОВЕРКА НА ПЕРЕКРЫТИЕ УЖЕ ДОБАВЛЕННЫХ ИКОНОК
		for icon_location in icon_locations:
			location = icon_location['location']
			if (
			offset_w < location[0] + icon_spacing + icon_size
			and offset_w + icon_size + icon_spacing > location[0] - icon_spacing
			and offset_h < location[1] + icon_spacing + icon_size
			and offset_h + icon_size + icon_spacing > location[1] - icon_spacing
			):
				offset_w = random.randint(24, bg_w - icon_size - 24)
				offset_h = random.randint(24, bg_h - icon_size - 24)

		icon = icon.rotate(rotation_angle, resample=Image.BICUBIC)
		bg.paste(apply_random_color(icon), (offset_w, offset_h), icon)

		icon_data = {
			'icon_num': idx,
			'icon_name': el,
			'x': (offset_w - margin, offset_w + icon_size + margin),
			'y': (offset_h - margin, offset_h + icon_size + margin),
			'location': (offset_w, offset_h)
		}

		icon_locations.append(icon_data)

	image_bytes = io.BytesIO()
	bg.save(image_bytes, format='PNG')
	image_b64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')

	icons_b64 = []

	for el in indexes:
		with open(f'./png/{el}', 'rb') as image_file:
			image = image_file.read()
			icons_b64.append(base64.b64encode(image).decode('utf-8'))

	return image_b64, icon_locations, icons_b64

#print(get_random_images(4))
#location = gen_captcha_img()
#print(location)