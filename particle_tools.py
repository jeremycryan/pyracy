#!/usr/bin/env python

#   Outside libraries
import pygame

#   Python libraries
import random
import time
from math import sin, cos, pi

################################################################################
########################## PARTICLE DEFINITION #################################
################################################################################

class Particle(object):
    """ A single particle from a system, drawn on the screen. """

    def __init__(self, pos = (0, 0), path = "square", width = 10, height = 10):
        """ Initialization function for particle """

        #   Type of particle --- either str 'square', 'circle', or an image path
        self.path = path

        #   Initial position of the particle
        self.pos = pos

        #   Some initial values
        self.created_at = time.time()
        self.anim_speed = 1.0   #   Alter this to slow/speed the animation
        self.behaviors = []

        #   Default values that can be modified by particle behaviors
        self.opacity = 1.0
        self.color = (160, 20, 200)
        #   TODO make width and height variable on image used
        self.width = width     #   Width of particle in pixels
        self.height = height    #   Height pf particle in pixels

        #   Potential parameters:
        #   - Initial position
        #   - Initial velocity
        #   - Acceleration/deceleration
        #   - Curvature in motion
        #   - Initial scale, growth/shrinking
        #   - Initial opacity, fading
        #   - Duration of particle
        #   - Death condition of particle (e.g. at opacity 0 or scale 0)
        #   - Color/value shift
        #   - "Chaos" attribute for each of these... how much variation there
        #       is for each behavior
        #   - Particle shape/source image/physical appearance
        #   - It's sounding increasingly like "ParticleAttribute" should be a
        #       class of its own...

        #   Important attributes:
        #   - Current all of those things
        #   - Time of creation

    def create(self, pos):
        """ Returns a particle instance with the same attributes at a given
        position. """

        #   Instantiate the particle
        particle = Particle(pos, self.path, self.width, self.height)

        #   Add all of the original particles behaviors
        particle.behaviors = self.behaviors[:]

        return particle

    def update_particle(self, dt):
        """ Updates the particle based on the amount of time that has passed."""

        #   Calls the update function for each behavior attached to this particle
        for item in self.behaviors:
            item.update(self, dt)

    def apply_behavior(self, behavior):
        """ Applies a particle behavior to the particle. """

        self.behaviors.append(behavior)

    def draw(self, screen):
        """ Draws the particle on the screen at its current position """

        #   Draw method for square particle
        if self.path == "square":
            self.draw_square(screen)
        else:
            print("Unable to draw particle of type %s." % self.path)

    def draw_square(self, screen):
        """ Draws the particle as a square, centered at the position self.pos"""

        #   Create values for width and height
        w = int(self.width)
        h = int(self.height)
        half_w = 0.5 * w
        half_h = 0.5 * h

        #   Determine position of blit based on width and height
        x = self.pos[0] - half_w
        y = self.pos[1] - half_h
        blit_pos = (x, y)

        #   Create pygame surface
        square = pygame.Surface((w, h))
        square.fill(self.color)
        alpha = int(self.opacity * 255)
        square.set_alpha(alpha)

        #   Blit to screen
        screen.blit(square, (x, y))


    def on_apply(self, particle):
        """ Applies any immediate alterations to the particle when the effect is
        added. """
        pass


    def update(self):
        """ Updates all of the particles attributes based on the initial
        conditions and elapsed time """
        pass



class ParticleBehavior(object):
    """ Defines a single behavior of a particle, such as a change in opacity
    over time. """

    def __init__(self, *args, **kwargs):
        """ Init function for particle behavior """
        pass

    def update(self, particle, dt):
        """ Applies the animation effect to the particle. """
        pass

################################################################################
###################### SPECIFIC PARTICLE EFFECTS ###############################
################################################################################

class OpacityEffect(ParticleBehavior):
    """ Defines an opacity animation for a particle """


    def __init__(self, init_opacity = 0.8, decay = 0.2):
        """ Initializes the opacity effect.

        init_opacity is the initial opacity of the particle, with 1.0 being
            completely opaque.
        decay is the opacity reduction per second for the particle. """

        #   Initialize the superclass
        super(OpacityEffect, self).__init__(init_opacity = 0.8, decay = 0.2)

        #   Set the parameters of the effect
        self.init_opacity = init_opacity
        self.decay = decay


    def on_apply(self, particle):
        """ Applies any immediate alterations to the particle when the effect is
        added. """

        #   Set the initial opacity
        particle.opacity = self.init_opacity


    def update(self, particle, dt):
        """ Applies the animation effect to the particle.

        particle: the particle object to apply the change
        dt: the time since last update, in seconds """

        #   Modify the particle's opacity basaed on the decay rate
        particle.opacity -= dt * self.decay


class ScaleEffect(ParticleBehavior):
    """ Defines an animation changing the particle's scale """


    def __init__(self, init_scale = 1.0, growth = 0.2):
        """ Initializes the scale effect.

        init_scale: the initial multiplicative scale applied to the particle;
            a scale of 1.0 means it doesn't change size.
        growth: the change in scale in terms of proportion per second. This
            compounds.
        """

        self.init_sclae = init_scale
        self.growth = growth


    def on_apply(self, particle):
        """ Applies any immediate alterations to the particle when the effect is
        added. """

        particle.width *= init_scale

        particle.height *= init_scale


    def update(self, particle, dt):
        """ Applies the animation effect to the particle.

        particle: the particle object to apply the change
        dt: the time since last update, in seconds """

        growth_prop = (1.0 + self.growth) ** dt

        particle.width *= growth_prop
        particle.height *= growth_prop




class LinearMotionEffect(ParticleBehavior):
    """ Defines an animation for a particle moving in a straight line. """


    def __init__(self, direction = 0, init_speed = 50.0, accel = 0):
        """ Initializes the motion effect.

        direction: proportional angle counterclockwise from the positive X axis,
            i.e. 0 is due right, 0.5 is due left, etc
        init_speed: initial speed of the particle's motion in pixels per second
        accel: change to speed, in pixels per second per second. If a negative
            acceleration would reduce the speed to below zero, the speed is
            set to zero instead. """

        #   Initialize the superclass
        super(LinearMotionEffect, self).__init__(direction = direction,
            init_speed = init_speed,
            accel = accel)

        self.direction = direction
        self.init_speed = init_speed
        self.accel = accel
        self.speed = init_speed


    def update(self, particle, dt):
        """ Applies the animation effect to the particle.

        particle: the particle object to apply the change
        dt: the time since last update, in seconds """

        #   Change the particle's position based on the speed. Uses an average
        #   of speeds before and after the tick to help mitigate changes in
        #   behavior at different loop speeds.
        old_speed = self.speed
        new_speed = old_speed + self.accel*dt
        avg_speed = 0.5 * (old_speed + new_speed)
        self.speed = new_speed

        #   Apply position change to x and y positions
        dir_rad = 2 * pi * self.direction
        x_prop, y_prop = cos(dir_rad), sin(dir_rad)
        dx, dy = x_prop * avg_speed * dt, y_prop * avg_speed * dt
        x = particle.pos[0] + dx
        y = particle.pos[1] + dy
        particle.pos = (x, y)


################################################################################
############################### DEMO SCRIPT ####################################
################################################################################

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    pygame.display.set_caption("Particle Tools Test")


    a = Particle(pos = (100, 100), path = "square", width = 20, height = 20)
    a.apply_behavior(OpacityEffect(decay = 1.0))
    a.apply_behavior(ScaleEffect(growth = -0.6))
    a.apply_behavior(LinearMotionEffect(direction = 0.25, init_speed = 50))

    particles = []

    then = time.time()
    timer = 0
    while True:
        now = time.time()
        dt = now - then
        then = now
        timer += dt
        screen.fill((0, 0, 0))
        space = 0.10
        if timer > space:
            timer -= space
            x = (random.random() * 100) + 50
            y = (random.random() * 100) + 50
            particles.append(a.create((x, y)))

        for part in particles:
            if part.opacity <= 0:
                particles.remove(part)
            part.update_particle(dt)
            part.draw(screen)


        pygame.display.flip()
        time.sleep(0.01)
