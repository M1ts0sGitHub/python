# Pomotime - Pomodoro Timer
import os ,shutil
import time
import pygame

zip_file = ['assets/files.zip', 'https://drive.usercontent.google.com/download?id=1whImOA9VjKZa9dd2s_AzzD2fKVU_yWrc']
hashes_file = ['assets/files.txt','https://drive.usercontent.google.com/download?id=1wSL1xmRfh6qtQkDLvcyixYIlAiW0F6jW']

def file_exists(file):
    path, filename = os.path.split(file)
    return os.path.exists(path) and os.path.exists(os.path.join(path, filename))

def file_integrity(file, hash):
    import hashlib
    if file_exists(file):
        with open(file, 'rb') as f:
            # print(f'expected:{hash}, actual: {hashlib.md5(f.read()).hexdigest()}')
            return hashlib.md5(f.read()).hexdigest() == hash
    return False

def delete_assets():
    if os.path.exists('assets'):
        shutil.rmtree('assets')

def download_assets():
    import requests
    # create folder assets if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
    r = requests.get(zip_file[1], allow_redirects=True)
    open(zip_file[0], 'wb').write(r.content)
    r = requests.get(hashes_file[1], allow_redirects=True)
    open(hashes_file[0], 'wb').write(r.content)

def extract_assets():
    import zipfile
    with zipfile.ZipFile('assets/files.zip', 'r') as zip_ref:
        zip_ref.extractall('assets')
    os.remove('assets/files.zip')

def programs_integrity():
    something_is_broken = False
    if not file_exists('assets/files.txt'):
        print('Some files of the program are not valid, will be deleted and re-downloaded')
        delete_assets()
        download_assets()
        extract_assets()
    else:
        # for each file of file files.txt check their integrity
        with open('assets/files.txt', 'r') as f:
            for line in f:
                file, hash = line.strip().split(',')
                if file_integrity(file, hash):
                    pass
                else:
                    something_is_broken = True
    if something_is_broken:
        # delete assets/files.txt
        os.remove('assets/files.txt')
        programs_integrity()
    else:
        print('All files of the program are valid. Program starts...')

class ReversedTimer:
    def __init__(self, focus_time, break_time):
        self.focus_timer_max = focus_time*60
        self.break_timer_max = break_time*60
        self.focus_timer = focus_time*60
        self.break_timer = break_time*60
        self.which_timer = 'focus_timer'
        self.state = 'paused'
    def reset(self):
        self.focus_timer = self.focus_timer_max
        self.break_timer = self.break_timer_max
        self.which_timer = 'focus_timer'
        self.state = 'paused'
    
    def start(self):
        if self.state == 'paused':
            self.state = 'running'
        else:
            self.state = 'paused'

    def update(self):
        if self.which_timer == 'focus_timer' and self.state == 'running':
            self.focus_timer -= 1
            return self.focus_timer
        elif self.which_timer == 'break_timer' and self.state == 'running':
            self.break_timer -= 1
            return self.break_timer
    def time_left(self):
        if self.which_timer == 'focus_timer':
            return self.focus_timer
        elif self.which_timer == 'break_timer':
            return self.break_timer
    
    def skip(self):
        self.focus_timer = self.focus_timer_max
        self.break_timer = self.break_timer_max
        self.state = 'paused'
        if self.which_timer == 'focus_timer':
            self.which_timer = 'break_timer'
        else:
            self.which_timer = 'focus_timer'

class button:
    def __init__(self, image1,image2):
        self.x, self.y = 0, 0
        self.button = 1
        self.image1 = pygame.image.load(image1)
        self.image2 = pygame.image.load(image2)
        self.width1, self.height1 = self.image1.get_width(), self.image1.get_height()
        self.width2, self.height2 = self.image2.get_width(), self.image2.get_height()

buttons = []
for theme in ['blue']: #, 'green', 'red']:
    b1 = button(f'assets/graphics/music_on_{theme}.png', f'assets/graphics/music_off_{theme}.png')
    b2 = button(f'assets/graphics/sounds_on_{theme}.png', f'assets/graphics/sounds_off_{theme}.png')
    b3 = button(f'assets/graphics/reset_{theme}.png', f'assets/graphics/reset_{theme}.png')
    b4 = button(f'assets/graphics/play_{theme}.png', f'assets/graphics/pause_{theme}.png')
    b5 = button(f'assets/graphics/skip_{theme}.png', f'assets/graphics/skip_{theme}.png')
    b6 = button(f'assets/graphics/settings_{theme}.png', f'assets/graphics/settings_{theme}.png')
    buttons.append([b1, b2, b3, b4, b5, b6])

class toolbar:
    def __init__(self, width, height, toolbars_buttons):
        self.width = width
        self.height = height
        self.toolbars_buttons = toolbars_buttons
        for i in range(len(self.toolbars_buttons)):
            self.toolbars_buttons[i].x = 1/6 * i * self.width + 1/12 * self.width
            self.toolbars_buttons[i].y = height - self.height / 2


def GUI():
    # Create the window
    # Intialize the pygame
    pygame.init()

    pomodoro_timer = ReversedTimer(25, 5)

    # create the screen
    width = 300
    height = 150
    screen = pygame.display.set_mode((width, height))

    # Caption and Icon
    pygame.display.set_caption("Pomotime")
    icon = pygame.image.load(r'./assets/graphics/icon.png')
    pygame.display.set_icon(icon)

    # Settings
    starting_time = time.time()
    # theme = 'blue'

    toolbar_object = toolbar(width, 240, buttons[0])

    # Game Loop
    running = True
    while running:
        screen.fill((88, 88, 188))

        # add a text to show 25:00 minutes with the font in /assets/fonts/jaro.ttf
        font = pygame.font.Font(os.path.join(r'assets\fonts\jaro.ttf'), 82)
        # convert reversed_timer to string
        text = str(int(pomodoro_timer.time_left() / 60)).zfill(2) + ':' + str(int(pomodoro_timer.time_left() % 60)).zfill(2)
        text = font.render(text, True, (0, 0, 0))
        screen.blit(text, (width // 2 - text.get_width() // 2, 0))
   
        for i in range(len(toolbar_object.toolbars_buttons)):
            if toolbar_object.toolbars_buttons[i].button == 1:
                toolbar_object.toolbars_buttons[i].image1_rect = toolbar_object.toolbars_buttons[i].image1.get_rect(center=(toolbar_object.toolbars_buttons[i].x, toolbar_object.toolbars_buttons[i].y))
                screen.blit(toolbar_object.toolbars_buttons[i].image1, toolbar_object.toolbars_buttons[i].image1_rect)
            else:
                toolbar_object.toolbars_buttons[i].image2_rect = toolbar_object.toolbars_buttons[i].image2.get_rect(center=(toolbar_object.toolbars_buttons[i].x, toolbar_object.toolbars_buttons[i].y))
                screen.blit(toolbar_object.toolbars_buttons[i].image2, toolbar_object.toolbars_buttons[i].image2_rect)


        if time.time() - starting_time > 1:
            pomodoro_timer.update()
            starting_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if text is clicked change the state of the timer between true or false
            if event.type == pygame.MOUSEBUTTONDOWN:
                if toolbar_object.toolbars_buttons[0].image1_rect.collidepoint(event.pos):
                    toolbar_object.toolbars_buttons[0].button = (toolbar_object.toolbars_buttons[0].button + 1) % 2
                elif toolbar_object.toolbars_buttons[1].image1_rect.collidepoint(event.pos):
                    toolbar_object.toolbars_buttons[1].button = (toolbar_object.toolbars_buttons[1].button + 1) % 2
                elif toolbar_object.toolbars_buttons[2].image1_rect.collidepoint(event.pos):
                    toolbar_object.toolbars_buttons[2].button = (toolbar_object.toolbars_buttons[2].button + 1) % 2
                    pomodoro_timer.reset()
                elif toolbar_object.toolbars_buttons[3].image1_rect.collidepoint(event.pos):
                    toolbar_object.toolbars_buttons[3].button = (toolbar_object.toolbars_buttons[3].button + 1) % 2
                    pomodoro_timer.start()
                elif toolbar_object.toolbars_buttons[4].image1_rect.collidepoint(event.pos):
                    toolbar_object.toolbars_buttons[4].button = (toolbar_object.toolbars_buttons[4].button + 1) % 2
                    pomodoro_timer.skip()
                    toolbar_object.toolbars_buttons[3].button = 1
                else:
                    toolbar_object.toolbars_buttons[5].button = (toolbar_object.toolbars_buttons[5].button + 1) % 2
                
                

        pygame.display.update()


    # quit the game and the python
    pygame.quit()

def __main__():
    programs_integrity()
    GUI()



__main__()