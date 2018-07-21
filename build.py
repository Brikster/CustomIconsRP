from PIL import Image
import shutil
import os

def set_cell(image: str, id: int, paste: str, big_page: bool):
	source_image = Image.open(image)
	paste_image = Image.open(paste)
	
	cell_size = 32 if big_page else 16
	x = (id - 1) % cell_size
	y = (id - 1) // cell_size
	
	source_image.paste(paste_image, (cell_size * x, cell_size * y))
	source_image.save(image)
	
def get_cell(image: str, id: int, big_page: bool):
	source_image = Image.open(image)
	
	cell_size = 32 if big_page else 16
	x = cell_size * ((id - 1) % cell_size)
	y = cell_size * ((id - 1) // cell_size)
	
	return source_image.crop((x, y, x + cell_size, y + cell_size))

#
# Build script of Ilya Andreev
#
print('*** Build script for custom icons resource-pack ***')	
	
if not os.path.exists('temp'):
	os.makedirs('temp/assets/minecraft/textures/font')

dir_src = ('files/pages/')
dir_dst = ('temp/assets/minecraft/textures/font/')

print('Copying pages to temp directory...')
for filename in os.listdir(dir_src):
    shutil.copyfile(dir_src + filename, dir_dst + filename)

for i in range(0, 10):
	print('Generating page ' + i + '...')
	for k in range(0, 256):	
		set_cell('temp/assets/minecraft/textures/font/unicode_page_9{page}.png'.format(page=i),
		k + 1, 'files/images/{page}/{icon}.png'
		.format(
			icon = k,
			page = i
		), i >= 7)
		
print('Generation completed!')	

print('Copying files to temp directory...')
shutil.copyfile('files/pack.mcmeta', 'temp/pack.mcmeta')
shutil.copyfile('files/copyright.txt', 'temp/assets/minecraft/textures/font/copyright.txt')

print('Building zip-file...')	
if not os.path.exists('target'):
	mkdir('target')

shutil.make_archive('target/pack', root_dir='./temp', format='zip')

shutil.rmtree('temp')

print('BUILD SUCCESSFUL.')
