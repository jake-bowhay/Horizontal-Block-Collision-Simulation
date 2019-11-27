import pyglet
import pymunk
from pymunk.pyglet_util import DrawOptions

Window = pyglet.window.Window(1280, 720, 'Block Collision Simulator', resizable=True)
Batch = pyglet.graphics.Batch()
Options = DrawOptions()

TitleLabel = pyglet.text.Label(text='Block Collision Simulator', x=Window.width / 2, y=Window.height - 20, batch=Batch
                               , anchor_x='center', anchor_y='center', font_size=24)
Space = pymunk.Space()

Ground = pymunk.Body(pymunk.Body.STATIC)
Ground.position = Window.width/2, 10
GroundBox = pymunk.Poly.create_box(Ground, size=(Window.width, 20))
Space.add(Ground, GroundBox)


@Window.event
def on_draw():
    Window.clear()
    TitleLabel.draw()
    Space.debug_draw(Options)


if __name__ == '__main__':
    pyglet.app.run()
