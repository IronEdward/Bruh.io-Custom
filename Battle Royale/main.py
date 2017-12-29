import pygame, random, math, sys, time
from pygame.locals import *
from classes import *

pygame.init()

arena_width, arena_height = (10000, 5000)
screen_width, screen_height = (1000,500)
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Battle Royale")

fps = pygame.time.Clock()

#Variables
spawn_border = 200
end = False
item_list = ["rifle","shotgun","submachine_gun","hp_s","hp_m","hp_l"]
player_count = 10
player_positions = list()
item_max = 10
bot_shoot_buffer = 500
player_border_width = 1
block_size = 100
block_count = 2000
maze = []
maze_loop_y_count_buffer = int(screen_height/block_size)
maze_loop_x_count_buffer = int(screen_width/block_size)
arena_border_thickness = 50

#Player 1-specific parameters:
x_speed = 0
y_speed = 0

#Name list generator:
names = list()
with open("names") as name_file:
    for line in name_file:
        names.append(line.split()[0])

#Functions
def item_generator():               #Generate items on the map
    items_on_map.append((item_list[random.randint(0,len(item_list)-1)], random.randint(spawn_border, arena_width - spawn_border), random.randint(spawn_border, arena_height - spawn_border)))
def degree_to_radian(degrees):      #Degrees -> Radians
    return (degrees * math.pi)/180
def initialization():               #Variable initialization
    global player_list, items_on_map, winner
    player_list = list()
    items_on_map = list()
    winner = ""
def name_generator():
    return names[random.randint(0, 39)]
def maze_generator():               #Generate map
    global maze, arena_width, arena_height, block_size
    for i in range(block_count):
        (block_x, block_y) = (random.randint(0, (arena_width/block_size)-1), random.randint(0, (arena_height/block_size)-1))
        if (block_x, block_y) not in maze:
            maze.append((block_x, block_y))

def draw(state, winner):            #Blit to screen
    screen.fill((255,255,255))
    screen_edge = [(player_list[0].x - screen_width/2), (player_list[0].y - screen_height/2)]                               #Edge of player 1's screen
    #Draw broder:
    pygame.draw.rect(screen, black, (-(screen_edge[0]+arena_border_thickness), -(screen_edge[1]+arena_border_thickness), arena_border_thickness, arena_height + arena_border_thickness))
    pygame.draw.rect(screen, black, (-screen_edge[0], -(screen_edge[1]+arena_border_thickness), arena_width+arena_border_thickness, arena_border_thickness))
    pygame.draw.rect(screen, black, (arena_width-screen_edge[0], -screen_edge[1], arena_border_thickness, arena_height + arena_border_thickness))
    pygame.draw.rect(screen, black, (-(screen_edge[0]+arena_border_thickness), arena_height-screen_edge[1], arena_width+arena_border_thickness, arena_border_thickness))

    #Draw Maze:
    blit_buf = [screen_edge[0] - int(screen_edge[0]/block_size)*100, screen_edge[1] - int(screen_edge[1]/block_size)*100]   #Buffer that stores important values for blitting. 
    for y_buf in range(maze_loop_y_count_buffer+1):
        for x_buf in range(maze_loop_x_count_buffer+1):
            #print(int(screen_edge[0]/block_size) + x_buf)
            if (int(screen_edge[0]/block_size) + x_buf, int(screen_edge[1]/block_size) + y_buf) in maze:
                pygame.draw.rect(screen, blue, (x_buf*block_size-blit_buf[0], y_buf*block_size-blit_buf[1], block_size, block_size))
    
    #Draw player 1:
    pygame.draw.circle(screen, player_list[0].color, (int(screen_width/2), int(screen_height/2)), player_list[0].size, 0)
    for index, i in enumerate(player_list[1:]):    #Blit players
        if player_positions[0][0] - screen_width/2 <= player_positions[index][0] <= player_positions[0][0] + screen_width/2 and player_positions[0][1] - screen_height/2 <= player_positions[index][1] <= player_positions[0][1] + screen_height/2:
            pygame.draw.circle(screen, i.color, (int(screen_width/2+player_positions[index][0]-player_positions[0][0]), int(screen_height/2+player_positions[index][1]-player_positions[0][1])), i.size, 0)
    for i in items_on_map:          #Blit items
        if player_positions[0][0] - screen_width/2 <= i[1] <= player_positions[0][0] + screen_width/2 and player_positions[0][1] - screen_height/2 <= i[2] <= player_positions[0][1] + screen_height/2:
            if i[0] == "rifle":
                pygame.draw.circle(screen, (0,0,0), (int(screen_width/2+i[1]-player_positions[0][0]), int(screen_height/2+i[2]-player_positions[0][1])), 10, 5)
            elif i[0] == "shotgun":
                pygame.draw.circle(screen, (0,0,0), (int(screen_width/2+i[1]-player_positions[0][0]), int(screen_height/2+i[2]-player_positions[0][1])), 10, 5)
            elif i[0] == "submachine_gun":
                pygame.draw.circle(screen, (0,0,0), (int(screen_width/2+i[1]-player_positions[0][0]), int(screen_height/2+i[2]-player_positions[0][1])), 10, 5)
            elif i[0] == "hp_s":
                pygame.draw.circle(screen, (0,0,0), (int(screen_width/2+i[1]-player_positions[0][0]), int(screen_height/2+i[2]-player_positions[0][1])), 10, 5)
            elif i[0] == "hp_m":
                pygame.draw.circle(screen, (0,0,0), (int(screen_width/2+i[1]-player_positions[0][0]), int(screen_height/2+i[2]-player_positions[0][1])), 10, 5)
            else:
                pygame.draw.circle(screen, (0,0,0), (int(screen_width/2+i[1]-player_positions[0][0]), int(screen_height/2+i[2]-player_positions[0][1])), 10, 5)

    for ind, i in enumerate(player_list):
        if i.bullet_fire == True:
            if player_positions[0][0] - screen_width/2 <= i.bullet_pos[0] <= player_positions[0][0] + screen_width/2 and player_positions[0][1] - screen_height/2 <= i.bullet_pos[1] <= player_positions[0][1] + screen_height/2:
                if (int(i.bullet_pos[0]/block_size), int(i.bullet_pos[1]/block_size)) in maze and int(i.bullet_pos[0]/block_size)*block_size <= i.bullet_pos[0] <= int(i.bullet_pos[0]/block_size)*block_size+block_size and \
                int(i.bullet_pos[1]/block_size)*block_size <= i.bullet_pos[1] <= int(i.bullet_pos[1]/block_size)*block_size+block_size or i.bullet_pos[0] < 0 or i.bullet_pos[0] > arena_width or i.bullet_pos[1] < 0 or i.bullet_pos[1] > arena_height:
                    i.bullet_fire = False
                    i.bullet_pos = [None, None]
                    i.bullet_decay = i.gun.decay

                else:
                    pygame.draw.circle(screen, (0,0,0), (int(screen_width/2+i.bullet_pos[0]-player_positions[0][0]), int(screen_height/2+i.bullet_pos[1]-player_positions[0][1])), i.gun.bullet_size)
    pygame.display.update()
    fps.tick(60)

#Dependent Classes
class Player:
    def __init__(self):
        self.x = random.randint(spawn_border,arena_width - spawn_border)
        self.y = random.randint(spawn_border,arena_height - spawn_border)
        while (int(self.x/block_size), int(self.y/block_size)) in maze:
            self.x = random.randint(spawn_border,arena_width - spawn_border)
            self.y = random.randint(spawn_border,arena_height - spawn_border)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.name = name_generator()
        self.size = 10
        self.speed = 5                  #Walking speed
        self.health = 100               #Initial Health
        self.bullet_fire = False        #Bullet boolean
        self.bullet_vel = list()        #Bullet velocity (0, 0 if not fired)
        self.bullet_pos = list()  #Bullet position
        self.gun = Gun.pistol()         #Gun type. Everybody starts with a pistol
        self.bullet_decay = self.gun.decay
        self.bullet_size = self.gun.bullet_size

    def shoot(self, angle):
        if self.bullet_fire == False:   #If no bullet present:
            self.bullet_fire = True
            self.bullet_pos = [self.x, self.y]
            self.bullet_vel[0] = int(self.gun.speed * math.sin(degree_to_radian(angle)))
            self.bullet_vel[1] = int(self.gun.speed * math.cos(degree_to_radian(angle)))

    def move(self, direction_x, direction_y):
        old_x = self.x; old_y = self.y
        if direction_y == 1:              #Up
            self.y -= self.speed
        elif direction_y == 2:            #Down
            self.y += self.speed
        if direction_x == 1:              #Right
            self.x += self.speed
        elif direction_x == 2:            #Left
            self.x -= self.speed
        #Collision checker
        if (int(self.x/block_size), int(self.y/block_size)) in maze:
            if int(self.x/block_size)*block_size <= self.x + self.size:
                self.x = old_x#int(self.x/block_size)*block_size - self.size
            elif self.x - self.size <= int(self.x/block_size)*block_size+block_size:
                self.x = old_x#int(self.x/block_size)*block_size+block_size + self.size

            if int(self.y/block_size)*block_size <= self.y + self.size:
                self.y = old_y#int(self.y/block_size)*block_size - self.size
            elif self.y - self.size <= int(self.y/block_size)*block_size+block_size:
                self.y = old_y#int(self.y/block_size)*block_size+block_size + self.size

        if self.x - self.size <= 0:
            self.x = self.size
        elif self.x + self.size >= arena_width:
            self.x = arena_width - self.size
        if self.y - self.size <= 0:
            self.y = self.size
        elif self.y + self.size >= arena_height:
            self.y = arena_height - self.size

        #Item pickup processing:
        for i in items_on_map:
            if self.x - self.size <= i[1] <= self.x + self.size and self.y - self.size <= i[2] <= self.y + self.size:
                if "hp" in i[0]:
                    if i[0] == "hp_s":
                        self.health += Item.health_small.hp
                    elif i[0] == "hp_m":
                        self.health += Item.health_med.hp
                    elif i[0] == "hp_l":
                        self.health += Item.health_big.hp
                else:
                    if i[0] == "rifle":
                        self.gun = Gun.rifle()
                    elif i[0] == "submachine_gun":
                        self.gun = Gun.submachine_gun()
                    elif i[0] == "shotgun":
                        self.gun = Gun.shotgun()
                    self.bullet_decay = self.gun.decay
                items_on_map.remove(i)
    
    def action(self, angle, direction):
        #Gun action processing:
        if angle != -1 and bullet_fire == False:
            self.shoot(angle)
            self.bullet_pos[0] += self.bullet_vel[0]
            self.bullet_pos[1] += self.bullet_vel[1]
        if self.bullet_fire == True:
            if self.bullet_decay <= 0:
                self.bullet_decay = self.gun.decay
                self.bullet_fire = False 
            else:
                self.bullet_pos[0] += self.bullet_vel[0]
                self.bullet_pos[1] += self.bullet_vel[1]
                self.bullet_decay -= Gun.decay_rate

        #Movement processing:
        move(direction)

#Gameplay Loop:
while end == False:
    #Spawn characters: 
    initialization()
    maze_generator()
    #Make the players(index 0 is player 1):
    for i in range(player_count):
        player_list.append(Player())
    #Insert player positions:
    for i in player_list:
        player_positions.append([i.x, i.y])
    terminal = False
    while terminal == False:
        #Spawn items randomly if the item count is lower than the defined variable
        if len(items_on_map) < item_max and random.randint(0, 100) == 1:
            item_generator()
        for e in pygame.event.get():
            #Player 1 Movement:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    y_speed = 1
                elif e.key == pygame.K_s:
                    y_speed = 2
                
                if e.key == pygame.K_a:
                    x_speed = 2
                elif e.key == pygame.K_d:
                    x_speed = 1
            elif e.type == pygame.KEYUP:
                if e.key in (K_w, K_s):
                    y_speed = 0
                elif e.key in (K_a, K_d):
                    x_speed = 0
            #Player 1 Shooting:
            if e.type == pygame.MOUSEBUTTONUP:      #If it's MOUSEBUTTONDOWN, the bullets would get fired rapidly nonstop.
                """This was originally supposed to use the function in the "Player" class, but it doesn't yet. """
                """--------------------------------------------------------------------------------------------"""
                #Process mouse position:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()
                mouse_x -= screen_width / 2
                mouse_y -= screen_height / 2
                #Get bigger value:
                if abs(mouse_x) > abs(mouse_y):
                    divider = abs(mouse_x)
                else:
                    divider = abs(mouse_y)
                #Calculate bullet velocity:
                vel_x = mouse_x * player_list[0].gun.speed / divider
                vel_y = mouse_y * player_list[0].gun.speed / divider
                """--------------------------------------------------------------------------------------------"""
                #Bullet Processes:
                player_list[0].bullet_fire = True
                player_list[0].bullet_vel = [vel_x, vel_y]
                player_list[0].bullet_pos = [player_list[0].x, player_list[0].y]
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        player_list[0].move(x_speed, y_speed)       #Move player and item collision
        if player_list[0].bullet_fire == True:
            player_list[0].bullet_pos[0] += player_list[0].bullet_vel[0]
            player_list[0].bullet_pos[1] += player_list[0].bullet_vel[1]
            player_list[0].bullet_decay -= Gun.decay_rate
            if player_list[0].bullet_decay <= 0:
                player_list[0].bullet_fire = False
                player_list[0].bullet_pos = [None, None]
                player_list[0].bullet_decay = player_list[0].gun.decay
        #Other player actions
        for index, i in enumerate(player_list[1:]):       #First loop
            for index2, j in enumerate(player_list):
                if i != j:
                    #Check if i's bullet has hitten j:
                    if i.bullet_fire == True:
                        #Check bullet coordinates:
                        i.bullet_pos[0] += i.bullet_vel[0]
                        i.bullet_pos[1] += i.bullet_vel[1]
                        i.bullet_decay -= Gun.decay_rate
                        if j.x - j.size/2 <=  i.bullet_pos[0] <= j.x + j.size/2 and j.y - j.size/2 <=  i.bullet_pos[1] <= j.y + j.size/2:
                            j.health -= i.gun.force     #Subtract health from 2nd player
                            i.bullet_fire = False       #Change bullet boolean
                            player_list[index2] = j     #Update 2nd player
                            if j.health <= 0:           #If the player died:
                                player_list.remove(j)   #Remove from list
                                player_positions.remove(player_positions[index2])
                        if i.bullet_decay <= 0:
                            i.bullet_fire = False
                            i.bullet_pos = [None, None]
                            i.bullet_decay = i.gun.decay
                    #If said player is in shooting range:
                    if i.x - bot_shoot_buffer <= j.x <= i.x + bot_shoot_buffer and i.y - bot_shoot_buffer <= j.y <= i.y + bot_shoot_buffer and i.bullet_fire == False:
                        x_dist = i.x - j.x
                        y_dist = i.y - j.y
                        #Get bigger value:
                        if abs(x_dist) > abs(y_dist):
                            divider = abs(x_dist)
                        else:
                            divider = abs(y_dist)
                        #Calculate bullet velocity:
                        vel_x = x_dist * i.gun.speed / divider
                        vel_y = y_dist * i.gun.speed / divider
                        i.bullet_fire = True
                        i.bullet_vel = [vel_x, vel_y]
                        i.bullet_pos = [i.x, i.y]
                    #If not, just move around in a direction
                    else:
                        #Move player and Process item collision:
                        i.move(random.randint(1, 2), random.randint(1, 2))
                    player_list[index + 1] = i
        #Update player_positions[] to the current positions:
        for index, i in enumerate(player_list):
            player_positions[index] = [i.x, i.y]
        if len(player_list) == 1:
            terminal = True
            winner = player_list[0].name
        draw(terminal, winner)