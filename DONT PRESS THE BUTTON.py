from pygame import mixer
import pygame
from PIL import Image, ImageFilter
import threading
from time import sleep

pygame.init()
mixer.init()

win = pygame.display.set_mode((500, 500))

def load_image(image, position, blur=0, size=None, cropping=None):

    PIL_image = Image.open(image)

    if cropping:
        
        cropped_PIL_image = PIL_image.crop(cropping)
        cropped_blurred_PIL_image = cropped_PIL_image.filter(ImageFilter.GaussianBlur(radius=blur))
        PIL_image.paste(cropped_blurred_PIL_image, cropping)

    else:

        blurred_PIL_image = PIL_image.filter(ImageFilter.GaussianBlur(radius=blur))
        PIL_image = blurred_PIL_image

    mode = PIL_image.mode
    PIL_size = PIL_image.size
    data = PIL_image.tobytes()

    py_image = pygame.image.fromstring(data, PIL_size, mode)
        
    if size:

        R=[position[0], position[1], size[0], size[1]]

        return [pygame.transform.scale(py_image, (size)), R]

    else:

        R=[position[0], position[1], PIL_image.size[0], PIL_image.size[1]]

        return [py_image, R]

def make_image(image):

    win.blit(image[0], (image[1][0], image[1][1]))

def update_x():

    global run

    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
    		run = False

def update_button_sensory():

    global pressed
    global times_pressed
    global buttons
    global button_mode

    mpos = pygame.mouse.get_pos()
    if pygame.Rect(buttons[button_mode][1]).collidepoint(mpos) and can_press:
    
        if pygame.mouse.get_pressed()[0]:
            
            if not pressed:
                
                pressed=True
                button_mode=0
                mixer.music.load('doorbell.mp3')
                mixer.music.play()
                times_pressed += 1
                update_story()

        else:
            pressed=False
            button_mode=1
            
    else:
        pressed=False
        button_mode=1

def make_round():

    try:
        pygame.display.set_caption(story[times_pressed])

    except KeyError:
         pass
        
    update_x()
    win.fill((0, 0, 0))
    make_image(buttons[button_mode])
    
    if not can_press:
        if box_using==1:
            make_image(metal_box[corode_mode])
        elif box_using==0:
            make_image(box)

    if cloud_mode==1:
        make_image(cloud)
    elif cloud_mode==2:
        make_image(raining_cloud)

    if make_magnet:
        make_image(magnet)
        pygame.mouse.set_pos((60, 60))
            
    make_text(text, 250, 450, (255, 255, 255), (0, 0, 0), 50)
    pygame.display.update()

def update_story():

    global buttons
    global text
    global can_press
    global box_using
    global times_pressed
    global cloud_mode
    global corode_mode
    global make_magnet
    
    if True:

        try:
            pygame.display.set_caption(story[times_pressed])

        except KeyError:
            pass

        if times_pressed == 7:
            buttons[0][1] = [0, 0, 150, 150]
            buttons[1][1] = [0, 0, 150, 150]
            
        if times_pressed == 30:
            
            can_press=False
            box_using = 0

            make_round()
            
            input('pssst! want me to SMASH that box? enter if you agree. :D')
            print('shhhhhh dont tell him! ^-^')
            
            can_press=True
            times_pressed=31

            make_round()

        if times_pressed == 44:
            
            box_using=1
            can_press=False

            make_round()
            
            sleep(2.5)
            times_pressed=45
            make_round()
            sleep(2.5)
            times_pressed=46
            make_round()
            
            input('''hey. i cannot break that. but i can make a noise!
enter if you agree.''')
            
            mixer.music.load('crazylaugh.mp3')
            mixer.music.play()

            times_pressed = 47
            make_round()
            sleep(2.5)
            times_pressed=48
            make_round()
            sleep(2.5)
            times_pressed=49
            make_round()
            sleep(2.5)
            times_pressed=50
            cloud_mode=1
            make_round()
            sleep(2.5)
            times_pressed=51
            make_round()
            sleep(2.5)
            times_pressed=52
            make_round()

            print('the rain drops can corrode the lock!')
            sleep(2.5)
            input('''sing with me! rain rain~ come here so your raindrops can corrode the lock~~~''')

            cloud_mode=2
            make_round()

            sleep(1)

            corode_mode=1
            make_round()

            sleep(1)

            can_press=True
            cloud_mode=0
            make_round()

        if times_pressed == 28:

            buttons[0][1] = [175, 175, 150, 150]
            buttons[1][1] = [175, 175, 150, 150]

        if times_pressed==53:

            make_round()
            sleep(2.5)
            times_pressed = 54
            make_round()
            sleep(2.5)
            times_pressed=55
            make_magnet=True
            make_round()
            threading.Thread(target=talk, args=()).start()
            sleep(2.5)
            times_pressed=56
            make_round()

def talk():

    global make_magnet
    
    input('''let me disable it.
enter''')
    print('disabling...')
    sleep(7)
    print('done!')
    make_magnet=False
        
def make_text(letter, x, y, colour_1, colour_2, size):
    
    font = pygame.font.Font('freesansbold.ttf', size)
    
    text = font.render(letter, True, colour_1, colour_2)
    textR=text.get_rect()
    
    textR.center=(x,y)
    win.blit(text, textR)

times_pressed=0
pressed=False
run = True
can_press=True
corode_mode=0

text=''
buttons = [load_image('RED pressed.png', (175, 175), size=(150, 150)), load_image('RED not pressed.png', (175, 175), size=(150, 150))]

box_using=0
button_mode = 1
box = load_image('box.png', (175, 175), size=(151, 151))
metal_box = [load_image('metal box.png', (175, 175), size=(151, 151)), load_image('coroded metal box.png', (175, 175), size=(151, 151))]

cloud_mode=0
cloud = load_image('cloud.png', (25, 0),)
raining_cloud = load_image('raining cloud.png', (25, 0))
magnet=load_image('magnet.png', (0, 0), size=(80, 80))
make_magnet=False

story={0:'Don\'t press the button', 1:'umm i said dont press it', 2:'oh no', 3:'please. press the x button instead.', 4:'no , im not kidding!!', 5:'PLEASE! THAT NOISE IS ANNOYING!',
       6:'IM TRYING TO SLEEP!!!!!!', 7:'fine! i\'ll have to move it!', 8:'wha- HOW??', 9:'GRrrr!', 10:'FINE!', 11:'YOU CAN PRESS IT! at least i have a pillow to block the noise', 28:'GGRRRR',
       29:'ITS TOO LOUD!!!!!', 30:'HAH!', 31:'WHAT! WHAT! WHAT!!!', 34:'-_-', 39:'im getting used to it anyways.', 44:'NO IM NOTTT!!!!', 45:'ahhh. NOW i can sleep.', 46:'zzzZZZ...',
       47:'wha- wha?? what\'s that noise?', 48:'was it a monkey?? never mind. back to my sleep.', 49:'wait a second.', 50:'its about to rain!', 51:'like i care.', 52:'zzzZZZ...',
       53:'OH! WHAT NOW!!', 54:'aha! i got an idea!', 55:'there. that should keep you busy.', 56:'zzzZZZ...', 57:'>:|'}
update_story()

while run:
    
    update_button_sensory()
    
    make_round()
    
pygame.quit()
print(times_pressed)
