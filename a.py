# move an <strong class="highlight">image</strong> rectangle to follow the <strong class="highlight">mouse</strong> <strong class="highlight">click</strong> position

import pygame as pg

# initialize <strong class="highlight">pygame</strong>
pg.init()

# use an <strong class="highlight">image</strong> you have (.bmp  .jpg  .png  .gif)
image_file = "activity-bridge.png"

# RGB color tuple for screen background
black = (0,0,0)

# screen width and height
sw = 640
sh = 480
# create a screen
screen = pg.display.set_mode((sw, sh))
# give the screen a title
pg.display.set_caption('image follows mouse click position')

# load an <strong class="highlight">image</strong>
# convert() unifies the pixel format for faster blit
image = pg.image.load(image_file).convert()
# get the rectangle the <strong class="highlight">image</strong> occupies
# rec(x, y, w, h)
start_rect = image.get_rect()
image_rect = start_rect

running = True
while running:
    event = pg.event.poll()
    keyinput = pg.key.get_pressed()
    # exit on corner 'x' <strong class="highlight">click</strong> or escape key press
    if keyinput[pg.K_ESCAPE]:
        raise SystemExit
    elif event.type == pg.QUIT:
        running = False
    elif event.type == pg.MOUSEBUTTONDOWN:
        print event.pos
        print start_rect.collidepoint(event.pos)
        #image_rect = start_rect.move(event.pos)

    # this erases the old sreen with black
    screen.fill(black)
    # put the <strong class="highlight">image</strong> on the screen
    screen.blit(image, image_rect)
    # update screen
    pg.display.flip()