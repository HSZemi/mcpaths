#! /usr/bin/env python

from pymclevel import mclevel
from pymclevel import MCAlphaDimension
from pymclevel import alphaMaterials
import numpy as np
import sys

if(len(sys.argv) != 2):
	print("Usage: {0} worldfile.dat".format(sys.argv[0]))
	sys.exit(1)
else:
	worldfile = sys.argv[1]

level = mclevel.fromFile(worldfile)

nether = MCAlphaDimension(level, -1)

chunkPositions = list(nether.allChunks)

print "Examining", len(chunkPositions), "chunks."

#sys.exit(0)

fortressfile = "fortresses.txt"
stonefile = "stones.txt"
railfile = "rails.txt"
portalfile = "portals.txt"

fortresshandle = open(fortressfile, 'w')
stonehandle = open(stonefile, 'w')
railhandle = open(railfile, 'w')
portalhandle = open(portalfile, 'w')

chunkcoordinates = np.zeros((16,16,256,3))



for x in range(16):
		for z in range(16):
			for y in range(256):
				chunkcoordinates[x][z][y] = (x,z,y)


for xPos,zPos in chunkPositions:
	chunk = nether.getChunk(xPos, zPos)
	xCoord = xPos * 16
	zCoord = zPos * 16
	
	fortressblocks = (chunk.Blocks == alphaMaterials.NetherBrick.ID)
	
	stoneblocks  = (chunk.Blocks == alphaMaterials.Cobblestone.ID)
	stoneblocks |= (chunk.Blocks == alphaMaterials.CobblestoneSlab.ID)
	stoneblocks |= (chunk.Blocks == alphaMaterials.DoubleCobblestoneSlab.ID)
	stoneblocks |= (chunk.Blocks == alphaMaterials.StoneStairs.ID)
	stoneblocks |= (chunk.Blocks == alphaMaterials.CobblestoneWall.ID)
	stoneblocks |= (chunk.Blocks == alphaMaterials.Stone.ID)
	stoneblocks |= (chunk.Blocks == alphaMaterials.StoneSlab.ID)
	stoneblocks |= (chunk.Blocks == alphaMaterials.DoubleStoneSlab.ID)
	stoneblocks |= (chunk.Blocks == alphaMaterials.StoneBricks.ID)
	stoneblocks |= (chunk.Blocks == alphaMaterials.StoneBrickSlab.ID)
	stoneblocks |= (chunk.Blocks == alphaMaterials.DoubleStoneBrickSlab.ID)
	stoneblocks |= (chunk.Blocks == alphaMaterials.StoneBrickStairs.ID)
	
	railblocks  = (chunk.Blocks == alphaMaterials.Rail.ID)
	railblocks |= (chunk.Blocks == alphaMaterials.PoweredRail.ID)
	railblocks |= (chunk.Blocks == alphaMaterials.DetectorRail.ID)
	railblocks |= (chunk.Blocks == alphaMaterials.ActivatorRail.ID)
	
	portalblocks  = (chunk.Blocks == alphaMaterials.Obsidian.ID)
	portalblocks |= (chunk.Blocks == alphaMaterials.NetherPortal.ID)

	for (x,z,y) in chunkcoordinates[fortressblocks]:
		fortresshandle.write("{0} {1}\n".format(int(x)+xCoord,int(z)+zCoord))
	for (x,z,y) in chunkcoordinates[stoneblocks]:
		stonehandle.write("{0} {1}\n".format(int(x)+xCoord,int(z)+zCoord))
	for (x,z,y) in chunkcoordinates[railblocks]:
		railhandle.write("{0} {1}\n".format(int(x)+xCoord,int(z)+zCoord))
	for (x,z,y) in chunkcoordinates[portalblocks]:
		portalhandle.write("{0} {1}\n".format(int(x)+xCoord,int(z)+zCoord))

fortresshandle.close()
stonehandle.close()
railhandle.close()
portalhandle.close()
print "Scanning complete."
