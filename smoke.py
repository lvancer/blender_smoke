import os
import shutil
import bpy
from random import uniform

        
class SmokeBlender:
    
    def __init__(self, input_folder, output_folder, output_s_folder):
        
        scale = uniform(0.3, 2)
        self.scale = (scale, scale, scale)
        self.density = uniform(0.01, 0.1)
        self.velocity_factor = uniform(1, 100)
        self.velocity_normal = uniform(0, 100)
        self.alpha = uniform(0.1, 0.8)
        self.beta = uniform(0.5, 0.8)
        self.vorticity = uniform(10, 100)
        self.location = (uniform(-1.25, 1.25), uniform(-1.0, 1.0), uniform(4.0, 7.0))

        
        self.input_folder = input_folder
        self.output = output_folder
        self.output_s = output_s_folder
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        if not os.path.exists(self.output_s):
            os.makedirs(self.output_s)
        
    def render(self):
        
        for img_file in os.listdir(self.input_folder):
            
            img = bpy.data.images.load(os.path.join(self.input_folder, img_file))
            width = img.size[0]
            height = img.size[1]
            
            scn = bpy.context.scene
            scn.frame_start=2
            scn.frame_end=2
            scn.render.resolution_x = width
            scn.render.resolution_y = height
            scn.render.resolution_percentage = 100
            self.add_background()
            self.add_smoke()
            self.set_camera()
            bpy.ops.render.render(write_still=True)
            self.random_camera()
            
            filename = img_file
            self.start_render(scn, os.path.join(self.output_s, filename.split('.')[0]+"@#"))
            
            bpy.data.textures["Texture.001"].image=img
            self.start_render(scn, os.path.join(self.output, filename.split('.')[0]+"@#"))
            
            output_filename = filename
                
            shutil.move(os.path.join(self.output, filename.split('.')[0]+"@2.png"), 
                        os.path.join(self.output, output_filename))
            shutil.move(os.path.join(self.output_s, filename.split('.')[0]+"@2.png"), 
                        os.path.join(self.output_s, output_filename))

    def start_render(self, scn, fp):
        scn.render.filepath = fp
        bpy.ops.render.render(animation=True)
    
    def add_smoke(self):
        bpy.ops.object.modifier_add(type='SMOKE')
        bpy.ops.object.material_slot_add()
        bpy.ops.object.quick_smoke()
        bpy.data.objects["Cube"].scale = self.scale
        bpy.data.objects["Cube"].location = (0.0, 0.0, 2.728)
        bpy.data.objects["Cube"].modifiers["Smoke"].flow_settings.smoke_color = (5, 5, 5)
        bpy.data.objects["Cube"].modifiers["Smoke"].flow_settings.density = self.density
        bpy.data.objects["Cube"].modifiers["Smoke"].flow_settings.use_initial_velocity = True
        bpy.data.objects["Cube"].modifiers["Smoke"].flow_settings.velocity_factor = self.velocity_factor
        bpy.data.objects["Cube"].modifiers["Smoke"].flow_settings.velocity_normal = self.velocity_normal
        bpy.data.objects["Cube"].hide_render = True
        bpy.context.object.modifiers["Smoke"].domain_settings.use_adaptive_domain = True
        bpy.context.object.modifiers["Smoke"].domain_settings.use_high_resolution = True
        bpy.context.object.modifiers["Smoke"].domain_settings.alpha = self.alpha
        bpy.context.object.modifiers["Smoke"].domain_settings.beta = self.beta
        bpy.context.object.modifiers["Smoke"].domain_settings.vorticity = self.vorticity
        
    def set_camera(self):
        camera = bpy.data.objects["Camera"]
        camera.location = (0.0, 0.0, 6.0)
        camera.rotation_euler = (0.0, 0.0, 0.0)

    def random_camera(self):
        camera = bpy.data.objects["Camera"]
        camera.location = self.location
        camera.rotation_euler = (0.0, 0.0, 0.0)
        
    def add_background(self):
        # img = bpy.data.images.load(filepath)
        img = bpy.data.images.new("filepath", 1024, 1024)
        
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                space_data = area.spaces.active
                bg = space_data.background_images.new()
                bg.image = img
                space_data.show_background_images = True
                break

        texture = bpy.data.textures.new("Texture.001", 'IMAGE')
        texture.image = img
        bpy.data.worlds['World'].active_texture = texture
        bpy.context.scene.world.texture_slots[0].use_map_horizon = True
        bpy.context.scene.world.use_sky_paper = True
        
        
if __name__ == "__main__":
    render = SmokeBlender("image", "output", "smoke")
    render.render()