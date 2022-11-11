import pygame, sys, math, json
pygame.init()

class Spriteclass: # used to set up where and what sprite
    def __init__(self, sprite, xy):
        self.image = sprite[0]
        self.scale = sprite[1]
        self.shift = sprite[2]
        self.xy = xy

class Animatedsprite(Spriteclass): # animated sprites move
    def __init__(self, sprite, xy):
        super().__init__(sprite, xy)
        self.images = sprite[0]
        self.image_index = 0
        self.framerate = sprite[3]
        self.curr_frame = 0

class Drawobject: # used to draw in 3d
    def __init__(self, image, pos_3d, depth):
        self.x_3d, self.y_3d = pos_3d
        self.xy_3d = (self.x_3d, self.y_3d)
        self.image = image
        self.depth = depth

def draw2d():
    # draw
    game_display.fill((0,0,0))

    # draw walls
    for block in map:
        if map[block] == 1:
            game_display.blit(wall00_small, (block[0]*50, block[1]*50))
        elif map[block] == 2:
            game_display.blit(wall01_small, (block[0]*50, block[1]*50))

    # draw grid
    [pygame.draw.line(game_display, (100,100,100), (x*50, 0), (x*50, screen_size[1])) for x in range(screen_size[0]//50)]
    [pygame.draw.line(game_display, (100,100,100), (0, y*50), (screen_size[0], y*50)) for y in range(screen_size[1]//50)]

    # draw player
    pygame.draw.circle(game_display, (255,255,0), (player_x*50, player_y*50), 10)
    direction_x = math.cos(player_angle)*15
    direction_y = math.sin(player_angle)*15
    pygame.draw.line(game_display, (255,255,0), (player_x*50, player_y*50), (player_x*50+direction_x, player_y*50+direction_y), 3)

    # draw sprites
    [pygame.draw.circle(game_display, (255,0,0), (sprite.xy[0]*50, sprite.xy[1]*50), 10) for sprite in sprites]
    [pygame.draw.circle(game_display, (255,100,0), (sprite.xy[0]*50, sprite.xy[1]*50), 10) for sprite in animated_sprites]

    pygame.display.update()

def draw3d():
    # draw floor
    pygame.draw.rect(game_display, (150,150,150), (0, screen_size[1]/2, screen_size[0], screen_size[1]))

    # draw sky
    game_display.blit(sky, (sky_offset, 0))
    game_display.blit(sky, (sky_offset-screen_size[0], 0))

    # draw walls
    rays.sort(key=lambda x: x.depth)
    for ray in rays[::-1]:
        game_display.blit(ray.image, ray.xy_3d)

    # weapon
    game_display.blit(weapon_sprites[weapon_index], weapon_screen_pos)

    pygame.display.update()

# initilize
screen_size = (800,500)
game_display = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
draw_3d = True

# texture
# sky
sky = pygame.image.load('sky.png').convert()
sky = pygame.transform.scale(sky, (screen_size[0], screen_size[1]//2))

wall00 = pygame.image.load('wall00.png').convert()
wall00 = pygame.transform.scale(wall00, (256,256))
wall00_small = pygame.transform.scale(wall00, (50,50))
wall01 = pygame.image.load('wall01.png').convert()
wall01 = pygame.transform.scale(wall01, (256,256))
wall01_small = pygame.transform.scale(wall01, (50,50))

textures = {
    1: wall00,
    2: wall01
}

# sprites
rock = pygame.image.load('rock.png').convert_alpha()
rock_settings = [rock, 0.5, 0.5]
metal_ball = pygame.image.load('metal_ball.png').convert_alpha()
metal_ball_settings = [metal_ball, 0.5, 0.6]

sprites = []

# animated sprites
crystal1 = pygame.image.load('crystal1.png').convert_alpha()
crystal2 = pygame.image.load('crystal2.png').convert_alpha()
crystal3 = pygame.image.load('crystal3.png').convert_alpha()
crystal_settings = [(crystal1, crystal2, crystal3), 1.0, 0.2, 10]
fire1 = pygame.image.load('fire1.png').convert_alpha()
fire2 = pygame.image.load('fire2.png').convert_alpha()
fire3 = pygame.image.load('fire3.png').convert_alpha()
fire_settings = [(fire1, fire2, fire3), 1.0, 0.2, 5]

animated_sprites = []

# weapon
shotgun1 = pygame.image.load('shotgun1.png').convert_alpha()
shotgun2 = pygame.image.load('shotgun2.png').convert_alpha()
shotgun3 = pygame.image.load('shotgun3.png').convert_alpha()
weapon_sprites = (shotgun1, shotgun2, shotgun3)

# json
json_file = json.load(open('map.json'))

map_size = json_file['map size']
map = {}
for wall in json_file['map']:
    map[(wall[0][0], wall[0][1])] = wall[1]

for sprite in json_file['sprites']:
    if sprite[1] == 1:
        sprites.append(Spriteclass(rock_settings, (sprite[0][0], sprite[0][1])))
    elif sprite[1] == 2:
        sprites.append(Spriteclass(metal_ball_settings, (sprite[0][0], sprite[0][1])))
    elif sprite[1] == 3:
        animated_sprites.append(Animatedsprite(crystal_settings, (sprite[0][0], sprite[0][1])))
    elif sprite[1] == 4:
        animated_sprites.append(Animatedsprite(fire_settings, (sprite[0][0], sprite[0][1])))

# player
player_x, player_y = json_file['player']
player_angle = 1
fov = math.pi / 3
half_fov = fov / 2
num_rays = screen_size[0] // 2
ray_angle_incroment = fov / num_rays

# weapon
weapon_reloading = False
weapon_animation = 0
weapon_index = 0
weapon_screen_pos = (screen_size[0]/2-shotgun1.get_width()/2,screen_size[1]-shotgun1.get_height())

# screen
screen_dis = (screen_size[0] // 2) / math.tan(half_fov)
scale = screen_size[0] // num_rays
sky_offset = 0


while True:
    pygame.display.set_caption(str(int(clock.get_fps())))

    # event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN:
                draw_3d = not draw_3d

            # shoot weapon
            if event.key == pygame.K_SPACE and weapon_reloading == False:
                weapon_reloading = True
                weapon_index += 1

    # weapon
    if weapon_reloading:
        weapon_animation += 1
        if weapon_animation == 5:
            weapon_animation = 0
            weapon_index += 1
            if weapon_index == len(weapon_sprites):
                weapon_index = 0
                weapon_reloading = False

    # ray
    rays = []
    ray_offset = half_fov
    for ray_index in range(num_rays):
        x_map = int(player_x)
        y_map = int(player_y)
        ray_angle = player_angle + ray_offset
        dir_x = math.cos(ray_angle)
        dir_y = math.sin(ray_angle)

        # vertical
        if dir_x > 0: # looking right
            x_vert, dx = x_map + 1, 1
        else: # looking left
            x_vert, dx = x_map - 1e-6, -1

        depth_vert = (x_vert - player_x) / dir_x
        y_vert = (player_y + depth_vert * dir_y)

        delta_depth = dx / dir_x
        dy = delta_depth * dir_y

        for i in range(map_size[0]):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert in map:
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        # horisontal
        if dir_y > 0:
            y_hor, dy = (y_map + 1, 1)
        else:
            y_hor, dy = (y_map - 1e-6, -1)

        depth_hor = (y_hor - player_y) / dir_y
        x_hor = player_x + depth_hor * dir_x

        delta_depth = dy / dir_y
        dx = delta_depth * dir_x

        for i in range(map_size[1]):
            title_hor = int(x_hor), int(y_hor)
            if title_hor in map:
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # choose whitch ray is shortest
        if depth_vert < depth_hor:
            depth = depth_vert
            ray_xy = (x_vert, y_vert)
            axis = 'vert'
            y_vert %= 1
            if dir_x > 0:
                offset = y_vert
            else:
                offset = (1 - y_vert)
        else:
            depth = depth_hor
            ray_xy = (x_hor, y_hor)
            axis = 'hor'
            x_hor %= 1
            if dir_y > 0:
                offset = (1 - x_hor)
            else: 
                offset = x_hor

        depth *= math.cos(player_angle - ray_angle)

        if (int(ray_xy[0]), int(ray_xy[1])) in map:
            wall = map[(int(ray_xy[0]), int(ray_xy[1]))]
        else:
            wall = None

        proj_height = screen_dis / (depth + 0.0001)

        if proj_height < screen_size[1]:
            wall_pos = (screen_size[0]-((ray_index+1) * scale), (screen_size[1] // 2) - proj_height // 2)
        else:
            wall_pos = (screen_size[0]-((ray_index+1) * scale), 0)

        # get wall image
        if wall != None:
            proj_height = screen_dis / (depth + 0.0001)
    
            if proj_height < screen_size[1]:
                wall_column = textures[wall].subsurface(offset * (256 - scale), 0, scale, 256)
                wall_column = pygame.transform.scale(wall_column, (scale, proj_height))
            else:
                texture_height = 256 * screen_size[1] / proj_height
                wall_column = textures[wall].subsurface(offset * (256 - scale), (256//2) - texture_height // 2, scale, texture_height)
                wall_column = pygame.transform.scale(wall_column, (scale, screen_size[1]))

            if axis == 'hor': # apply shadow
                wall_column.fill((150,150,150), special_flags=pygame.BLEND_MULT)

            rays.append(Drawobject(wall_column, wall_pos, depth))
        
        ray_offset -= ray_angle_incroment

    # floor casting. needs more testing
    '''for i in range(400):
        rot_i = player_angle + (i / scale - 30)
        sin, cos = math.sin(rot_i), math.cos(rot_i)

        for j in range(125):
            n = 50/(50-j+0.0001)
            x, y = player_x + cos*n, player_y + sin*n

            if int(x)%2 == int(y)%2:
                color = (100,100,100)
            else:
                color = (255,255,255)

            pygame.draw.rect(game_display, color, (i*scale, (50*2-j)*scale, scale, scale))
    pygame.display.update()'''

    # sprites
    for sprite in sprites:
        sprite_dx = sprite.xy[0] - player_x
        sprite_dy = sprite.xy[1] - player_y
        sprite_theta = math.atan2(sprite_dy, sprite_dx)

        sprite_delta = sprite_theta - player_angle
        if (sprite_dx > 0 and player_angle > math.pi) or (sprite_dx < 0 and sprite_dy < 0):
            sprite_delta += math.tau

        sprite_delta_rays = sprite_delta / ray_angle_incroment
        sprite_screen_x = ((num_rays//2)+ sprite_delta_rays) * scale

        sprite_dist = math.hypot(sprite_dx, sprite_dy)
        sprite_norm_dist = sprite_dist * math.cos(sprite_delta)
        if -(sprite.image.get_width()//2) < screen_size[0] < screen_size[0] + (sprite.image.get_width()//2) and sprite_norm_dist > 0.5:
            sprite_proj = screen_dis / sprite_norm_dist * sprite.scale
            sprite_proj_x, sprite_proj_y = sprite_proj * (sprite.image.get_width() / sprite.image.get_height()), sprite_proj

            new_sprite_image = pygame.transform.scale(sprite.image, (sprite_proj_x, sprite_proj_y))

            sprite_half_width = sprite_proj_x // 2
            sprite_height_shift = sprite_proj_y * sprite.shift
            sprite_pos = sprite_screen_x - sprite_half_width, (screen_size[1]//2) - sprite_proj_y // 2 + sprite_height_shift

            rays.append(Drawobject(new_sprite_image, sprite_pos, sprite_norm_dist))

    # animated sprites
    for sprite in animated_sprites:
        sprite_dx = sprite.xy[0] - player_x
        sprite_dy = sprite.xy[1] - player_y
        sprite_theta = math.atan2(sprite_dy, sprite_dx)

        sprite_delta = sprite_theta - player_angle
        if (sprite_dx > 0 and player_angle > math.pi) or (sprite_dx < 0 and sprite_dy < 0):
            sprite_delta += math.tau

        sprite_delta_rays = sprite_delta / ray_angle_incroment
        sprite_screen_x = ((num_rays//2)+ sprite_delta_rays) * scale

        sprite_dist = math.hypot(sprite_dx, sprite_dy)
        sprite_norm_dist = sprite_dist * math.cos(sprite_delta)
        sprite_image = sprite.images[sprite.image_index]
        if -(sprite_image.get_width()//2) < screen_size[0] < screen_size[0] + (sprite_image.get_width()//2) and sprite_norm_dist > 0.5:
            sprite_proj = screen_dis / sprite_norm_dist * sprite.scale
            sprite_proj_x, sprite_proj_y = sprite_proj * (sprite_image.get_width() / sprite_image.get_height()), sprite_proj

            new_sprite_image = pygame.transform.scale(sprite_image, (sprite_proj_x, sprite_proj_y))

            sprite_half_width = sprite_proj_x // 2
            sprite_height_shift = sprite_proj_y * sprite.shift
            sprite_pos = sprite_screen_x - sprite_half_width, (screen_size[1]//2) - sprite_proj_y // 2 + sprite_height_shift

            rays.append(Drawobject(new_sprite_image, sprite_pos, sprite_norm_dist))

        sprite.curr_frame += 1
        if sprite.curr_frame == sprite.framerate:
            sprite.curr_frame = 0
            sprite.image_index += 1
            if sprite.image_index == len(sprite.images):
                sprite.image_index = 0

    # player_movement
    keys = pygame.key.get_pressed()

    # turn right and left
    if keys[pygame.K_RIGHT]: # turn right
        sky_offset -= 16
        if sky_offset < 0:
            sky_offset += screen_size[0]
        player_angle += 0.02
        if player_angle > math.pi*2:
            player_angle -= math.pi*2
    if keys[pygame.K_LEFT]: # turn left
        sky_offset += 16
        if sky_offset > screen_size[0]:
            sky_offset -= screen_size[0]
        player_angle -= 0.02
        if player_angle < 0:
            player_angle += math.pi*2

    # move foward and backwards
    dir_x = math.cos(player_angle)*0.05
    dir_y = math.sin(player_angle)*0.05
    if keys[pygame.K_w]: # move fowards
        if (int(player_x + dir_x), int(player_y)) not in map:
            player_x += dir_x
        if (int(player_x), int(player_y + dir_y)) not in map:
            player_y += dir_y
    if keys[pygame.K_s]: # move backwards
        if (int(player_x - dir_x), int(player_y)) not in map:
            player_x -= dir_x
        if (int(player_x), int(player_y - dir_y)) not in map:
            player_y -= dir_y

    # move sideways
    dir_x = math.cos(player_angle+(math.pi/2))*0.05
    dir_y = math.sin(player_angle+(math.pi/2))*0.05
    if keys[pygame.K_d]: # move right
        if (int(player_x + dir_x), int(player_y)) not in map:
            player_x += dir_x
        if (int(player_x), int(player_y + dir_y)) not in map:
            player_y += dir_y
    if keys[pygame.K_a]: # move left
        if (int(player_x - dir_x), int(player_y)) not in map:
            player_x -= dir_x
        if (int(player_x), int(player_y - dir_y)) not in map:
            player_y -= dir_y

    if draw_3d:
        draw3d()
    else:
        draw2d()
    
    clock.tick(60)