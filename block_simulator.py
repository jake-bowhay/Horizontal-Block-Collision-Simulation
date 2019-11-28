import pyglet
import pymunk


class Block:
    """
    The class for a block
    Mass: the mass the block
    X: Initial x position
    Y: Initial y position
    PhysSpace: The physics space to add items to
    RenderBatch: Batch to add block to
    """

    def __init__(self, Mass, X, Y, PhysSpace, RenderBatch):
        self.Body = pymunk.Body(Mass, pymunk.inf)
        self.Body.position = X, Y
        self.BodyShape = pymunk.Poly.create_box(self.Body, size=(50, 50))
        self.BodyShape.elasticity = 1

        PhysSpace.add(self.Body, self.BodyShape)

        self.BlockImg = pyglet.image.load('res/sqr.png')
        self.BlockImg.anchor_x = self.BlockImg.width // 2
        self.BlockImg.anchor_y = self.BlockImg.height // 2
        self.BlockSprite = pyglet.sprite.Sprite(self.BlockImg, x=self.Body.position.x, y=self.Body.position.y,
                                                batch=RenderBatch)

    def update(self):
        self.BlockSprite.position = self.Body.position

    def give_velocity(self, velocity):
        self.Body.velocity = (velocity, 0)


# Initiate the window
Window = pyglet.window.Window(1280, 720, 'Block Collision Simulator', resizable=False)
Batch = pyglet.graphics.Batch()

# Define Title Label
TitleLabel = pyglet.text.Label(text='Block Collision Simulator', x=Window.width / 2, y=Window.height - 20, batch=Batch
                               , anchor_x='center', anchor_y='center', font_size=24, color=(0, 0, 0, 255))

# Initiate space for Physics engine
Space = pymunk.Space()

# Create the ground
Ground = pymunk.Poly.create_box(Space.static_body, size=(Window.width, 20))
Ground.body.position = Window.width / 2, 10
Space.add(Ground)

GroundImg = pyglet.image.load('res/ground.png')
GroundSprite = pyglet.sprite.Sprite(GroundImg, x=0, y=0, batch=Batch)

# Create Wall
Wall = pymunk.Poly.create_box(Space.static_body, size=(20, Window.height))
Wall.body.position = 10, Window.height / 2
Wall.elasticity = 1
Space.add(Wall)

WallImg = pyglet.image.load('res/wall.png')
WallSprite = pyglet.sprite.Sprite(WallImg, x=0, y=0, batch=Batch)

# Create Right Block
BlockRight = Block(10, 2 * (Window.width / 3), 45, Space, Batch)
BlockRight.give_velocity(-100)

# Create Left Block
BlockLeft = Block(1, Window.width / 3, 45, Space, Batch)


@Window.event
def on_draw():
    Window.clear()
    Batch.draw()


def update(dt):
    Space.step(dt)
    BlockRight.update()
    BlockLeft.update()


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.gl.glClearColor(1, 1, 1, 1)
    pyglet.app.run()
