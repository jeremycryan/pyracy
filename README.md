# Pyracy
*A collection of classes to support rapid game development with pygame.*

## Sprite Tools
These classes allow for manipulation of sprites and spritesheet objects, which read an image and display it on a pygame surface as an animation.

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
