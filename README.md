# Pyracy
*A collection of classes to support rapid game development with pygame.*



## Sprite Tools
These classes allow for manipulation of sprites and spritesheet objects, which read an image and display it on a pygame surface as an animation.

![image](https://raw.githubusercontent.com/jeremycryan/pyracy/master/TestSprite.png)

### The Sprite Sheet Object

The `SpriteSheet` object essentially holds the information for a single animation of a game object. For instance, your main character's idle, jumping, and running animations would be initialized as three separate sprite sheets, from three separate source images.

You can create a sprite sheet from an image by calling the `SpriteSheet` initializer. It takes the image path as a string, the number of columns and rows in the sheet as a tuple, and an int for the total number of frames in the animation.

`idle_anim = SpriteSheet('TestSprite.png', (4, 1), 4)`

You can access individual frames of the sprite as pygame surfaces with the `self.frames` attribute, or by calling `get_frame`.

### The Sprite Object

A `Sprite` object acts as a container for sprite sheets, allowing you to switch between animation modes for a single animated object. A game character with six different animations would be a single `Sprite` object, for instance.

To initialize a sprite, you just have an optional parameter for default frames per second. This framerate applies to all animations within the object.

`hydra = Sprite(fps = 9)`

To add a spritesheet to your sprite, use the `add_animation` method, which takes a dictionary of names for your `SpriteSheet` objects. You can have any number of uniquely named animations associated with a single sprite object.

`hydra.add_animation({"Idle": idle_anim})`

To start the animation, or switch to a different animation, use `start_animation`.

`hydra.start_animation("Idle")`

##  Particle Tools

These classes allow for customizable particle effects.

![image](https://raw.githubusercontent.com/jeremycryan/pyracy/master/particle_effect_example.png)

### The Particle Object

The `Particle` object holds relatively little information --- essentially just the size and image path of a particular particle, and some methods to update its attributes and draw it onto a screen.

It is initialized with any number of the parameters initial position, image path, width, height, and color. If the particle is part of a `ParticleEffect` instance, the position argument doesn't matter all that much, because particles will be instantiated by the class.

`smoke_bit = Particle(pos = (0, 0), path = 'circle', width = 20, height = 20, color = (125, 125, 125))`

Image path can be set as strings "circle" or "square", in which case it will just be drawn with the `pygame.draw` function. If you are loading an image from a file, you don't need to specify a color.

### The Particle Behavior Object

This is the meat of how the particle behaves and animates. A behavior, when applied to a particle, will animate that particle every time it is updated; for instance, make it more or less opaque, or move it across the screen.

There are several classes that are more defined and inherit from `ParticleBehavior`:

- `OpacityBehavior(init_opacity = 0.8, decay = 0.2)`

  This particle behavior affects a particles opacity. The particle will be created at opacity `init_opacity` and will fade at a speed of `decay` levels per second. With this class, an opacity of 1.0 is fully opaque, while 0 is fully transparent.
  
- `ScaleEffect(init_scale = 1.0, growth = 0.2)`
 
  This behavior affects a particle's size. `init_scale` scales the particle by a proportion on creation, after which it grows by `growth` amount per second, as a proportion of current size.
  
- `LinearMotionEffect(direction = 0, init_speed = 50.0, accel = 0)`

  This behavior moves the particle along a line. `direction` indicates initial direction of movement, as a proportion counterclockwise from the positive X axis; `init_speed` defines initial speed in pixels per second; and `accel` can specify a constant rate of acceleration (or decceleration) in pixels per second per second.
  
- `CircularMotionEffect(init_freq = 1.0, init_radius = 50.0, accel = 0, growth = 0, init_angle = 0)`

  Moves the particle in a circular path of radius `init_radius` pixels, at `init_freq` revolutions per second. This frequency increases at a rate of `accel` Hertz per second, and the radius widens at a rate of `growth` pixels per second. The initial angle is defined by `init_angle`.
  
These behaviors can be added to a particle effect with the `Particle.apply_behavior` method. For instance:

```
smoke_bit.apply_behavior(OpacityBehavior(init_opacity = 1.0, decay = 0.5))
smoke_bit.apply_behavior(LinearMotionEffect(direction = 0.25, init_speed = 30, accel = 0))
```

This make our little gray square drift upward at a constant speed while becoming more and more transparent.

### The Particle Effect Object

This object acts as a container for `Particle` objects. It can hold one or more particle objects, spawn them periodically, and itself move around the screen or with another object.

`ParticleEffect(pos = (0, 0), width = 50, height = 50, duration = -1)`

The `__init__` method takes an x, y position. The `width` and `height` parameter define a square field where particles are generated randomly, and the `duration` object specifies a time period, in seconds, after which the `ParticleEffect` expires.

#TODO finish this readme
