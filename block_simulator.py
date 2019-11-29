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
        BodyShape = pymunk.Poly.create_box(self.Body, size=(50, 50))
        BodyShape.elasticity = 1

        PhysSpace.add(self.Body, BodyShape)

        BlockImg = pyglet.image.load('res/sqr.png')
        BlockImg.anchor_x = BlockImg.width // 2
        BlockImg.anchor_y = BlockImg.height // 2
        self.BlockSprite = pyglet.sprite.Sprite(BlockImg, x=self.Body.position.x, y=self.Body.position.y,
                                                batch=RenderBatch)

    def update(self):
        self.BlockSprite.position = self.Body.position

    def give_velocity(self, velocity):
        self.Body.velocity = (velocity, 0)


class Simulation(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pyglet.gl.glClearColor(1, 1, 1, 1)
        pyglet.clock.schedule_interval(self.update, 1 / 60)

        self.Batch = pyglet.graphics.Batch()

        # Create Title Label
        self.TitleLabel = pyglet.text.Label(text='Block Collision Simulator', x=self.width / 2, y=self.height - 20,
                                            batch=self.Batch, anchor_x='center', anchor_y='center', font_size=24,
                                            color=(0, 0, 0, 255))
        # Initiate space for Physics engine
        self.Space = pymunk.Space()

        # Create the ground
        Ground = pymunk.Poly.create_box(self.Space.static_body, size=(self.width, 20))
        Ground.body.position = self.width / 2, 10
        self.Space.add(Ground)

        GroundImg = pyglet.image.load('res/ground.png')
        self.GroundSprite = pyglet.sprite.Sprite(GroundImg, x=0, y=0, batch=self.Batch)

        # Create Wall
        Wall = pymunk.Poly.create_box(self.Space.static_body, size=(20, self.height))
        Wall.body.position = 10, self.height / 2
        Wall.elasticity = 1
        self.Space.add(Wall)

        WallImg = pyglet.image.load('res/wall.png')
        self.WallSprite = pyglet.sprite.Sprite(WallImg, x=0, y=0, batch=self.Batch)

        # Create Right Block
        self.BlockRight = Block(10, 2*(self.width / 3), 45, self.Space, self.Batch)
        self.BlockRight.give_velocity(-100)

        # Create Left Block
        self.BlockLeft = Block(1, self.width / 3, 45, self.Space, self.Batch)

        pyglet.app.run()

    def on_draw(self):
        self.clear()
        self.Batch.draw()

    def update(self, dt):
        self.Space.step(dt)
        self.BlockRight.update()
        self.BlockLeft.update()


if __name__ == '__main__':
    Window = Simulation(1280, 720, "Block Collision Simulator", resizable=False)

