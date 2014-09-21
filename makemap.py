#! /usr/bin/env python3

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import sys, os



backgroundcolor = "#ffffffff"
fortressfile = "fortresses.txt"
stonefile = "stones.txt"
railfile = "rails.txt"
portalfile = "portals.txt"

svg_output = "output/map.svg"

fortresscolor = "#720d0d"
stonecolor = "#4d4d4d"
railcolor = "#f6ff00"
portalcolor = "#161637"


fortresses = []
stones = []
rails = []
portals = []

svgheadtemplate = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="{0}"
   height="{1}"
   id="svg2"
   version="1.1">
   '''
   
svgtailtemplate = '''</svg>'''

svggroupheadtemplate = '''<g
     id="{0}"
     style="display:inline">
'''

svggrouptailtemplate = '''</g>
'''

svgrecttemplate = '''<rect
       style="color:#000000;fill:{0};fill-opacity:1;stroke:none;stroke-width:0.1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
       id="rect{1}"
       width="{4}"
       height="{5}"
       x="{2}"
       y="{3}" />
'''

def readPoints(filename):
	data = []
	f = open(filename, 'r')
	for line in f:
		items = line.split()
		data.append((int(items[0]), int(items[1])))
	f.close()
	return data

def dataToMap(data, width, height):
	mymap = [[False for j in range(height)] for i in range(width)]
	for (x,z) in data:
		x -= min_x
		z -= min_z
		mymap[x][z] = True
	return mymap

def writeRectangles(width, height, a, svgid, mymap, color):

	for (x,z) in ((0,1),(0,-1),(1,0),(-1,0)):
		x -= min_x
		z -= min_z
		svgid += 1
		a.write(svgrecttemplate.format("#0000ff",svgid, x, z, 1, 1))


	for z in range(height):
		for x in range(width):
			if(mymap[x][z]):
				posX = x
				posZ = z
				nextrect = True
				size = 1
				while(nextrect):
					size += 1
					for k in range(x,x+size):
						for l in range(z,z+size):
							nextrect = (nextrect and mymap[k][l])
				rect_w = size - 1
				rect_h = size - 1
				nextrect = True
				while(nextrect):
					rect_w += 1
					for k in range(x,x+rect_w):
						for l in range(z,z+rect_h):
							nextrect = (nextrect and mymap[k][l])
				rect_w -= 1
				nextrect = True
				while(nextrect):
					rect_h += 1
					for k in range(x,x+rect_w):
						for l in range(z,z+rect_h):
							nextrect = (nextrect and mymap[k][l])
				rect_h -= 1
				
				for k in range(x,x+rect_w):
					for l in range(z,z+rect_h):
						mymap[k][l] = False
				
				svgid += 1
				a.write(svgrecttemplate.format(color,svgid, x, z, rect_w, rect_h))
	return svgid

fortresses = readPoints(fortressfile)
stones = readPoints(stonefile)
rails = readPoints(railfile)
portals = readPoints(portalfile)

max_x = 0
max_z = 0
min_x = 0
min_z = 0
padding = 10

for (x,z) in fortresses:
	max_x = max(max_x, x)
	max_z = max(max_z, z)
	min_x = min(min_x, x)
	min_z = min(min_z, z)
for (x,z) in stones:
	max_x = max(max_x, x)
	max_z = max(max_z, z)
	min_x = min(min_x, x)
	min_z = min(min_z, z)
for (x,z) in rails:
	max_x = max(max_x, x)
	max_z = max(max_z, z)
	min_x = min(min_x, x)
	min_z = min(min_z, z)
for (x,z) in portals:
	max_x = max(max_x, x)
	max_z = max(max_z, z)
	min_x = min(min_x, x)
	min_z = min(min_z, z)


print(max_x)
print(max_z)
print(min_x)
print(min_z)

max_x += padding
max_z += padding
min_x -= padding
min_z -= padding

width = max_x - min_x
height = max_z - min_z

fortresses = set(fortresses)
stones = set(stones)
rails = set(rails)
portals = set(portals)


fortressmap = dataToMap(fortresses, width, height)
stonemap = dataToMap(stones, width, height)
railmap = dataToMap(rails, width, height)
portalmap = dataToMap(portals, width, height)


a = open(svg_output, 'w')
svgid = 0

a.write(svgheadtemplate.format(width, height))

a.write(svggroupheadtemplate.format("fortress"))
svgid = writeRectangles(width, height, a, svgid, fortressmap, fortresscolor)
a.write(svggrouptailtemplate)

a.write(svggroupheadtemplate.format("stone"))
svgid = writeRectangles(width, height, a, svgid, stonemap, stonecolor)
a.write(svggrouptailtemplate)


a.write(svggroupheadtemplate.format("rail"))
svgid = writeRectangles(width, height, a, svgid, railmap, railcolor)
a.write(svggrouptailtemplate)


a.write(svggroupheadtemplate.format("portal"))
svgid = writeRectangles(width, height, a, svgid, portalmap, portalcolor)
a.write(svggrouptailtemplate)

a.write(svgtailtemplate)
a.close()

