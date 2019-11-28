import pyglet
import pymunk
from pymunk.pyglet_util import DrawOptions


class Block:
    def __init__(self, Mass, X, Y, PhysSpace):
        self.Body = pymunk.Body(Mass, pymunk.inf)
        self.Body.position = X, Y
        self.BodyShape = pymunk.Poly.create_box(self.Body, size=(50, 50))
        self.BodyShape.elasticity = 1

        PhysSpace.add(self.Body, self.BodyShape)

        self.BlockImg = pyglet.image.load('res/sqr.png')
        self.BlockImg.anchor_x = self.BlockImg.width // 2
        self.BlockImg.anchor_y = self.BlockImg.height // 2
        self.BlockSprite = pyglet.sprite.Sprite(self.BlockImg, x=self.Body.position.x, y=self.Body.position.y)

    def draw(self):
        self.BlockSprite.draw()

    def update(self):
        self.BlockSprite.position = self.Body.position


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
Wall.body.position = 10, Window.height / 2
Wall.elasticity = 1
Space.add(Wall)

# Create Right Box
BoxRight = pymunk.Body(10, pymunk.inf)
BoxRight.position = 2 * (Window.width / 3), 45
BoxRightShape = pymunk.Poly.create_box(BoxRight, size=(50, 50))
BoxRightShape.elasticity = 1
BoxRight.velocity = (-200, 0)
Space.add(BoxRight, BoxRightShape)

BoxImg = pyglet.image.load('res/sqr.png')
BoxImg.anchor_x = BoxImg.width // 2
BoxImg.anchor_y = BoxImg.height // 2
BoxRightSprite = pyglet.sprite.Sprite(BoxImg, x=BoxRight.position.x, y=BoxRight.position.y)

# Create Left Box
BoxLeft = pymunk.Body(1, pymunk.inf)
BoxLeft.position = Window.width / 3, 45
BoxLeftShape = pymunk.Poly.create_box(BoxLeft, size=(50, 50))
BoxLeftShape.elasticity = 1
Space.add(BoxLeft, BoxLeftShape)
BoxLeftSprite = pyglet.sprite.Sprite(BoxImg, x=BoxLeft.position.x, y=BoxLeft.position.y)

TestBlock = Block(10, 50, 50, Space)


@Window.event
def on_draw():
    Window.clear()
    TitleLabel.draw()
    Space.debug_draw(Options)
    BoxRightSprite.draw()
    BoxLeftSprite.draw()
    TestBlock.draw()


def update(dt):
    Space.step(dt)
    BoxRightSprite.position = BoxRight.position
    BoxLeftSprite.position = BoxLeft.position
    TestBlock.update()


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.gl.glClearColor(1, 1, 1, 1)
    pyglet.app.run()
