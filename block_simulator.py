import pyglet
import pymunk
from pymunk.pyglet_util import DrawOptions

# Initiate the window
Window = pyglet.window.Window(1280, 720, 'Block Collision Simulator', resizable=True)
Batch = pyglet.graphics.Batch()
Options = DrawOptions()

# Define Title Label
TitleLabel = pyglet.text.Label(text='Block Collision Simulator', x=Window.width / 2, y=Window.height - 20, batch=Batch
                               , anchor_x='center', anchor_y='center', font_size=24)

# Initiate space for Physics engine
Space = pymunk.Space()

# Create the ground
Ground = pymunk.Body(pymunk.inf, pymunk.inf, pymunk.Body.STATIC)
Ground.position = Window.width/2, 10
GroundBox = pymunk.Poly.create_box(Ground, size=(Window.width, 20))
Space.add(Ground, GroundBox)

# Create Wall
Wall = pymunk.Body(pymunk.inf, pymunk.inf, pymunk.Body.STATIC)
Wall.position = 10, Window.height/2
WallBox = pymunk.Poly.create_box(Wall, size=(20,Window.height))
Space.add(Wall, WallBox)

# Create Box
Box = pymunk.Body(10, 1000)
Box.position = Window.width/2, Window.height/2
BoxPoly = pymunk.Poly.create_box(Box, size=(50,50))
Space.add(Box, BoxPoly)

@Window.event
def on_draw():
    Window.clear()
    TitleLabel.draw()
    Space.debug_draw(Options)


if __name__ == '__main__':
    pyglet.app.run()
