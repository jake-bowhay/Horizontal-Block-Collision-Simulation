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
Ground = pymunk.Poly.create_box(Space.static_body, size=(Window.width, 20))
Ground.body.position = Window.width / 2, 10
Space.add(Ground)

# Create Wall
Wall = pymunk.Poly.create_box(Space.static_body, size=(20, Window.height))
Wall.body.position = 10, Window.height/2
Wall.elasticity = 1
Space.add(Wall)

# Create Right Box
BoxRight = pymunk.Body(10, pymunk.inf)
BoxRight.position = 2 * (Window.width / 3), 45
BoxRightShape = pymunk.Poly.create_box(BoxRight, size=(50, 50))
BoxRightShape.elasticity = 1
BoxRight.velocity = (-100, 0)
Space.add(BoxRight, BoxRightShape)

# Create Left Box
BoxLeft = pymunk.Body(1, pymunk.inf)
BoxLeft.position = Window.width / 3, 45
BoxLeftShape = pymunk.Poly.create_box(BoxLeft, size=(50, 50))
BoxLeftShape.elasticity = 1
Space.add(BoxLeft, BoxLeftShape)

@Window.event
def on_draw():
    Window.clear()
    TitleLabel.draw()
    Space.debug_draw(Options)


def update(dt):
    Space.step(dt)


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()
