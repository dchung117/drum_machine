import os
import pygame
from pygame import mixer

# Initialize pygame module
pygame.init()

def draw_grid(clicked: list,
    active_beat: list,
    active_list: list):
    # left menu for sound selection
    left_box = pygame.draw.rect(surface=screen, color=gray, rect=pygame.Rect([0, 0, 200, HEIGHT-200]), width=5)

    # bottom menu for main controls (e.g. play, pause, save, load, etc.)
    bottom_box = pygame.draw.rect(surface=screen, color=gray, rect=pygame.Rect([0, HEIGHT-200, WIDTH, 200]), width=5)

    # Make grid
    boxes = []
    colors = [gray, white]

    # write hi-hat, snare, kick text, draw (blit) onto screen
    # todo: do we need to save these text objects? if not, let's move them into the "for i in range(instruments)..." loop
    hi_hat_text = label_font.render("Hi Hat", True, colors[int(active_list[0])])
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render("Snare", True, colors[int(active_list[1])])
    screen.blit(snare_text, (30, 130))
    kick_text = label_font.render("Kick", True, colors[int(active_list[2])])
    screen.blit(kick_text, (30, 230))
    crash_text = label_font.render("Crash", True, colors[int(active_list[3])])
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render("Clap", True, colors[int(active_list[4])])
    screen.blit(clap_text, (30, 430))
    floor_tom_text = label_font.render("Floor Tom", True, colors[int(active_list[5])])
    screen.blit(floor_tom_text, (30, 530))

    # Draw lines between each instrument
    for i in range(instruments):
        pygame.draw.line(screen, gray, start_pos=(0, i*100 + 100), end_pos=(200, i*100 + 100), width=3)

    # Create tile beats for each instrument (this is the grid)
    for i in range(beats):
        for j in range(instruments):
            # check if box is clicked
            if clicked[j][i]:
                if active_list[j]: # check if instrument is active
                    click_color=green
                else:
                    click_color=dark_gray
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

def draw_save_menu(beat_name: str,
    is_typing: bool):
    pygame.draw.rect(screen, black, rect=[0, 0, WIDTH, HEIGHT], width=0, border_radius=5)
    menu_text = label_font.render("SAVE MENU: Enter a name for current beat", True, white)
    screen.blit(menu_text, (400, 40))

    # entry button (i.e. box to type beat name)
    if is_typing:
        entry_color = dark_gray
        width = 5
    else:
        entry_color = gray
        width = 0
    entry_rect = pygame.draw.rect(screen, entry_color, rect=[400, 200, 600, 200], width=width, border_radius=5)
    entry_text = label_font.render(beat_name, True, white)
    screen.blit(entry_text, (430, 250))

    # save button
    save_btn = pygame.draw.rect(screen, gray, rect=[WIDTH//2 - 200, int(HEIGHT*0.75), 400, 100], width=0, border_radius=5)
    save_text = label_font.render("Save beat", True, white)
    screen.blit(save_text, (WIDTH//2 - 75, int(HEIGHT*0.75) + 30))

    # exit button
    exit_btn = pygame.draw.rect(screen, gray, rect=[WIDTH-200, HEIGHT-100, 180, 90], width=0, border_radius=5)
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH-160, HEIGHT-70))

    return entry_rect, save_btn, exit_btn

def draw_load_menu(idx: int):
    pygame.draw.rect(screen, black, rect=[0, 0, WIDTH, HEIGHT], width=0, border_radius=5)
    menu_text = label_font.render("LOAD MENU: Select beat to load", True, white)
    screen.blit(menu_text, (400, 40))

    # load button
    load_btn = pygame.draw.rect(screen, gray, rect=[WIDTH//2 - 200, int(HEIGHT*0.87), 400, 100], width=0, border_radius=5)
    load_text = label_font.render("Load beat", True, white)
    screen.blit(load_text, (WIDTH//2 - 75, int(HEIGHT*0.87) + 30))

    # delete btn
    delete_btn = pygame.draw.rect(screen, gray, rect=[WIDTH//2 - 500, int(HEIGHT*0.87), 200, 100], width=0, border_radius=5)
    delete_text = label_font.render("Delete beat", True, white)
    screen.blit(delete_text, (WIDTH//2 - 490, int(HEIGHT*0.87) + 25))

    # show all saved beats (only display 10)
    saved_beats_menu = pygame.draw.rect(screen, gray, rect=[190, 90, 1000, 600], width=5, border_radius=5)

    # draw rectangle around selected beat
    if 0 <= idx < len(saved_beats):
        pygame.draw.rect(screen, light_gray, rect=[190, 100+idx*50, 1000, 50], width=0, border_radius=5)

    # placeholders for num_beats, bpm, beats
    b_beats, b_bpm, b_clicked = None, None, None

    for b in range(len(saved_beats)):
        if b < 10:
            # Row text
            row_text = medium_font.render(f"{b+1}", True, white)
            screen.blit(row_text, (200, 100 + b*50))

            # beat name
            name_start_idx = saved_beats[b].index("name: ") + 6
            name_end_idx = saved_beats[b].index("beats: ") - 2
            b_name = saved_beats[b][name_start_idx:name_end_idx]
            name_text = medium_font.render(f"{b_name}", True, white)
            screen.blit(name_text, (240, 100 + b*50))

        # if beat is selected, get the info
        if 0 <= idx < len(saved_beats) and (b == idx):
            # num_beats
            num_beats_idx_end = saved_beats[b].index("bpm: ") - 2
            b_beats = int(saved_beats[b][name_end_idx+9:num_beats_idx_end])

            # bpm
            bpm_idx_end = saved_beats[b].index("selected: ") - 2
            b_bpm = int(saved_beats[b][num_beats_idx_end+7:bpm_idx_end])

            # beat clicks
            b_clicks_string = saved_beats[b][bpm_idx_end+14:-3]
            b_clicked = b_clicks_string.split("], [")
            b_clicked = [s.split(", ") for s in b_clicked]
            b_clicked = [[True if x == "True" else False for x in row] for row in b_clicked]

    # Make loaded info
    loaded_info = [b_beats, b_bpm, b_clicked]

    exit_btn = pygame.draw.rect(screen, gray, rect=[WIDTH-200, HEIGHT-100, 180, 90], width=0, border_radius=5)
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH-160, HEIGHT-70))

    return load_btn, delete_btn, saved_beats_menu, loaded_info, exit_btn

def play_notes(clicked: list,
    active_list: list):
    # loop through instruments
    for i in range(len(clicked)):
        # Check if the instrument is played on the active beat AND is active
        if clicked[i][active_beat] and active_list[i]:
            sound_list[i].play() # play the sound

# load in sounds
sounds_path = "sounds"
hi_hat = mixer.Sound(os.path.join(sounds_path, "hi hat.WAV"))
snare = mixer.Sound(os.path.join(sounds_path, "snare.WAV"))
kick = mixer.Sound(os.path.join(sounds_path, "kick.WAV"))
crash = mixer.Sound(os.path.join(sounds_path, "crash.WAV"))
clap = mixer.Sound(os.path.join(sounds_path, "clap.WAV"))
tom = mixer.Sound(os.path.join(sounds_path, "tom.WAV"))
sound_list = [hi_hat, snare, kick, crash, clap, tom]
pygame.mixer.set_num_channels(len(sound_list)*18) # ensure sounds that need multi-channels aren't cut off

# Set up app GUI
WIDTH = 1400
HEIGHT = 800

# colors (rgb)
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
light_gray = (170, 170, 170)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

# Create screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Beat Maker")

# Set up font
label_font = pygame.font.Font("freesansbold.ttf", 32)
medium_font = pygame.font.Font("freesansbold.ttf", 24)

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
save_menu = False # save menu
load_menu = False # load menu

# saved file
file = open("saved_beats.txt", "r")
saved_beats = []
for line in file:
    saved_beats.append(line)
beat_name = ""
is_typing = False
idx = 100

# active instruments
active_list = [True for _ in range(instruments)]
clicked = [[False for _ in range(beats)] for _ in range(instruments)]
if __name__ == "__main__":
    run = True
    while run:
        # Run code 60 fps
        timer.tick(FRAME_RATE)

        # Black background
        screen.fill(black)

        # Draw the grid
        boxes = draw_grid(clicked, active_beat, active_list)

        # draw lower menu buttons (play/pause)
        play_pause = pygame.draw.rect(screen, gray, rect=[50, HEIGHT - 150, 200, 100], width=0, border_radius=5)
        play_text = label_font.render("Play/Pause", True, white)
        screen.blit(play_text, [70, HEIGHT - 130])

        # Add bpm controls
        bpm_rect = pygame.draw.rect(screen, gray, rect=[300, HEIGHT - 150, 220, 100], width=5, border_radius=5)
        bpm_text = medium_font.render("Beats Per Minute", True, white)
        screen.blit(bpm_text, [308, HEIGHT - 130])
        bpm_text_2 = label_font.render(f"{bpm}", True, white)
        screen.blit(bpm_text_2, [370, HEIGHT - 100])

        bpm_add = pygame.draw.rect(screen, gray, rect=[525, HEIGHT-150, 48, 48], width=0, border_radius=5)
        bpm_sub = pygame.draw.rect(screen, gray, rect=[525, HEIGHT-100, 48, 48], width=0, border_radius=5)
        bpm_add_text = medium_font.render("+5", True, white)
        bpm_sub_text = medium_font.render("-5", True, white)
        screen.blit(bpm_add_text, [530, HEIGHT-140])
        screen.blit(bpm_sub_text, [530, HEIGHT-90])

        # handle number of beats
        beats_rect = pygame.draw.rect(screen, gray, rect=[600, HEIGHT - 150, 220, 100], width=5, border_radius=5)
        beats_text = medium_font.render("Beats In Loop", True, white)
        screen.blit(beats_text, [618, HEIGHT - 130])
        beats_text_2 = label_font.render(f"{beats}", True, white)
        screen.blit(beats_text_2, [680, HEIGHT - 100])

        beats_add = pygame.draw.rect(screen, gray, rect=[825, HEIGHT-150, 48, 48], width=0, border_radius=5)
        beats_sub = pygame.draw.rect(screen, gray, rect=[825, HEIGHT-100, 48, 48], width=0, border_radius=5)
        beats_add_text = medium_font.render("+1", True, white)
        beats_sub_text = medium_font.render("-1", True, white)
        screen.blit(beats_add_text, [830, HEIGHT-140])
        screen.blit(beats_sub_text, [830, HEIGHT-90])

        # instrument on/off controls
        instrument_rects = []
        for i in range(instruments):
            i_rect = pygame.rect.Rect((0, i*100), (200, 100))
            instrument_rects.append(i_rect)

        # save and load menus
        save_button = pygame.draw.rect(screen, gray, rect=[900, HEIGHT-150, 200, 48], width=0, border_radius=5)
        save_text = label_font.render("Save beat", True, white)
        load_button = pygame.draw.rect(screen, gray, rect=[900, HEIGHT-100, 200, 48], width=0, border_radius=5)
        load_text = label_font.render("Load beat", True, white)
        screen.blit(save_text, (920, HEIGHT-140))
        screen.blit(load_text, (920, HEIGHT-90))

        # clear board
        clear_button = pygame.draw.rect(screen, gray, rect=[1150, HEIGHT-150, 200, 100], width=0, border_radius=5)
        clear_text = label_font.render("Clear board", True, white)
        screen.blit(clear_text, (1160, HEIGHT-120))

        # modify text if playing
        if is_playing:
            play_text_2 = medium_font.render("Playing", True, dark_gray)
        else:
            play_text_2 = medium_font.render("Paused", True, dark_gray)
        screen.blit(play_text_2, [70, HEIGHT - 100])

        # draw save/load menu (if clicked)
        if save_menu:
            entry_button, save_button, exit_button = draw_save_menu(beat_name, is_typing)
        if load_menu:
            load_button, delete_button, saved_beats_menu, loaded_info, exit_button = draw_load_menu(idx)

        # play notes
        if beat_changed:
            play_notes(clicked, active_list)

        # get events from the queue (USER INPUTS)
        for event in pygame.event.get():
            # quit game - break out of loop
            if event.type == pygame.QUIT:
                run = False

            # check if any beats are clicked
            if event.type == pygame.MOUSEBUTTONDOWN and (not save_menu) and (not load_menu):
                # Loop through each beat box
                for i in range(len(boxes)):
                    # Get box indices if it was clicked on
                    if boxes[i][0].collidepoint(event.pos):
                        coords = boxes[i][1]

                        # Updated clicked list
                        clicked[coords[1]][coords[0]] = not clicked[coords[1]][coords[0]]

            # check if play/pause or number of bpm button was clicked (unless saving/loading) - update it
            if event.type == pygame.MOUSEBUTTONUP and (not save_menu) and (not load_menu):
                if play_pause.collidepoint(event.pos):
                    is_playing = not is_playing
                elif bpm_add.collidepoint(event.pos):
                    bpm += 5
                elif bpm_sub.collidepoint(event.pos):
                    bpm = max(0, bpm - 5)
                elif beats_add.collidepoint(event.pos):
                    beats += 1
                    for i in range(len(clicked)):
                        clicked[i].append(False)
                elif beats_sub.collidepoint(event.pos):
                    beats = max(1, beats - 1)
                    for i in range(len(clicked)):
                        clicked[i].pop(-1) # remove last beat from table
                elif clear_button.collidepoint(event.pos): # clear beats
                    clicked = [[False for _ in range(beats)] for _ in range(instruments)]
                elif save_button.collidepoint(event.pos): # save the current beat
                    save_menu = True
                elif load_button.collidepoint(event.pos): # load a saved beat
                    load_menu = True

                # check for instrument on/off command
                for i, i_rect in enumerate(instrument_rects):
                    if i_rect.collidepoint(event.pos):
                        active_list[i] = not active_list[i]
            elif event.type == pygame.MOUSEBUTTONUP and save_menu: # when save/load menu is active
                if exit_button.collidepoint(event.pos): # exit save/load menu
                    save_menu = False
                    load_menu = False
                    is_playing = True
                    beat_name = ""
                    is_typing = False
                elif entry_button.collidepoint(event.pos): # click the entry rectangle
                    if is_typing:
                        is_typing = False
                    elif not is_typing:
                        is_typing = True
                elif save_button.collidepoint(event.pos): # save the beat
                    with open("saved_beats.txt", "w") as f:
                        # Append data for new beat
                        saved_beats.append(f"name: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}\n")

                        # Save the updated beats
                        for b in saved_beats:
                            f.write(str(b))
                    save_menu = False
                    beat_name = ""
                    is_typing = False
            elif event.type == pygame.MOUSEBUTTONUP and load_menu:
                if saved_beats_menu.collidepoint(event.pos): # click the load rectangle
                    idx = (event.pos[1] - 100) // 50 # get the beat selected
                elif load_button.collidepoint(event.pos): # load selected beat
                    if 0 <= idx < len(saved_beats):
                        beats, bpm, clicked = loaded_info
                        load_menu = False
                elif delete_button.collidepoint(event.pos): # delete selected beat
                    if 0 <= idx < len(saved_beats):
                        saved_beats.pop(idx)
                elif exit_button.collidepoint(event.pos): # exit menu
                    save_menu = False
                    load_menu = False

            if event.type == pygame.TEXTINPUT and is_typing: # render typed text into entry rectangle
                beat_name += event.text
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and (len(beat_name) > 0) and is_typing: # backspace
                    beat_name = beat_name[:-1]

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
