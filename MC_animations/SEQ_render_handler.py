# MOO-ACK! PRODUCTIONS RENDER SEQUENCE CODE
# Intended for command-line rendering primarily.

import bpy
from bpy.app.handlers import persistent


# -----------------------------------------------------------------------------
# Notes/comments
# -----------------------------------------------------------------------------
"""
Original purpose of this file is to run with anything rendering with more
than one camera angle. Problem is with changing cameras, the Z-depth data
does not update in the sequencer properly. Hoping to make this tool force
update the camera, found that even updating in render and refreshign doesn't
seem to flush out the udpate source of the z-data.

What if instead, we have a FULL linked copy generated/created on render,
and it does that for each CAMERA type? then no need to have any hanlder,
it should just be the right data (right?)

^^ this works. is making a linked scene hard/slow? no - it's near instant!
And I just proved that the above DOES work, setting new scenes.

so! For each camera, create a Scene.Cam.X scene which is the same as
bpy.ops.scene.new(type="LINK_OBJECT_DATA") (or LINK_OBJECTS?).
Just set each active scene first.. and then immedaite scene.name=newName.

"""

# -----------------------------------------------------------------------------
# Global vars
# -----------------------------------------------------------------------------

warned_once = False
verbose = True


# -----------------------------------------------------------------------------
# Hanlder & registration
# -----------------------------------------------------------------------------

def main(context):

	# argument inputs??
	# remove_dup_linked_scenes(context)  for past VSE results

	run_once(context)


	# If a handler is needed, add it
	no_handler = True
	if no_handler:return
	try:
		bpy.app.handlers.frame_change_pre.clear() # well this is aggresive
		# bpy.app.handlers.frame_change_pre.remove(frame_handler)
	except:
		pass
	bpy.app.handlers.frame_change_pre.append(frame_handler)


#@persistent not needed, only per-file handler
def frame_handler(scene):
	
	# settings
	set_resolution = True
	set_camera = True	

	# fix camera & resolution
	if True:update_camera(scene, set_resolution, set_camera)


def run_once(context):

	# set the scene:
	if "SEQ".lower() not in context.scene.name.lower():
		scns = bpy.data.scenes
		for sn in scns:
			if "SEQ".lower() in sn: bpy.context.screen.scene=sn
	if verbose:print(context.scene.name)

	# now go through and create scenes for each strip based on active camera
	# active_seq = None

	cams = []
	initial_scene = context.scene # .name?

	# get the top-most non-hidden sequence layer
	initial_scenes = list(bpy.data.scenes)
	for seq in context.scene.sequence_editor.sequences:
		# if seq.frame_final_start > scene.frame_current: continue
		# if seq.frame_final_end <= scene.frame_current: continue
		if seq.type != 'SCENE': continue
		if seq.mute == True: continue


		# resolution matching
		# set the render resolutions to match
		if True:
			seq.scene.render.resolution_x = context.scene.render.resolution_x
			seq.scene.render.resolution_y = context.scene.render.resolution_y
			seq.scene.render.resolution_percentage = context.scene.render.resolution_percentage

		# now do scene duplciation if appropraite
		if seq.scene_camera not in cams:
			cams.append(seq.scene_camera)
			context.screen.scene=bpy.data.scenes[seq.scene.name]
			# set the active camera FIRST
			context.scene.camera = seq.scene_camera

			bpy.ops.scene.new(type="LINK_OBJECT_DATA")
			new_scn = context.scene
			for new_scn in bpy.data.scenes:
				if new_scn not in initial_scenes:
					initial_scenes.append(new_scn)
					break
			if new_scn == context.scene: # originally: if new_scn == context.scene:
				new_scn.name = seq.scene.name+"."+seq.scene_camera.name
				
				# switch abck to original scene
				context.screen.scene=bpy.data.scenes[initial_scene.name]
				seq.scene = new_scn
			else:
				print("We didn't actually get the newly created scene?")

				context.screen.scene=bpy.data.scenes[initial_scene.name]

			





# -----------------------------------------------------------------------------
# Hanlder & registration
# -----------------------------------------------------------------------------


# outdated code, for reference back only
def update_camera_old(scene, set_resolution, set_camera):
	global verbose, warned_once

	# automatically switch to the sequencer mode?
	print("frame:{y}, scene: {x}".format(x=scene.name,y=scene.frame_current))
	if "SEQ".lower() not in scene.name.lower():
		#if warned_once==False:
		print("*** WARNING: NOT RENDERING IN SEQUENCE MODE ***")
		warned_once = True
		return
	else:
		pass

	if verbose:print("Running frame "+str(scene.frame_current))

	active_seq = None

	# get the top-most non-hidden sequence layer
	for seq in scene.sequence_editor.sequences:
		if seq.frame_final_start > scene.frame_current: continue
		if seq.frame_final_end <= scene.frame_current: continue
		if seq.type != 'SCENE': continue
		if seq.mute == True: continue

		if active_seq == None:
			active_seq = seq
		elif active_seq.channel < seq.channel:
			active_seq = seq

	print("    active sequence: "+str(active_seq))
	if active_seq==None:return

	# now compare / update the camera accordingly
	if set_camera==True:
		print("    1:{x},{y}".format(x=active_seq.scene_camera.name,y=active_seq.scene.camera.name))
		if active_seq.scene_camera != active_seq.scene.camera:
			active_seq.scene.camera = active_seq.scene_camera
		print("    2:{x},{y}".format(x=active_seq.scene_camera.name,y=active_seq.scene.camera.name))

	# set the render resolutions to match
	if set_resolution==True:
		active_seq.scene.render.resolution_x = scene.render.resolution_x
		active_seq.scene.render.resolution_y = scene.render.resolution_y
		active_seq.scene.render.resolution_percentage = scene.render.resolution_percentage

	# update things?
	active_seq.scene.update()
	scene.update()


# -----------------------------------------------------------------------------
# Run the main code
# -----------------------------------------------------------------------------


main(bpy.context)


