"""@package docstring
Documentation for this module.
 
Obstacle class
Author: Dev^(enthusiases)
This class is responsible for maintaining several properties of the obstacle object
"""

##
# @file DisplayObstacle.py
# @brief This class is responsible for maintaining all obstacles that are displayed 

import pygame
import time
import Obstacle
import DetectCollision
from random import *
import math

class DisplayObstacle:
    TW_AMP = 100000
    TW_X_OFFSET = 799
    TW_Y_OFFSET = 90
    TW_FRQ = 1/100
    TW_SPEED = 0.3
    BEYOND_SCREEN = -100
    BASE_TIME = 1.5
    RANDOM_INTERVAL = 2.5

    ## @brief Constructor for DisplayObstacle
    #  @param game_window pygame.display
    def __init__(self, game_window):
        self.__game_screen = game_window
        self.__obstacle_list = pygame.sprite.Group()

    ## @brief get the list of obstacles
    #  @return the list of obstacles
    def get_obstacle_list(self):
        return self.__obstacle_list

    ## @brief remove a obstacle from the obstacle list
    #  @param obstacle obstacle type
    def remove_obstacle(self, obstacle):
        self.__obstacle_list.remove(obstacle)
    
    ## @brief drawing the obstacle onto the screen at a specific location
    #  @param current_x x position for obstacle to be drawn at
    #  @param current_y y position for obstacle to be drawn at
    #  @param obstacle Obstacle object
    def draw_obstacle(self,current_x, current_y, obstacle):
        obstacleImg = obstacle.get_img()
        
        # Scaling down the image to a fixed size
        #obstacleImg =  pygame.transform.scale(obstacleImg, (obstacle.get_width(), obstacle.get_height()))
        
        if (obstacle.get_name() == "Obstacle-4"):
            current_y = self.tumbleweed_math_func(current_x)
        obstacle.set_rect(current_x, current_y)
        #obstacle.set_img(obstacleImg)
        self.__game_screen.blit(obstacleImg, (current_x, current_y - obstacle.get_height())) #bug with rect 
        # TESTING PURPOSES: draw rectangle border
        #pygame.draw.rect(self.__game_screen, (255,0,0), obstacle.get_rect(), 2)

   
    ## @brief generate an obstacle from a random list of obstacles to be drawn on the screen (drawing them randomly at times
    #         from 3 and 5 seconds)
    #  @param obstacle_pos_x x position to draw obstacle on screen
    #  @param obstacle_pos_y y position to draw obstacle on screen
    #  @param obstacle_list list of obstacle objects
    #  @param prev_obstacle_spawn_time Keeping track of when the last obstacle was generated
    #  @param powerups_list list of powerups on the screen
    def generate_obstacle(self, obstacle_pos_x, obstacle_pos_y, obstacle_list, prev_obstacle_spawn_time, powerups_list):
        random_index = randint(0, len(obstacle_list) - 1)

        random_time = DisplayObstacle.BASE_TIME + (random() * DisplayObstacle.RANDOM_INTERVAL)

        current_time = time.time()
        # If the current time from when the last obstacle was spawned someone between 3 and 5 second
        if (current_time - prev_obstacle_spawn_time > random_time and current_time != prev_obstacle_spawn_time):
            selected_obstacle = obstacle_list[random_index]
            new_obstacle = Obstacle.Obstacle(selected_obstacle.get_name(), selected_obstacle.get_width(), selected_obstacle.get_height(), selected_obstacle.get_speed(), selected_obstacle.get_img())
            
            overlapping = DetectCollision.find_collision_powerups(new_obstacle, powerups_list)
            if not overlapping:
                self.__obstacle_list.add(new_obstacle)
                self.draw_obstacle(obstacle_pos_x, obstacle_pos_y, new_obstacle) 
                prev_obstacle_spawn_time = current_time 

            
            #print("Generated", (obstacle_list[random_index].get_name(), obstacle_list[random_index].get_speed()), "At:", obstacle_pos_x, obstacle_pos_y)
            #print( [(obstacle.get_name(), obstacle.get_speed()) for obstacle in self.get_obstacle_list()])
        return prev_obstacle_spawn_time
       
    ## @brief update all obstacle objects on the screen to be drawn to there new position. If an obstacle X position is less than
    #         -100 pixels, then remove the current obstacle from the obstacle list.
    def update_obstacle_display(self):
        #print([(obstacle.get_name(), obstacle.get_pos()) for obstacle in self.get_obstacle_list()])
        for obstacle in self.get_obstacle_list():
            
            obstacle_pos = obstacle.get_pos() #returns [x,y] 
            x = obstacle_pos[0]
            if obstacle.get_name() == "Obstacle-4":
                x -= DisplayObstacle.TW_SPEED * obstacle.get_speed()
            x -= obstacle.get_speed()

            y = obstacle_pos[1] # y position of obstacle doesn't change

            # updating the current position of the obstacle and drawing the obstacle at new position
            obstacle.set_rect(x, y)
            self.draw_obstacle(x, y, obstacle)

            
            # if obstacle is well beyond the screen window, then remove from obstacle_list
            if x < DisplayObstacle.BEYOND_SCREEN:
                self.remove_obstacle(obstacle)
                #self.__obstacleList.pop(0)
    
    def update_speed(self, speed):
        for element in self.__obstacle_list:
            element.set_speed(speed)

    ## @brief calculating the height calcuation (y-value) for the tumbleweed, similuating a tumble weed starting from a high point and being dropped and bouncing
    #  @param t current horizontal (x-value) of the tumbleweed obstacle
    #  @return the calculated height of the tumbleweed based on its current horizontal (x-value) position
    def tumbleweed_math_func(self, t):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        output = screen_height - DisplayObstacle.TW_AMP*math.fabs((t -  DisplayObstacle.TW_X_OFFSET)**
        (-1)*math.sin(DisplayObstacle.TW_FRQ*t)) - DisplayObstacle.TW_Y_OFFSET
        return output 




    
     
