from pyray import *
import random
from math import *
from rayextra import *
import level
from pyray import ffi

    
class Player:
  def __init__(self,x,z):
    self.position = Vector3(x,5,z)
    self.velocity = Vector3(0,0,0)
    self.rotation = Vector2(0,0)
    self.camera = Camera3D(self.position, Vector3(1,0,0), Vector3(0,1,0), 120, CameraProjection.CAMERA_PERSPECTIVE)
    
  def move(self):
    mp = get_mouse_delta()
    player.rotation.x -= mp.x*(dt/60)
    player.rotation.y -= mp.y*(dt/60)
    self.position.x += sin(self.rotation.x) * (self.velocity.x*dt)
    self.position.z += cos(self.rotation.x) * (self.velocity.x*dt)
    
    self.position.x += sin(self.rotation.x + pi/2) * (self.velocity.z*dt)
    self.position.z += cos(self.rotation.x + pi/2) * (self.velocity.z*dt)
    self.rotation.y = degrees(self.rotation.y)
    if self.rotation.y > 89:
      self.rotation.y = 89
    if self.rotation.y < -89:
      self.rotation.y = -89
    self.rotation.y = radians(self.rotation.y)
    
    self.velocity.x *= 0.96
    self.velocity.z *= 0.96
    self.camera.position = self.position
    self.camera.target = vector3_add(self.position,Vector3(sin(self.rotation.x),tan(self.rotation.y),cos(self.rotation.x)))


set_config_flags(FLAG_WINDOW_RESIZABLE+FLAG_VSYNC_HINT)
init_window(800,600,"Khaosphora")

global dt
dt = 0


skyboxtex = load_texture("assets/sky.png")
ground = load_texture("assets/ground.png")

enemytex = load_texture("assets/enemy.png")
playertex = load_texture("assets/player.png")

characters = {
  "zombie": [
    enemytex,
    55,
    55
  ],
  "player": [
    playertex,
    57,
    59
  ]
}

player = Player(level.spawn[0],level.spawn[1])

time = 0
disable_cursor()


wire = False

skybox = load_model_from_mesh(gen_mesh_sphere(500,32,32))
skybox.materials[0].maps[MaterialMapIndex.MATERIAL_MAP_ALBEDO].texture = skyboxtex
rl_disable_backface_culling()


while not window_should_close():
  dt = get_frame_time()*60
  time += dt
  
  if is_key_pressed(KEY_TAB):
    wire = not wire
    if wire:
      rl_enable_wire_mode()
    else:
      rl_disable_wire_mode()
  if is_key_pressed(KEY_F11):
    toggle_borderless_windowed()
  if is_key_down(KEY_W):
    player.velocity.x += 0.1*dt
  if is_key_down(KEY_S):
    player.velocity.x -= 0.1*dt 
  if is_key_down(KEY_A):
    player.velocity.z += 0.1*dt
  if is_key_down(KEY_D):
    player.velocity.z -= 0.1*dt
  if is_key_down(KEY_SPACE):
    #player.velocity.y += 0.1*dt
    player.position.y += 0.5*dt
  if is_key_down(KEY_LEFT_SHIFT):
    #player.velocity.y -= 0.1*dt
    player.position.y -= 0.5*dt
  
  player.move()
    
  # do rendering shit
  begin_drawing()
  clear_background(BLACK)
  begin_mode_3d(player.camera)
  
  rl_push_matrix()
  rl_translatef(player.position.x,player.position.y,player.position.z)
  rl_rotatef(90,1,0,0)
  draw_model(skybox,(0,0,0),1,WHITE)
  rl_pop_matrix()
    
  
  for i in level.walls:
    draw_wall(ground, Vector3(i[0][0],0,i[0][1]),Vector2(i[1][0],i[1][1]),i[2],WHITE,i[2]*(1/10))
  for i in level.floors:
    draw_floor(ground, Vector2(i[0][0],i[0][1]),Vector2(i[1][0],i[1][1]),Vector2(i[2][0],i[2][1]),Vector2(i[3][0],i[3][1]),i[4],WHITE,2)
  draw_character(characters["zombie"],player.camera,Vector3(1,0,1),time)
  
  
  end_shader_mode()
  end_mode_3d()
  draw_circle(get_screen_width()//2,get_screen_height()//2,3,(128,128,128,128))
  draw_fps(10,10)
  draw_text("3D Engine test v0.2-1",10,30,20,WHITE)
  end_drawing()
