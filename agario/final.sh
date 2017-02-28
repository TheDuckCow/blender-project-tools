#!/bin/bash
# render to a video container
cd RENDER/360-Videos-Metadata
# add the metadata
python 360VideosMetadata.py -i /Users/patrickcrawford/Insync/Business/Agar-io-first-person-360/Previz/agario-render-0001-1283.mp4  ../../Previz/agario-previz.mp4
cd ../../