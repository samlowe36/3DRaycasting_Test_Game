import math

# game settings

res = width, height = 1600, 900     #sets resolution
half_width = width // 2
half_height = height // 2
fps = 60    # sets fps

#initial settings for the player (speed of movement, camera rotation, starting location, and angle of player's direction
player_pos = 1.5, 5 #mini_map
player_angle = 0
player_speed = 0.004
player_rot_speed = 0.002

fov = math.pi / 3
half_fov = fov / 2
num_rays = width // 2       #this block is math required for the raycasting and our field of view
half_num_rays = num_rays // 2
delta_angle = fov / num_rays
max_depth = 20

screen_dist = half_width/ math.tan(half_fov)    #settings for the pseudo 3d
scale = width // num_rays