import arcade
import random
import os
import math

screen_width = 800
screen_height = 800

blob_radius = 10
blob_colour = (0, 250, 0)

bomb_side_length = 3
bomb_colour = (255, 0, 0)

food_radius = 1
food_colour = (0, 255, 0)

blob_number = 10
bomb_number = 20
food_number = 10


class Blob:
    def __init__(self, radius, colour):

        self.initial_x_dir = random.randrange(-2, 2)
        self.initial_y_dir = random.randrange(-2, 2)
        self.radius = radius
        self.colour = colour
        self.health_bar_length = 18

        self.health_bar_length_list = []

        for i in range(10):
            self.health_bar_length_list.append(18)

        self.food_detection_radius = 2
        self.dna_blob = []

        self.id_blob = 0

        self.blob_positions = []
        self.blob_movement = []

        self.change_x = 0
        self.change_y = 0
    
    def get_colour(self, b_id, energy):
        colour_list = list(self.colour)
        i = self.blob_positions[:]
        print(i[b_id])

    def draw_health_bars(self, b_id, energy):
        i = self.blob_positions[:]
        self.health_bar_positions = []
        

    def random_pos(self):
        # Set random positions for blobs
        blob_id = 0
        
        for i in range(blob_number):
            blob_energy = 100
            blob_colour = (0, 255, 0)
            # Set random x and y values
            rand_x = random.randrange(1, screen_width-1)
            rand_y = random.randrange(1, screen_height-1)

            dx = random.randrange(-3, 4)
            dy = random.randrange(-3, 4)

            temp_pos = [rand_x, rand_y, blob_id, blob_energy, dx, dy, blob_colour]
            temp_move = [dx, dy]

            blob_id += 1

            self.blob_positions.append(temp_pos)
            self.blob_movement.append(temp_move)

            print("Blob Positions: ", self.blob_positions, "Blob Movement: ", self.blob_movement)

    def calc_energy(self, blob_index):
        i = self.blob_positions[blob_index]
        current_energy = i[3]
        new_energy = current_energy - math.sqrt((i[4]*i[4]) + (i[5]*i[5]))

        self.blob_positions[blob_index][3] = new_energy

        print("Blob ", i[2], " has energy: ", new_energy)

    def distance_from_food(self, food_positions):
        
        for i in self.blob_positions:
            #TempDNA = ID, Food detection radius
            temp_dna = []

            self.id_blob = i[2]
            temp_dna.append(self.id_blob)
            temp_dna.append(self.food_detection_radius)

            x_pos = i[0]
            y_pos = i[1]
            food_pos_index = 0
            for a in food_positions:

                if x_pos > a[0]-(blob_radius + self.food_detection_radius)\
                and x_pos < a[0]+(blob_radius + self.food_detection_radius)\
                and y_pos > a[1]-(blob_radius + self.food_detection_radius)\
                and y_pos < a[1]+(blob_radius + self.food_detection_radius):


                    del food_positions[food_pos_index] # Delete food from screen
                    self.calc_energy(self.id_blob)
                    print("NEAR FOOD")

                food_pos_index += 1


    def blob_initialise(self):
        self.random_pos()

    def kill_blob(self, b_id):
        self.blob_positions.pop(b_id)

    def lose_health(self, b_id, energy):
        self.draw_health_bars(b_id, energy)

    def move(self):
        new_blob_pos = []
        new_corr_blob_pos = []
        move_indexer = 0

        for i in self.blob_positions:
            self.x = i[0]
            self.y = i[1]

            delta_x = self.blob_movement[move_indexer][0]
            delta_y = self.blob_movement[move_indexer][1]
            lose_health_flag = False
            dead_flag = False
            # Check for collisions with walls
            if self.x < 0:
                delta_x *= -1
                self.x += delta_x
                self.blob_movement[move_indexer][0] *= -1
                #self.lose_health(i[2], i[3])
                lose_health_flag = True
                self.id_blob = i[2]
                #print("Blob ", self.id_blob, " collided with left wall.")
                if i[3] < 5:
                    self.kill_blob(i[2])
                    dead_flag = True
            if self.x > screen_width:
                delta_x *= -1
                self.x += delta_x
                self.blob_movement[move_indexer][0] *= -1
                #self.lose_health(i[2], i[3])
                lose_health_flag = True
                self.id_blob = i[2]
                #print("Blob ", self.id_blob, " collided with right wall.")
                if i[3] < 5:
                    self.kill_blob(i[2])
                    dead_flag = True
            if self.y < 0:
                delta_y *= -1
                self.y += delta_y
                self.blob_movement[move_indexer][1] *= -1
                #self.lose_health(i[2], i[3])
                lose_health_flag = True
                self.id_blob = i[2]
                #print("Blob ", self.id_blob, " collided with top wall.")
                if i[3] < 5:
                    self.kill_blob(i[2])
                    dead_flag = True
            if self.y > screen_height:
                delta_y *= -1
                self.y += delta_y
                self.blob_movement[move_indexer][1] *= -1
                #self.lose_health(i[2], i[3])
                lose_health_flag = True
                self.id_blob = i[2]
                #print("Blob ", self.id_blob, " collided with bottom wall.")
                if i[3] < 5:
                    self.kill_blob(i[2])
                    dead_flag = True
            else:
                self.x += delta_x
                self.y += delta_y 

            if not(dead_flag):
                temp_move_pos = [self.x, self.y, i[2], i[3], delta_x, delta_y, self.health_bar_length]
                
                new_blob_pos.append(temp_move_pos)
    
                self.blob_positions = new_blob_pos

                if lose_health_flag:
                    self.lose_health(i[2], i[3])
                    lose_health_flag = False

                temp_move_pos = [self.x, self.y, i[2], i[3], delta_x, delta_y, self.health_bar_length_list[move_indexer]]
                
                new_corr_blob_pos.append(temp_move_pos)
    
                self.blob_positions = new_corr_blob_pos

                self.calc_energy(i[2])
            
            dead_flag = False

            move_indexer += 1

    def draw(self):
        self.health_bar_positions = []
        for pos in self.blob_positions:
            arcade.draw_circle_filled(pos[0], pos[1], self.radius, self.colour)
            copy = pos[:]
            copy[1] += 17
            positions = copy[:2]
            self.health_bar_positions.append(positions)
            arcade.draw_rectangle_outline(copy[0], copy[1], self.radius*2, 5, (255, 255, 255))
            arcade.draw_rectangle_outline(copy[0], copy[1], copy[6], 3, (255, 0, 255))      
            

class Bomb:
    def __init__(self):
        self.initial_x_dir = random.randrange(-2, 2)
        self.initial_y_dir = random.randrange(-2, 2)
        self.length = bomb_side_length
        self.colour = bomb_colour

        self.bomb_positions = []
    
    def random_pos(self):
        # Set random positions for blobs
        for i in range(bomb_number):

            # Set random x and y values
            rand_x = random.randrange(1, screen_width-1)
            rand_y = random.randrange(1, screen_height-1)

            temp_pos = [rand_x, rand_y]
            self.bomb_positions.append(temp_pos)

    def draw(self):
        for pos in self.bomb_positions:
            arcade.draw_lrtb_rectangle_filled(pos[0], pos[0]+self.length, pos[1], pos[1]-self.length, self.colour)

class Food:
    def __init__(self):
        self.initial_x_dir = random.randrange(-2, 2)
        self.initial_y_dir = random.randrange(-2, 2)
        self.radius = food_radius
        self.colour = food_colour

        self.food_positions = []
    
    def random_pos(self):
        # Set random positions for blobs
        for i in range(food_number):

            # Set random x and y values
            rand_x = random.randrange(1, screen_width-1)
            rand_y = random.randrange(1, screen_height-1)

            temp_pos = [rand_x, rand_y]
            self.food_positions.append(temp_pos)

            #print("Food Positions: ", self.food_positions)

    def food_initialise(self):
        self.random_pos()

    def draw(self):
        for pos in self.food_positions:
            arcade.draw_circle_filled(pos[0], pos[1], self.radius, self.colour)

class Game(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)
        self.bl = Blob(blob_radius, blob_colour)
        self.bm = Bomb()
        self.fd = Food()

        self.bl.random_pos()
        self.bm.random_pos()
        self.fd.random_pos()

        self.score = 0

        self.set_mouse_visible(False)

        # Create sprite lists here and set them to None

    def setup(self):
        # Create sprites and Sprite lists here

        self.score = 0

        arcade.Sprite()

    def on_draw(self):
        # Render the screen

        # Start_Render() clears the screen to the background colour and erases the last frame. 
        arcade.start_render()

        self.bl.draw()
        self.bm.draw()
        self.fd.draw()

        # Call draw() on sprite lists below

    def update(self, dt):
        # All movement and game logic goes here. Update() is usually called on sprite lists that need it
        self.bl.move()
        
        self.bl.distance_from_food(self.fd.food_positions)
    
def main():
    game = Game(screen_width, screen_height)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()