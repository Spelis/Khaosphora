from typing import Any
from pyray import *
from math import *

FLAG_VSYNC_HINT = 64
FLAG_FULLSCREEN_MODE = 2
FLAG_WINDOW_RESIZABLE = 4
FLAG_WINDOW_UNDECORATED = 8
FLAG_WINDOW_HIDDEN = 128
FLAG_WINDOW_MINIMIZED = 512
FLAG_WINDOW_MAXIMIZED = 1024
FLAG_WINDOW_UNFOCUSED = 2048
FLAG_WINDOW_TOPMOST = 4096
FLAG_WINDOW_ALWAYS_RUN = 256
FLAG_WINDOW_TRANSPARENT = 16
FLAG_WINDOW_HIGHDPI = 8192
FLAG_WINDOW_MOUSE_PASSTHROUGH = 16384
FLAG_BORDERLESS_WINDOWED_MODE = 32768
FLAG_MSAA_4X_HINT = 32
FLAG_INTERLACED_HINT = 65536

KEY_NULL = 0
KEY_APOSTROPHE = 39
KEY_COMMA = 44
KEY_MINUS = 45
KEY_PERIOD = 46
KEY_SLASH = 47
KEY_ZERO = 48
KEY_ONE = 49
KEY_TWO = 50
KEY_THREE = 51
KEY_FOUR = 52
KEY_FIVE = 53
KEY_SIX = 54
KEY_SEVEN = 55
KEY_EIGHT = 56
KEY_NINE = 57
KEY_SEMICOLON = 59
KEY_EQUAL = 61
KEY_A = 65
KEY_B = 66
KEY_C = 67
KEY_D = 68
KEY_E = 69
KEY_F = 70
KEY_G = 71
KEY_H = 72
KEY_I = 73
KEY_J = 74
KEY_K = 75
KEY_L = 76
KEY_M = 77
KEY_N = 78
KEY_O = 79
KEY_P = 80
KEY_Q = 81
KEY_R = 82
KEY_S = 83
KEY_T = 84
KEY_U = 85
KEY_V = 86
KEY_W = 87
KEY_X = 88
KEY_Y = 89
KEY_Z = 90
KEY_LEFT_BRACKET = 91
KEY_BACKSLASH = 92
KEY_RIGHT_BRACKET = 93
KEY_GRAVE = 96
KEY_SPACE = 32
KEY_ESCAPE = 256
KEY_ENTER = 257
KEY_TAB = 258
KEY_BACKSPACE = 259
KEY_INSERT = 260
KEY_DELETE = 261
KEY_RIGHT = 262
KEY_LEFT = 263
KEY_DOWN = 264
KEY_UP = 265
KEY_PAGE_UP = 266
KEY_PAGE_DOWN = 267
KEY_HOME = 268
KEY_END = 269
KEY_CAPS_LOCK = 280
KEY_SCROLL_LOCK = 281
KEY_NUM_LOCK = 282
KEY_PRINT_SCREEN = 283
KEY_PAUSE = 284
KEY_F1 = 290
KEY_F2 = 291
KEY_F3 = 292
KEY_F4 = 293
KEY_F5 = 294
KEY_F6 = 295
KEY_F7 = 296
KEY_F8 = 297
KEY_F9 = 298
KEY_F10 = 299
KEY_F11 = 300
KEY_F12 = 301
KEY_LEFT_SHIFT = 340
KEY_LEFT_CONTROL = 341
KEY_LEFT_ALT = 342
KEY_LEFT_SUPER = 343
KEY_RIGHT_SHIFT = 344
KEY_RIGHT_CONTROL = 345
KEY_RIGHT_ALT = 346
KEY_RIGHT_SUPER = 347
KEY_KB_MENU = 348
KEY_KP_0 = 320
KEY_KP_1 = 321
KEY_KP_2 = 322
KEY_KP_3 = 323
KEY_KP_4 = 324
KEY_KP_5 = 325
KEY_KP_6 = 326
KEY_KP_7 = 327
KEY_KP_8 = 328
KEY_KP_9 = 329
KEY_KP_DECIMAL = 330
KEY_KP_DIVIDE = 331
KEY_KP_MULTIPLY = 332
KEY_KP_SUBTRACT = 333
KEY_KP_ADD = 334
KEY_KP_ENTER = 335
KEY_KP_EQUAL = 336
KEY_BACK = 4
KEY_VOLUME_UP = 24
KEY_VOLUME_DOWN = 25

def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)
  

  
def draw_wall(texture, startpos,endpos, height, color,texsize):
    color = Color(color[0], color[1], color[2], color[3])
    rl_set_texture(texture.id)
    rl_begin(0x0007) # QUADS
    rl_color4ub(color.r, color.g, color.b, color.a)
    
    texw = (calculate_distance([startpos.x,startpos.z],[endpos.x,endpos.y])*texsize)/(height+0.01)
    
    rl_normal3f(0.0, 0.0, 1.0)       # Normal Pointing Towards Viewer
    rl_tex_coord2f(0.0, texsize);     rl_vertex3f(startpos.x,         startpos.y,          startpos.z)  # Bottom Left Of The Texture and Quad
    rl_tex_coord2f(texw, texsize);    rl_vertex3f(endpos.x,           startpos.y,          endpos.y)  # Bottom Right Of The Texture and Quad
    rl_tex_coord2f(texw, 0.0);        rl_vertex3f(endpos.x,           startpos.y + height, endpos.y)  # Top Right Of The Texture and Quad
    rl_tex_coord2f(0.0, 0.0);         rl_vertex3f(startpos.x,         startpos.y + height, startpos.z)  # Top Left Of The Texture and Quad

    rl_set_texture(0)


def draw_floor(texture, pos1, pos2, pos3, pos4, height, color, texsize):
    color = Color(color[0], color[1], color[2], color[3])
    rl_set_texture(texture.id)

    rl_begin(0x0007)  # QUADS
    rl_color4ub(color.r, color.g, color.b, color.a)

    texw = calculate_distance([pos1.x, pos1.y], [pos2.x, pos2.y]) / texsize/3
    texh = calculate_distance([pos1.x, pos1.y], [pos4.x, pos4.y]) / texsize/3

    rl_normal3f(0.0, 1.0, 0.0)  # Normal Pointing Upwards
    rl_tex_coord2f(0.0, 0.0);    rl_vertex3f(pos1.x, height, pos1.y)  # Top Left Of The Texture and Quad
    rl_tex_coord2f(texw, 0.0);   rl_vertex3f(pos2.x, height, pos2.y)  # Top Right Of The Texture and Quad
    rl_tex_coord2f(texw, texh);  rl_vertex3f(pos3.x, height, pos3.y)  # Bottom Right Of The Texture and Quad
    rl_tex_coord2f(0.0, texh);   rl_vertex3f(pos4.x, height, pos4.y)  # Bottom Left Of The Texture and Quad

    rl_set_texture(0)


def get_angle(point_a, point_b):
    dx = point_b.x - point_a.x
    dy = point_b.z - point_a.z
    angle_radians = atan2(dy, dx)
    angle_degrees = degrees(angle_radians)
    return angle_degrees
  
def xz2angle(x,z):
      angle_radians = atan2(z, x)
      angle_degrees = degrees(angle_radians)
      return angle_degrees
  
  
def get8sided(a,b):
      angle = get_angle(a, b)
      normalized_angle = (angle + 360) % 360
      normalized_angle *= -1
      octant = int((normalized_angle - 22.5) / 45) % 8
      return octant
  

class rec:
  def __init__(self,x,y,w,h):
    self.x = x
    self.y = y
    self.width = w
    self.height = h
    
def draw_text(text, pos_x, pos_y, font_size, color):
    # Check if default font has been loaded
    if get_font_default().texture.id != 0:
        position = Vector2((float)(pos_x), (float)(pos_y))

        default_font_size = 10   # Default Font chars height in pixel
        if font_size < 0:
            font_size = 0
        spacing = font_size / default_font_size

        draw_text_ex(get_font_default(), text, position, float(font_size), float(spacing), color)

def measure_text(text, font_size):
    text_size = Vector2(0.0, 0.0)

    # Check if default font has been loaded
    if get_font_default().texture.id != 0:
        default_font_size = 10   # Default Font chars height in pixel
        if font_size < 0:
            font_size = 0
        spacing = font_size / default_font_size

        text_size = measure_text_ex(get_font_default(), text, float(font_size), float(spacing))

    return int(text_size.x)

def draw_texture_3d(name,texture, cam, position, size, color, rot=None, texoff:tuple=(0,0,None,None)):
    texoff = rec(texoff[0], texoff[1], texoff[2] or texture.width, texoff[3] or texture.height)
    campos = cam.position
    if texoff.height < 0:
      texoff.y -= texoff.height
    x, y, z = position.x, position.y, position.z
    width, height, length = size.x, size.y, size.z
    if rot == None:
        rot = -get_angle(campos, position)
        doubleside = False
    else:
        rot = rot
        doubleside = True
    rl_begin(0x0007)
    rl_set_texture(texture.id)
    rl_color4ub(*color)

    rot = radians(rot)
    wt = width / 2

    source_width = texoff.width
    source_height = texoff.height
    dest_width = width
    dest_height = height

    rl_normal3f(0.0, 0.0, 1.0)  # Normal Pointing Towards Viewer
    rl_tex_coord2f(texoff.x / texture.width, texoff.y / texture.height);                           rl_vertex3f(x - (wt * sin(rot)), y, z - (wt * cos(rot)))  # Bottom Left
    rl_tex_coord2f((texoff.x + source_width) / texture.width, texoff.y / texture.height);          rl_vertex3f(x + (wt * sin(rot)), y, z + (wt * cos(rot)))  # Bottom Right
    rl_tex_coord2f((texoff.x + source_width) / texture.width, (texoff.y + source_height) / texture.height); rl_vertex3f(x + (wt * sin(rot)), y + height, z + (wt * cos(rot)))  # Top Right
    rl_tex_coord2f(texoff.x / texture.width, (texoff.y + source_height) / texture.height);         rl_vertex3f(x - (wt * sin(rot)), y + height, z - (wt * cos(rot)))  # Top Left
    if doubleside:
        rl_normal3f(0.0, 0.0, -1.0)  # Normal Pointing Away From Viewer
        rl_tex_coord2f(texoff.x / texture.width, texoff.y / texture.height);                           rl_vertex3f(x + (wt * sin(rot)), y, z + (wt * cos(rot)))  # Bottom Left
        rl_tex_coord2f((texoff.x + source_width) / texture.width, texoff.y / texture.height);          rl_vertex3f(x - (wt * sin(rot)), y, z - (wt * cos(rot)))  # Bottom Right
        rl_tex_coord2f((texoff.x + source_width) / texture.width, (texoff.y + source_height) / texture.height); rl_vertex3f(x - (wt * sin(rot)), y + height, z - (wt * cos(rot)))  # Top Right
        rl_tex_coord2f(texoff.x / texture.width, (texoff.y + source_height) / texture.height);         rl_vertex3f(x + (wt * sin(rot)), y + height, z + (wt * cos(rot)))  # Top Left
    rl_end()
    
    rl_push_matrix()
    textpos = vector3_add(position, Vector3(0,size.y,0))
    rot = -(get_angle(campos, textpos))-90
    
    rl_translatef(textpos.x, textpos.y, textpos.z)
    rl_rotatef(rot,0,1,0)
    rl_rotatef(180,1,0,0)
    
    draw_text_ex(get_font_default(), name, Vector2(0,0), 10, 1, WHITE)
    
    rl_pop_matrix()

def draw_character(_type,cam,pos,time):
  # draw_texture_3d("MONSTER",enemytex,player.camera,Vector3(1,0,1),Vector3(10,10,10),WHITE,texoff=(get8sided(Vector3(player.position.x,0,player.position.z),Vector3(1,0,1))*56,(round(time/10)%4)*57,55,-54))
  character = _type
  draw_texture_3d("enemy",character[0],cam,pos,Vector3(10,10,10),WHITE,texoff=(get8sided(Vector3(cam.position.x,0,cam.position.z),Vector3(1,0,1))*56,(round(time/10)%4)*57,55,-54))
