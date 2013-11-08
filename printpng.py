#!/usr/bin/python

import argparse
import subprocess
from PIL import Image

INIT_PRINTER = "\x1B@\x1BiS\x1BiR\x01"

def process_image(image):
	image = image.rotate(270)
	image = image.convert('L') # convert to BW
	image.save("tmp.png")
	width, height = image.size
	output = str()

	for y in xrange(height-1, -1, -1):
		# loop backwards through y
		pixels = {}
		for x in xrange(width/8-1, -1, -1):
			# loop through blocks of 8 pixels on x
			pixel_line = str()
			for i in xrange(0, 8):
				if image.getpixel((x*8+i,y)) < 128:
					pixel_line += "1"
				else:
					pixel_line += "0"
			pixels[x] = chr(int(pixel_line, 2))

		if width > 90:
			output += "G%s\x00" % (chr(width/8))
		else:
			# if width is <=90, we'll pad the image
			output += "G%s\x00\x00\x00\x00\x00" % (chr(width/8+4))

		for p in pixels:
			output += pixels[p]
	return output

def linefeed(count=0):
	output = str()
	for i in xrange(0, count):
		output += "Z"
	output += "\x1A"
	return output

def print_image(printer, filename):
	image = Image.open(filename)
	data = process_image(image)

	fd = open("pyimage.txt", "w")
	fd.write(data)
	fd.close()

	lpr =  subprocess.Popen(["/usr/bin/lpr", "-P", printer], \
							stdin=subprocess.PIPE)
	lpr.stdin.write(INIT_PRINTER)
	lpr.stdin.write(data)
	lpr.stdin.write(linefeed(1))
	print "Sent data to printer."

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Print a PNG file on a Brother P-Touch 2430 PC')
	parser.add_argument('-p', '--printer', type=str, help='CUPS name of the printer', required=True)
	parser.add_argument('image', type=str, help='Filename of a PNG image')

	args = parser.parse_args()
	print_image(printer=args.printer, filename=args.image)
