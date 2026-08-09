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
        
    def show(self)-> int: 
        # wenn flag mode aktiviert ist int x y pos eingegeben wird dan 
        if self.is_revealed == True:
            if self.is_flaged == True:
                return 9
            elif self.is_bomb == False:
                return self.return_emoji_number()
            else: 
                return "💣"
        return "⬛️"

    def return_emoji_number(self):
        number_emojis = ["0️⃣ ","1️⃣ ", "2️⃣ ", "3️⃣ ", "4️⃣ ", "5️⃣ ", "6️⃣ ", "7️⃣ ", "8️⃣ "]
        return number_emojis[self.neighbour_mine_number]

    
    def get_neighbour_number(self,grid,xpos,ypos,area_leng)-> None:
        count = 0 
        if grid[xpos][ypos].is_bomb == True:
            return -1
        for row in range(3):
            for collum in range(3):
                nx = xpos - 1 + row
                ny = ypos - 1 + collum

                if 0 <= nx < area_leng and 0 <= ny < area_leng:
                    if grid[nx][ny].is_bomb:
                        count += 1

        self.neighbour_mine_number = count
        
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
        for i in range(area_leng):
             for j in range(area_leng):
                grid[i][j].get_neighbour_number(grid,i,j,area_leng) 
        winning_count = 0
        while True:
            for index in grid:
                print(*[block.show() for block in index], sep="")

            pos_is_possible = False
            while pos_is_possible == False:
                selectx = get_int_input("welche x pos")
                selecty = get_int_input("welche y pos")
                if (selectx >= 0 and selectx < area_leng
                    and selecty >=0 and selecty< area_leng):
                    pos_is_possible = True 
                else:
                    print("please enter a valid point")
            if grid[selecty][selectx].is_revealed == False:
                winning_count += 1
            grid[selecty][selectx].is_revealed = True
            pos_is_possible = False
            if grid[selecty][selectx].is_bomb == True:
                os.system('clear')
                print("du bist tot")
                break
            if winning_count >= (area_leng * area_leng) - number_of_bombs:
                os.system('clear')
                print("Du hast Gewonnen!")
                break
            else:
                os.system('clear')
main()