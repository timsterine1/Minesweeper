import os
os.system("clear")
import random

class Block:
    def __init__(self):
        self.is_revealed = False
        self.is_flaged = False
        self.shown = False
        self.is_bomb = False
        self.neighbour_mine_number = 0
        

    #nicht zeichnen sondern nur die zahl wiedergeben die gezeichnet werden soll
    def show(self)-> int: 
        # wenn flag mode aktiviert ist int x y pos eingegeben wird dan 
        if self.is_flaged == True:
            # dan wird das zeichenwas ausgegeben wird auf 9 gesetzt 
            return 9
        elif self.is_bomb == False:
            # dan wird das was ausgegeben wird mit einer function calculated
            # berechnet und ausgegeben 
            return self.get_neighbour_number()
            
        else: 
             # dann ist es eine bombe und game over 
             return -1

    
    def get_neighbour_number(self)-> int:
        #eis wird gegugt wieviele bombem im umkreis sind 
        #ein loop feur den 3x3 kasten
        #vll mit -2 anfangen fuer x und y weil beim ersten durchkauf
        #ist es dan -1 dan 0 und dan 1feur x und zusammen mit y
        # ist es dan ein 3er grud wenn eine bombe da ist den zaheker um 1 hoch am edne wiedergeben 

        return 0



def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
                print("please enter a number")

def main():
        area_leng = get_int_input("how large should the grid be? ")
        number_of_bombs = get_int_input("how many bombs do you want? ")
   
        grid = [[Block() for _ in range(area_leng)] for _ in range(area_leng)]
        
        def place_bombs():
            count = 1
            while count <= number_of_bombs:
                random_x = random.randint(0,area_leng-1)
                random_y = random.randint(0,area_leng-1)
                if grid[random_x][random_y].is_bomb == False:
                     grid[random_x][random_y].is_bomb = True
                     count += 1
        place_bombs()
        for index in grid:
                print([block.show() for block in index])

main()