import pygame
from pygame import mixer

# Initialize pygame module
pygame.init()

def draw_grid(clicked, active_beat):
    # left menu for sound selection
    left_box = pygame.draw.rect(surface=screen, color=gray, rect=pygame.Rect([0, 0, 200, HEIGHT-200]), width=5)

    # bottom menu for main controls (e.g. play, pause, save, load, etc.)
    bottom_box = pygame.draw.rect(surface=screen, color=gray, rect=pygame.Rect([0, HEIGHT-200, WIDTH, 200]), width=5)

    # Make grid
    boxes = []
    colors = [gray, white, white]

    # write hi-hat, snare, kick text, draw (blit) onto screen
    # todo: do we need to save these text objects? if not, let's move them into the "for i in range(instruments)..." loop
    hi_hat_text = label_font.render("Hi Hat", True, white)
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render("Snare", True, white)
    screen.blit(snare_text, (30, 130))
    kick_text = label_font.render("Kick", True, white)
    screen.blit(kick_text, (30, 230))
    crash_text = label_font.render("Crash", True, white)
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render("Clap", True, white)
    screen.blit(clap_text, (30, 430))
    floor_tom_text = label_font.render("Floor Tom", True, white)
    screen.blit(floor_tom_text, (30, 530))

    # Draw lines between each instrument
    for i in range(instruments):
        pygame.draw.line(screen, gray, start_pos=(0, i*100 + 100), end_pos=(200, i*100 + 100), width=3)

    # Create tile beats for each instrument (this is the grid)
    for i in range(beats):
        for j in range(instruments):
            # check if box is clicked
            if clicked[j][i]:
                click_color=green
            else:
                click_color=gray

            # color the rectangle w/ clicked
            rect = pygame.draw.rect(surface=screen, color=click_color, \
                rect=pygame.Rect([i*(WIDTH - 200) // beats + 205, j*100 + 5, (WIDTH - 200) // beats - 10, (HEIGHT - 200)//instruments - 10]), width=0, border_radius=3)

            # add gold frame
            pygame.draw.rect(surface=screen, color=gold, \
                rect=pygame.Rect([i*(WIDTH - 200) // beats + 200, j*100, (WIDTH - 200) // beats, (HEIGHT - 200)//instruments]), width=5, border_radius=5)

            # rectangle outline
            pygame.draw.rect(surface=screen, color=black, \
                rect=pygame.Rect([i*(WIDTH - 200) // beats + 200, j*100, (WIDTH - 200) // beats, (HEIGHT - 200)//instruments]), width=2, border_radius=5)
            # Store the rectangle object and the beat/instrument idx
            boxes.append((rect, (i, j)))


    # Draw current beat in loop
    active = pygame.draw.rect(screen, blue, rect=[active_beat*(WIDTH - 200) // beats + 200, 0, (WIDTH - 200)//beats, instruments*100],
        width=5, border_radius=3)

    return boxes

# Set up app GUI
WIDTH = 1400
HEIGHT = 800

# colors (rgb)
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

# Create screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Beat Maker")

# Set up font
label_font = pygame.font.Font("freesansbold.ttf", 32)

FRAME_RATE = 60 # fps
timer =  pygame.time.Clock()

# beat boxes
beats = 8
instruments = 6
boxes = []

# beats per minute
bpm = 240
is_playing = True
active_length = 0 # length of current beat
active_beat = 0 # current beat (e.g. 1 to 8 inclusive)
beat_changed = True # flag noting if beat changed

clicked = [[False for _ in range(beats)] for _ in range(instruments)]
if __name__ == "__main__":
    run = True
    while run:
        # Run code 60 fps
        timer.tick(FRAME_RATE)

        # Black background
        screen.fill(black)

        # Draw the grid
        boxes = draw_grid(clicked, active_beat)

        # get events from the queue (USER INPUTS)
        for event in pygame.event.get():
            # quit game - break out of loop
            if event.type == pygame.QUIT:
                run = False

            # check if any beats are clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Loop through each beat box
                for i in range(len(boxes)):
                    # Get box indices if it was clicked on
                    if boxes[i][0].collidepoint(event.pos):
                        coords = boxes[i][1]

                        # Updated clicked list
                        clicked[coords[1]][coords[0]] = not clicked[coords[1]][coords[0]]

        # BEAT TRACKING
        # Create beat length (i.e. how long each beat should play for) (minutes)
        beat_length = 3600 // bpm # 60 fps * 60 s/min = 3600 frames per min

        if is_playing:
            if active_length < beat_length: # add 1 to active_length
                active_length += 1
            else: # reset active length
                active_length = 0
                if active_beat < beats - 1:
                    # change beat
                    active_beat += 1
                    beat_changed = True
                else: # reset beat to first
                    active_beat = 0
                    beat_changed = True

        # Update changes to the display
        pygame.display.flip()

    # Uninitialize and quit pygame
    pygame.quit()
