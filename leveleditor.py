from pyray import *
import random
from math import *
from rayextra import *
import level

def draw_text_cam(text,x,y,size,color):
  global status
  status = text

set_config_flags(FLAG_WINDOW_RESIZABLE)
init_window(1280,720,"leveleditor")
set_exit_key(0)

mode = 0
pos1 = 0
pos2 = 0
pos3 = 0
pos4 = 0
spawn = Vector2(0,0)

global cam
cam = Camera2D(Vector2(0,0),Vector2(0,0),0,2)

walls = []
floors = []

try:
  for i in level.walls:
    walls.append([Vector2(i[0][0],i[0][1]),Vector2(i[1][0],i[1][1]),i[2]])
  spawn = Vector2(level.spawn[0],level.spawn[1])
  for i in level.floors:
    floors.append([Vector2(i[0][0],i[0][1]),Vector2(i[1][0],i[1][1]),Vector2(i[2][0],i[2][1]),Vector2(i[3][0],i[3][1]),i[4]])
except:
  pass

drawtooltip = [False,0,0,10,10,""]
status = ""

while not window_should_close():
  status = ""
  zoomdiv = (1/cam.zoom)
  dt = get_frame_time()*60
  drawtooltip[0] = False
  drawtooltip[5] = ""
  mp = get_screen_to_world_2d(get_mouse_position(),cam)
  
  begin_drawing()
  clear_background(BLACK)
  begin_mode_2d(cam)
  
  if is_mouse_button_down(MouseButton.MOUSE_BUTTON_MIDDLE):
    delta = get_mouse_delta()
    delta = vector2_scale(delta, -1.0 / cam.zoom)
    cam.target = vector2_add(cam.target, delta)
  
  wheel = get_mouse_wheel_move()
  if wheel != 0:
    mouseWorldPos = get_screen_to_world_2d(get_mouse_position(),cam)
    cam.offset = get_mouse_position()
    cam.target = mouseWorldPos
    cam.zoom += wheel*0.125
    if cam.zoom < 0.125:
      cam.zoom = 0.125
  
  draw_pixel(0,0,WHITE)
  
  if is_key_down(KEY_LEFT):
    cam.target.x -= 10*dt
  if is_key_down(KEY_RIGHT):
    cam.target.x += 10*dt
  if is_key_down(KEY_UP):
    cam.target.y -= 10*dt
  if is_key_down(KEY_DOWN):
    cam.target.y += 10*dt
  
  if is_key_pressed(KEY_W):
    if mode == 1:
      mode = 0
    else:
      pos1 = 0
      pos2 = 0
      mode = 1
  if is_key_pressed(KEY_F):
    if mode == 4:
      mode = 0
    else:
      mode = 4
      pos1 = 0
      pos2 = 0
      pos3 = 0
      pos4 = 0
  if is_key_pressed(KEY_A):
    if mode == 2:
      mode = 0
    else:
      mode = 2
  if is_key_pressed(KEY_S):
    with open("level.py","w") as f:
      string = "walls = ["
      for i in walls:
        string += str([[i[0].x,i[0].y],[i[1].x,i[1].y],i[2]]) + ","
      string += f"]\nspawn = {spawn.x,spawn.y}\nfloors = ["
      for i in floors:
        string += str([[i[0].x,i[0].y],[i[1].x,i[1].y],[i[2].x,i[2].y],[i[3].x,i[3].y],i[4]]) + ","
      string += "]"
      f.write(string)
  if is_key_pressed(KEY_Q):
    break
  if is_key_pressed(KEY_D):
    if mode == 3:
      mode = 0
    else:
      mode = 3
  if is_key_pressed(KEY_E):
    if mode == 5:
      mode = 0
    else:
      mode = 5
  if is_key_pressed(KEY_P):
    spawn = mp
  
  if mode == 1:
    draw_text_cam("Wall Mode, press W to exit",10,10,20,WHITE)
    if pos1 == 0:
      p1 = mp
    if pos2 == 0:
      p2 = mp

    # Function to find the closest point within a threshold
    def find_closest_point(current_pos, threshold=10):
        closest_point = current_pos
        min_distance = float('inf')
        for wall in walls:
            for point in wall[0:2]:
                distance = vector_2distance(current_pos, point)
                if distance < (threshold*zoomdiv) and distance < min_distance:
                    closest_point = point
                    min_distance = distance
        for floor in floors:
            for point in floor[0:4]:
                distance = vector_2distance(current_pos, point)
                if distance < (threshold*zoomdiv) and distance < min_distance:
                    closest_point = point
                    min_distance = distance
        return closest_point

    # Apply snapping to p1 and p2
    p1 = find_closest_point(p1)
    p2 = find_closest_point(p2)

    if pos1 != 0 and pos2 != 0:
        walls.append([p1, p2,5])
        p1 = p2
        p2 = mp  # Reset p2 to current mouse position
        pos2 = 0
        continue
    if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
      if pos1 == 0:
        pos1 = find_closest_point(get_mouse_position())
      else:
        pos2 = find_closest_point(get_mouse_position())
    draw_circle_v(p1, 3*zoomdiv, BLUE)
    draw_line_v([p1.x, p1.y], [p2.x, p2.y], WHITE)
    draw_circle_v(p2, 3*zoomdiv, ORANGE)
  
  if mode == 4:
    draw_text_cam("Floor Mode, press F to exit",10,10,20,WHITE)
    if pos1 == 0:
      p1 = mp
    if pos2 == 0:
      p2 = mp
    if pos3 == 0:
      p3 = mp
    if pos4 == 0:
      p4 = mp

    # Function to find the closest point within a threshold
    def find_closest_point(current_pos, threshold=10):
        closest_point = current_pos
        min_distance = float('inf')
        for wall in walls:
            for point in wall[0:2]:
                distance = vector_2distance(current_pos, point)
                if distance < (threshold*zoomdiv) and distance < min_distance:
                    closest_point = point
                    min_distance = distance
        for floor in floors:
            for point in floor[0:4]:
                distance = vector_2distance(current_pos, point)
                if distance < (threshold*zoomdiv) and distance < min_distance:
                    closest_point = point
                    min_distance = distance
        return closest_point

    # Apply snapping to p1, p2, p3, and p4
    p1 = find_closest_point(p1)
    p2 = find_closest_point(p2)
    p3 = find_closest_point(p3)
    p4 = find_closest_point(p4)

    if pos1 != 0 and pos2 != 0 and pos3 != 0 and pos4 != 0:
        f = [p1, p2, p3, p4]
        #f.reverse()
        f.append(0)
        floors.append(f)
        p1 = p4
        p2 = mp
        p3 = mp
        p4 = mp
        pos2 = pos3 = pos4 = 0
        continue
    if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
      if pos1 == 0:
        pos1 = find_closest_point(get_mouse_position())
      elif pos2 == 0:
        pos2 = find_closest_point(get_mouse_position())
      elif pos3 == 0:
        pos3 = find_closest_point(get_mouse_position())
      else:
        pos4 = find_closest_point(get_mouse_position())
    draw_circle_v(p1, 3*zoomdiv, BLUE)
    draw_line_v([p1.x, p1.y], [p2.x, p2.y], WHITE)
    draw_line_v([p2.x, p2.y], [p3.x, p3.y], WHITE)
    draw_line_v([p3.x, p3.y], [p4.x, p4.y], WHITE)
    draw_line_v([p4.x, p4.y], [p1.x, p1.y], WHITE)
    draw_circle_v(p2, 3*zoomdiv, ORANGE)
    draw_circle_v(p3, 3*zoomdiv, GREEN)
    draw_circle_v(p4, 3*zoomdiv, RED)
  if mode == 2:
    draw_text_cam("Display Mode, press A to exit",10,10,20,WHITE)
    for ind,val in enumerate(walls):
      draw_text_cam(f"({val[0].x}, {val[0].y}) ({val[1].x}, {val[1].y})",10,30+(20*ind),20,WHITE)
  
  for ind,i in enumerate(walls):
    if check_collision_point_line(mp,[i[0].x,i[0].y],[i[1].x,i[1].y],5):
      if is_key_pressed(KEY_PAGE_UP):
        i[2]+=1
      if is_key_pressed(KEY_PAGE_DOWN):
        i[2]-=1
      if mode == 0:
        color = GREEN
        if is_key_pressed(KEY_I):
          oldpos1 = walls[ind][0]
          walls[ind][0] = walls[ind][1]
          walls[ind][1] = oldpos1
        drawtooltip[0] = True
        drawtooltip[5] += f"Wall {ind}\nPos = ({i[0].x:.5}, {i[0].y:.5}) - ({i[1].x:.5}, {i[1].y:.5})\nHeight: {i[2]}\nLength = {vector_2distance(i[0],i[1]):.5}\ndx: {abs(i[1].x-i[0].x):.5} - dy: {abs(i[1].y-i[0].y):.5}\n\n"
    else:
      color = (255-(i[2]*2)%255,255-(i[2]*2)%255,255,255)
    draw_line_v([i[0].x,i[0].y],[i[1].x,i[1].y],color)
    direction = Vector2(i[1].x - i[0].x, i[1].y - i[0].y)
    direction = vector2_normalize(direction)
    center = Vector2((i[0].x + i[1].x) / 2, (i[0].y + i[1].y) / 2)
    direction.y *= -1
    end_point = Vector2(center.x + direction.y * 5, center.y + direction.x * 5)
    draw_line_v([center.x, center.y], [end_point.x, end_point.y], YELLOW)
    draw_circle_v(end_point, 3*zoomdiv, YELLOW)

  for ind,i in enumerate(floors):
    if check_collision_point_line(mp,[i[0].x,i[0].y],[i[1].x,i[1].y],5) or check_collision_point_line(mp,[i[1].x,i[1].y],[i[2].x,i[2].y],5) or check_collision_point_line(mp,[i[2].x,i[2].y],[i[3].x,i[3].y],5) or check_collision_point_line(mp,[i[3].x,i[3].y],[i[0].x,i[0].y],5):
      if is_key_pressed(KEY_PAGE_UP):
        i[4]+=1
      if is_key_pressed(KEY_PAGE_DOWN):
        i[4]-=1
      if is_key_pressed(KEY_I):
        oldpos1 = floors[ind][0]
        floors[ind][0] = floors[ind][2]
        floors[ind][2] = oldpos1
      if mode == 0:
        color = GREEN
        drawtooltip[0] = True
        drawtooltip[5] += f"Floor {ind}\nPos = ({i[0].x:.5}, {i[0].y:.5}) - ({i[1].x:.5}, {i[1].y:.5}) - ({i[2].x:.5}, {i[2].y:.5}) - ({i[3].x:.5}, {i[3].y:.5})\nHeight: {i[4]}\n\n"
    else:
      color = (255-(i[4]*2)%255,255-(i[4]*2)%255,255,255)
    draw_line_v([i[0].x,i[0].y],[i[1].x,i[1].y],color)
    draw_line_v([i[1].x,i[1].y],[i[2].x,i[2].y],color)
    draw_line_v([i[2].x,i[2].y],[i[3].x,i[3].y],color)
    draw_line_v([i[3].x,i[3].y],[i[0].x,i[0].y],color)    
    # Draw line pointing towards direction vector from the center

    
  
  if mode == 3:
    draw_text_cam("Delete Walls Mode, press D to exit",10,10,20,WHITE)
    for ind,val in enumerate(walls):
      if check_collision_point_line(mp,[val[0].x,val[0].y],[val[1].x,val[1].y],5):
        draw_line_v([val[0].x,val[0].y],[val[1].x,val[1].y],RED)
        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
          walls.pop(ind)
          break

  if mode == 5:
    draw_text_cam("Delete Floors Mode, press E to exit",10,10,20,WHITE)
    for ind,val in enumerate(floors):
      if check_collision_point_line(mp,[val[0].x,val[0].y],[val[1].x,val[1].y],5) or \
         check_collision_point_line(mp,[val[1].x,val[1].y],[val[2].x,val[2].y],5) or \
         check_collision_point_line(mp,[val[2].x,val[2].y],[val[3].x,val[3].y],5) or \
         check_collision_point_line(mp,[val[3].x,val[3].y],[val[0].x,val[0].y],5):
        draw_line_v([val[0].x,val[0].y],[val[1].x,val[1].y],RED)
        draw_line_v([val[1].x,val[1].y],[val[2].x,val[2].y],RED)
        draw_line_v([val[2].x,val[2].y],[val[3].x,val[3].y],RED)
        draw_line_v([val[3].x,val[3].y],[val[0].x,val[0].y],RED)
        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
          floors.pop(ind)
          break  
  
  draw_circle_v(spawn,3*zoomdiv,GREEN)
  
  
  end_mode_2d()
  mp = get_mouse_position()
  if drawtooltip[0]:
    w = measure_text(drawtooltip[5],10)+20
    h = len(drawtooltip[5].split("\n")*10)+20
    draw_rectangle_rec([mp.x+10,mp.y+10,w,h],(20,20,20,200))
    draw_rectangle_lines_ex([mp.x+10,mp.y+10,w,h],1,WHITE)
    for ind,i in enumerate(drawtooltip[5].split("\n")):
      draw_text(i,round(mp.x)+20,round(mp.y)+20+(ind*10),10,WHITE)
  draw_text(status,10,10,20,WHITE)
  end_drawing()

close_window()
