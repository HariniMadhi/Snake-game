import pygame, os, sys
from walls import Walls
from snake import Snake
from apple import Apple
from tkinter import Tk, Button
from constants import H, W, CELL_SIZE, SCORE_FONT, LARGE_FONT, TURQUOISE, BLACK, BLUE

os.environ['SDL_VIDEO_CENTERED'] = '1'  # center the window

pygame.init()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Snake')

walls_list = Walls.create_list(Walls(), CELL_SIZE)


def print_text(font, text, color, textpos=None):
    font = pygame.font.SysFont(font[0], font[1])
    text = font.render(text, 1, color)
    if textpos is None:
        textpos = text.get_rect(centerx=W / 2, centery=H / 2)
    screen.blit(text, textpos)

    
def draw_text():
    text = "Apples:{} Points: {} Lives: {} ".format(apple.count, hero.points, "-" * hero.lives)
    print_text(SCORE_FONT, text, TURQUOISE, (10, 10))

        
def write_file():
    
    file_name = "results.txt"
    try:
        f = open(file_name, "r")
        n = f.read().count(player_name) + 1  # how many the same names are already in file
        f.close()
    except FileNotFoundError:
        f = open(file_name, "w")
        f.close()
        n = 0

    f = open(file_name, "a")
    f.write("{} {} {} \n".format(player_name + str(n), apple.count, hero.points))
    f.close()


def draw_walls():
    for wall in walls_list:
        pygame.draw.rect(screen, pygame.Color("blue"), wall, 0)

    
def countdown():
    global start, seconds
    
    pygame.time.wait(1000)
    screen.fill(BLACK)
    print_text(LARGE_FONT, "{}".format(seconds), BLUE)
    seconds -= 1
    pygame.display.flip()


def ate_apple():
    head = hero.body[0]
    head_rect = pygame.Rect((head[0] * CELL_SIZE, head[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    return head_rect.colliderect(apple.rect)
           

def popup(msg):
    popupwin = Tk()  # popup window for asking name

    def center(win):   # center the popup window
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        # win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.geometry("+%d+%d" % (x, y))

    center(popupwin)

    def set_name(event = None):  # get the name from the input
        global player_name
        player_name = entry.get().strip()
        if not player_name:  # if the input is blank, default name is "Anonymous"
            player_name = 'Anonymous'
            
        popupwin.destroy()  # destroying window after accepting the name

    popupwin.title("!")
    label = Label(popupwin, text=msg, font=NORM_FONT)  # message, asking name
    label.pack(side="top", fill="x", pady=10)

    entry = Entry(popupwin, width=15)  # input for name
    entry.pack()
    entry.insert(0, 'Anonymous')  # default name
    entry.bind("<Return>", set_name)
    entry.focus_set()
    
    b1 = Button(popupwin, text="OKey", command=set_name)
    b1.pack()
    
    popupwin.mainloop()


hero = Snake(image)  # the snake

clock = pygame.time.Clock()  # for timing and snake's speed
apple = Apple(CELL_SIZE)  # an apple
start = False
game_over = False
seconds = 3  # seconds before start


def main():
    global start, game_over
    popup("Enter your name, please")

    hero.draw(screen)  # drawing snake
    apple.draw(screen)  # drawing apple
    draw_walls()  # drawing walls
    draw_text()  # showing walls

    while seconds > 0:
        countdown()  # countdown before game start
    start = True

    while True:  # main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not game_over:
                    write_file()  # write result (name, apples, points) to the file
                pygame.quit()
                sys.exit()
                break

            elif event.type == KEYDOWN:  # if key pressed we change snake's direction
                hero.set_direction(event.key)
            elif event.type == KEYUP:
                hero.speed = 10

if __name__ == "__main__":
    main()
