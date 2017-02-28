########
bl_info = {
	"name": "Agario Addon",
	"category": "Object",
	"version": (1, 0, 0),
	"blender": (2, 75, 0),
	"location": "3D window n-tab",
	"description": "Internal addon for making the agario animations",
	"warning": "",
	"wiki_url": "",
	"author": "Patrick W. Crawford <support@theduckcow.com>",
	"tracker_url":""
}

#verbose
v = True

import bpy


class selectCamCont(bpy.types.Operator):
	"""Select the Camera controller"""
	bl_idname = "object.select_camcont"
	bl_label = "select Camera controller"

	def execute(self,context):
		
		if not "CAM" in bpy.data.objects:
			self.report({'ERROR'}, "Missing object CAM")
			return {'CANCELLED'}
		ob = bpy.data.objects["CAM"]
		bpy.ops.object.select_all(action='DESELECT')
		ob.select = True
		bpy.context.scene.objects.active = ob
		return {'FINISHED'}

#######
# add properties and drivers to the thing
class addCurves(bpy.types.Operator):
	"""Add curvature to selected objects"""
	bl_idname = "object.addcurvature"
	bl_label = "Add curvature and drivers to objects"

	def execute(self,context):
		active = bpy.context.scene.objects.active
		for ob in context.selected_objects:
			bpy.context.scene.objects.active = ob

			preConts = len(ob.modifiers)  # starting number of constraints
			if ob.type != 'MESH' or ("CURVE1" in ob.modifiers and "CURVE2" in ob.modifiers) or ob == bpy.data.objects["CAM.CONT"]:
				continue # already set it up for this one, or it's the controller which shouldn't get it!

			bpy.ops.object.modifier_add(type='CURVE')
			bpy.ops.object.modifier_add(type='CURVE')
			ob.modifiers[preConts].name = "CURVE1"
			ob.modifiers[preConts+1].name = "CURVE2"
			ob.modifiers[preConts].object = bpy.data.objects["CURVE1"]
			ob.modifiers[preConts+1].object = bpy.data.objects["CURVE2"]

			d1 = ob.modifiers[preConts].driver_add("show_viewport").driver
			d2 = ob.modifiers[preConts+1].driver_add("show_viewport").driver
			d1.type = 'SUM'
			d2.type = 'SUM'
			varL_dist = d1.variables.new()
			varL_dist.type = 'SINGLE_PROP'
			varL_dist.name = "reference"
			varL_dist.targets[0].id = bpy.data.objects["CAM"]
			varL_dist.targets[0].data_path = "[\"CURVE_ON\"]"

			varL_dist = d2.variables.new()
			varL_dist.type = 'SINGLE_PROP'
			varL_dist.name = "reference"
			varL_dist.targets[0].id = bpy.data.objects["CAM"]
			varL_dist.targets[0].data_path = "[\"CURVE_ON\"]"

		bpy.context.scene.objects.active = active
		bpy.context.scene.frame_current += 1 # necessary to refresh the scene
		bpy.context.scene.frame_current -= 1
		return {'FINISHED'}


#######
# 
class toggleCurvature(bpy.types.Operator):
	"""Toggle the world curvature to/from being flat"""
	bl_idname = "object.togglecurvature"
	bl_label = "Toggle curvature"

	def execute(self,context):
		
		try:
			ob = bpy.data.objects["CAM"]
			if ob["CURVE_ON"] == 1:
				ob["CURVE_ON"] = 0
			else:
				ob["CURVE_ON"] = 1
			#bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
			bpy.context.scene.frame_current += 1
			#bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
			bpy.context.scene.frame_current -= 1
		except:
			self.report({'ERROR'}, "Missing object CAM with property CURVE_ON")
			return {'CANCELLED'}
		return {'FINISHED'}

#######
# Panel for the UI
class agarioPanel(bpy.types.Panel):
	"""Agario panel"""
	bl_label = "Agario tools"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	# bl_space_type = 'VIEW_3D'
	# bl_region_type = 'TOOLS'
	# bl_context = "objectmode"
	# bl_category = "Tools"
	
	#bl_label = "Minecraft's Properties"

	def draw(self, context):
		layout = self.layout
		scene = context.scene
		row = layout.column(align=True)
		#row.label("Tools")
		
		#row = layout.row()
		row.operator("object.select_camcont",text="select CAM",icon="SCENE")
		if "CAM" in bpy.data.objects:
			#row = layout.row()
			if bpy.data.objects["CAM"]["CURVE_ON"]==1:
				row.operator("object.togglecurvature",text="Toggle to Flat",icon="MATPLANE")
			else:
				row.operator("object.togglecurvature",text="Toggle to Curve",icon="WORLD")
			#row = layout.row()
			row.operator("object.addcurvature",text="Add Curve to Objs",icon="OUTLINER_OB_CURVE")
			#row.prop(bpy.data.objects["playerHeight"].location,"z")
		else:
			row.label("Scene not setup for Agar.io animation")


def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()
