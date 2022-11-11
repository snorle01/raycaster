import pygame, sys, json

screen_size = (800,500)
editor_display = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# map
map_size = (13,10)
map = []

# player
player_spawn = (0.5, 0.5)

# sprites
sprites_map = []

# textures
wall00 = pygame.image.load('wall00.png').convert()
wall00 = pygame.transform.scale(wall00, (50,50))
wall01 = pygame.image.load('wall01.png').convert()
wall01 = pygame.transform.scale(wall01, (50,50))

wall_textures = {
    1: wall00,
    2: wall01
}

# sprite textures
rock = pygame.image.load('rock.png').convert_alpha()
rock = pygame.transform.scale(rock, (50,50))
metal_ball = pygame.image.load('metal_ball.png').convert_alpha()
metal_ball = pygame.transform.scale(metal_ball, (50,50))
crystal = pygame.image.load('crystal1.png').convert_alpha()
crystal = pygame.transform.scale(crystal, (50,50))
fire = pygame.image.load('fire1.png').convert_alpha()
fire = pygame.transform.scale(fire, (50,50))

sprites_textures = {
    1: rock,
    2: metal_ball,
    3: crystal,
    4: fire
}

while True:
    pygame.display.set_caption(str(int(clock.get_fps())))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # change tile
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0]//50, mouse_pos[1]//50)
        if mouse_pos[0] < map_size[0] and mouse_pos[1] < map_size[1]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for wall in map:
                    if mouse_pos == (wall[0][0],wall[0][1]):
                        if pygame.mouse.get_pressed()[0]:
                            wall[1] += 1
                            if wall[1] == len(wall_textures)+1:
                                map.remove(wall)
                        if pygame.mouse.get_pressed()[2]:
                            wall[1] -= 1
                            if wall[1] == 0:
                                map.remove(wall)
                        break
                else:
                    if pygame.mouse.get_pressed()[0]:
                        map.append([mouse_pos,1])
                    if pygame.mouse.get_pressed()[2]:
                        map.append([(mouse_pos[0],mouse_pos[1]),2])
        
        if event.type == pygame.KEYDOWN:
            # exsport map
            if event.key == pygame.K_SPACE:

                data = {
                    'player': player_spawn,
                    'sprites': sprites_map,
                    'map': map,
                    'map size': map_size
                }
                with open('map.json', 'w') as json_file:
                    json.dump(data, json_file)

            # open map
            if event.key == pygame.K_RETURN:
                json_file = json.load(open('map.json'))
                player_spawn = json_file['player']
                sprites_map = json_file['sprites']
                map = json_file['map']
                map_size = json_file['map size']

            # set player spawn
            if event.key == pygame.K_p:
                player_spawn = (mouse_pos[0]+0.5, mouse_pos[1]+0.5)
            
            # place sprite
            if event.key == pygame.K_s:
                for sprite in sprites_map:
                    if mouse_pos == (sprite[0][0]-0.5,sprite[0][1]-0.5):
                        sprite[1] += 1
                        if sprite[1] == 5:
                            sprites_map.remove(sprite)
                        break
                else:
                    sprites_map.append([[mouse_pos[0]+0.5,mouse_pos[1]+0.5],1])
                
    # draw
    editor_display.fill((0,0,0))

    # draw grid
    for y, row in enumerate(range(map_size[1])):
        for x, wall in enumerate(range(map_size[0])):
            pygame.draw.rect(editor_display, (255,255,255), (x*50, y*50, 50, 50), 1)

    # draw walls
    for wall in map:
        editor_display.blit(wall_textures[wall[1]], (wall[0][0]*50, wall[0][1]*50))

    #draw sprites
    for sprite in sprites_map:
        editor_display.blit(sprites_textures[sprite[1]], (sprite[0][0]*50-25, sprite[0][1]*50-25))

    # draw player
    pygame.draw.circle(editor_display, (0,255,0), (player_spawn[0]*50, player_spawn[1]*50), 10)

    pygame.display.update()

    clock.tick(60)