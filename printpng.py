#!/usr/bin/python

# printpng.py -- part of png2ptouch
# https://github.com/zakx/png2ptouch
# Copyright (C) 2013 zakx <sg@unkreativ.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

def print_image(printer, image):
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

	image = Image.open(args.image)
	print_image(printer=args.printer, image=image)
