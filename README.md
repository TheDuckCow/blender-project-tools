# Blender Project Tools

Code & tools made to assist with various niche Moo-Ack! Productions projects

Note: these scripts are very niche and likely not terribly useful outside the scope of the respective productions, but descriptions for useful tools will be placed below as appropriate. Some tools are modified. Some scripts or dependenceis have varying license so there is officially no overall license for this repository.


### MC_animations/SEQ_render_handler.py

This is used to fix an issue where rendering from the video sequence editor and having other scene strips with changing cameras and using blender internal + nodes for defocusing. Essentially, the Z-depth path is set from the start of the render so even if the strip's active camera changes, while the view will change, the z-depth data remains as if the first camera were still active. This script gets around this by creating linked copies of the scene for each camera found in sequencer strips, intended to run only at the time of render (on command line or once in the UI) to resolve such Z-depth issues.


### 360-Videos-Metadata

Source code git no longer available, this is used to add the meta data for 360 videos