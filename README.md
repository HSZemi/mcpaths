mcpaths
=======

mcpaths draws a map of the minecraft nether

Introduction
------------

mcpaths's purpose is to draw a 2D map of the nether dimension of a minecraft map.

It takes into account nether fortresses (e.g. nether bricks), railroad systems (e.g. rail blocks),
stone blocks (cobblestone, stone and stone bricks with their respective slabs and stairs) as well as 
portals (e.g. Obsidian).

There is no algorithm implemented to check whether a block of a certain type is in fact connected to,
for instance, an active portal or a path.


Setup
-----
Initialize mcpaths by executing initialize.sh once:
```./initialize.sh```

This will just execute the following command:
```git clone https://github.com/mcedit/pymclevel.git```

pymclevel is required for the coordinate extraction. You won't be able to run getcoordinates.py 
without pymclevel.


Usage
-----
First call getcoordinates.py on a level.dat file in order to extract the coordinates of the relevant blocks:
```./getcoordinates.py path/to/minecraft/world/level.dat```

This will generate a bunch of files in your mcpaths directory:
  * fortresses.txt
  * portals.txt
  * rails.txt
  * stones.txt

Second, call makemap.py in order to create the svg map in the output directory:
```./makemap.py```

The map will be generated as map.svg in the output directory and can be viewed with any svg viewer or in
the html page provided.