#!/bin/bash
# render preview first

/Applications/Blender-2.75/blender.app/Contents/MacOS/blender -b ANIMATION/scene_10.blend -a


# render to a video container
/Applications/Blender-2.75/blender.app/Contents/MacOS/blender -b RENDER/render-video-youtube.blend -a
cd RENDER/360-Videos-Metadata
# add the metadata
python 360VideosMetadata.py -i ../agario-render-0001-1140.mp4 ../../Previz/agario-previz.mp4
cd ../../