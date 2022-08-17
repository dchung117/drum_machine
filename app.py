import pygame
from pygame import mixer

# Initialize pygame module
pygame.init()

def draw_grid():
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
            rect = pygame.draw.rect(surface=screen, color=gray, \
                rect=pygame.Rect([i*(WIDTH - 200) // beats + 200, j*100, (WIDTH - 200) // beats, (HEIGHT - 200)//instruments]), width=3, border_radius=5)
# Set up app GUI
WIDTH = 1400
HEIGHT = 800

# colors (rgb)
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# Create screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Beat Maker")

# Set up font
label_font = pygame.font.Font("freesansbold.ttf", 32)

FRAME_RATE = 60 # fps
timer =  pygame.time.Clock()
beats = 8
instruments = 6

if __name__ == "__main__":
    run = True
    while run:
        # Run code 60 fps
        timer.tick(FRAME_RATE)

        # Black background
        screen.fill(black)

        # Draw the grid
        draw_grid()

        # get events from the queue
        for event in pygame.event.get():
            # quit game - break out of loop
            if event.type == pygame.QUIT:
                run = False

        # Update changes to the display
        pygame.display.flip()

    # Uninitialize and quit pygame
    pygame.quit()
