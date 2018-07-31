#!/usr/bin/env python

#   Outside libraries
import pygame

#   Python libraries
import time

class SpriteSheet(object):
    """ Sprite sheet object for pygame. """

    def __init__(self, img_path, sheet_size, frame_num):
        """ Initializes the spritesheet object. Takes the following arguments:

        img_path (str): relative file path for sprite sheet image
        sheet_size (tuple): two items (r, c) for the number of rows and columns
            in the sprite sheet
        frame_num (int): number of frames in the sprite sheet. """

        #   Save input arguments as attributes
        self.img_path = img_path
        self.x_size, self.y_size = sheet_size
        self.frame_num = frame_num

        #   Optional parameters
        self.reverse_x = False
        self.reverse_y = False
        self.reversed_animation = False
        self.repeat = True

        #   Read the image path
        self.load_image_file()
        self.split()


    def load_image_file(self):
        """ Reads the sprite sheet image file and computes dimensions """

        #   Load the image from path as a pygame surface
        self.sheet_img = pygame.image.load(self.img_path)

        #   Determine surface width and height
        self.sheet_height = self.sheet_img.get_height()
        self.sheet_width = self.sheet_img.get_width()


    def split(self):
        """ Breaks up the source image into a list of frames """

        #   Determine frame size, in pixels
        frame_height = int(self.sheet_height / self.y_size)
        frame_width = int(self.sheet_width / self.x_size)

        #   Make an empty list to store frames in
        self.frames = []

        #   Repeat for each frame in animation
        for idx in range(self.frame_num):

            #   Initialize a surface object for the frame
            frame = pygame.Surface((frame_width, frame_height))
            trans_color = (254, 0, 0)
            frame.fill(trans_color)
            frame.set_colorkey(trans_color)

            #   Crop the frame number into a pygame surface
            x_origin, y_origin = self.get_frame_position(idx)
            frame.blit(self.sheet_img, (-x_origin, -y_origin))

            #   Add frame to list
            self.frames.append(frame)


    def reverse(self, xbool, ybool):
        """ Reverses the frames of the animation based on which booleans are
        True. """

        #   Flip each frame
        for idx, frame in enumerate(self.frames):
            self.frames[idx] = pygame.transform.flip(frame, xbool, ybool)


    def get_frame_position(self, n):
        """ Gets the position of the top left corner of frame n, in pixels,
        based on the source image. """

        #   Calculate the x position of the frame
        x_origin_int = n % self.x_size  #   Column number of frame
        x_origin_prop = 1.0*x_origin_int / self.x_size  #   Prop from left
        x_origin = x_origin_prop * self.sheet_width     #   X position

        #   Calculate the y position of the frame
        y_origin_int = n % self.y_size  #   Row number of frame
        y_origin_prop = 1.0*y_origin_int / self.y_size  #   Prop from top
        y_origin = y_origin_prop * self.sheet_height    #   Y position

        return (x_origin, y_origin)


    def get_frame(self, n):
        """ Returns the frame surface based on an index. Overflow wraps when
        repeat is true, otherwise it returns the last frame of the animation."""

        if self.repeat:
            return self.frames[n % self.frame_num]
        else:
            return self.frames[min(n, self.frame_num - 1)]


class Sprite(object):
    """ Object for rendering a game sprite onto a screen, using pygame. """

    def __init__(self, fps = 12):
        """ Initialization method for sprite object. """

        #   Initialize animations dictionary
        self.animations = {}

        #   Set initial flags and values
        self.x_pos = 0
        self.y_pos = 0
        self.paused = False
        self.active_animation = None

        #   Set frames per second
        self.fps = fps


    def start_animation(self, name):
        """ Starts the animation of the chosen name. """

        #   Unpause animatino if paused
        self.paused = False

        #   Remember when this animation was selected
        self.last_start = time.time()

        #   Change active animation
        self.active_animation = name


    def draw(self, surf):
        """ Draws the current frame onto a surface. """

        #   Raise an error if the active animation isn't in animations
        if not self.active_animation in self.animations:
            print("The active animation %s couldn't be found." % \
                self.active_animation)
            raise

        #   Load up the active spritesheet
        active_spritesheet = self.animations[self.active_animation]

        #   Determine what frame of the animation you should be on
        now = time.time()
        elapsed = now - self.last_start
        frame_time = 1.0/self.fps
        frames_count = int(elapsed/frame_time)

        #   Draw the animation on the surface
        frame_to_draw = active_spritesheet.get_frame(frames_count)
        surf.blit(frame_to_draw, (int(self.x_pos), int(self.y_pos)))


    def add_animation(self, anim_dict):
        """ Adds one or more animations to the sprite's animation dictionary.
        Parameter should have strings as keys and pyrate spritesheet objects
        as values. """

        for name in anim_dict:
            self.animations[name] = anim_dict[name]

    def set_position(self, pos):
        """ Sets the position of the sprite on the screen. """

        self.x_pos, self.y_pos = pos


if __name__ == '__main__':
    #   Example script that draws a hydra on the screen. It only takes four
    #   lines of code to add the animation to a sprite, and one line to draw it.

    pygame.init()
    screen = pygame.display.set_mode((220, 150))
    pygame.display.set_caption("Sprite Tools Test")

    a = SpriteSheet('TestSprite.png', (4, 1), 4)
    b = Sprite(fps = 9)
    b.add_animation({"Idle": a})
    b.start_animation("Idle")

    while True:
        screen.fill((50, 50, 50))
        b.draw(screen)
        pygame.display.flip()
