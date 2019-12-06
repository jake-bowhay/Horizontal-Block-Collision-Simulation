import pyglet
import pymunk


class Block:
    def __init__(self, Mass, Elasticity, X, Y, PhysSpace, RenderBatch):
        """
        The class for a block in the simulation
        :param Mass: The mass the block
        :param Elasticity: The elasticity of the block between 0-1. 0 gives no bounce and 1 gives a perfect bounce
        :param X: Initial x position
        :param Y: Initial y position
        :param PhysSpace: The pymunk physics space to add items to
        :param RenderBatch: The the pyglet batch to add block to. This will be how the block is drawn
        """
        # Create pymunk body with the given mass and infinite moment of inertia so that it doesn't rotate
        self.Body = pymunk.Body(Mass, pymunk.inf)
        self.Body.position = X, Y
        # Create the polygon to give the body space and represent the block in plunk space
        BodyShape = pymunk.Poly.create_box(self.Body, size=(50, 50))
        # Assign id for use later in determining what items are colliding
        BodyShape.id = 'Block'
        BodyShape.elasticity = Elasticity
        # Add block to the pymunk physics space
        PhysSpace.add(self.Body, BodyShape)

        BlockImg = pyglet.image.load('res/sqr.png')
        # Set anchor point of image to be the centre
        BlockImg.anchor_x = BlockImg.width // 2
        BlockImg.anchor_y = BlockImg.height // 2
        # Create sprite for block in pyglet to display the block
        self.BlockSprite = pyglet.sprite.Sprite(BlockImg, x=self.Body.position.x, y=self.Body.position.y,
                                                batch=RenderBatch)

    def update(self):
        # Set the position of the sprite to be equal to the position of the physics body
        self.BlockSprite.position = self.Body.position

    def give_velocity(self, velocity):
        """
        Set x component of velocity
        :param velocity: float containing velocity to be set
        """
        self.Body.velocity = (velocity, 0)


class Simulation(pyglet.window.Window):
    def __init__(self, Data, *args, **kwargs):
        """
        The pyglet window to draw the simulation in
        :param Data: Data to describe what to be simulated. Should be a dictionary with two keys 'StartVelocity'
        should be a float and 'Blocks' which should be a list. Each item in the list represents a block
        to be created in the simulation and should be a dictionary with two keys 'mass' and 'elasticity' both of which
        should be floats.
        """
        super().__init__(*args, **kwargs)

        # Set background to be white
        pyglet.gl.glClearColor(1, 1, 1, 1)

        # Set window icon
        icon = pyglet.image.load('res/icon.ico')
        self.set_icon(icon)

        # Set clock speed to 1/60 and the function to call
        pyglet.clock.schedule_interval(self.update, 1/60)

        # Create pyglet batch to draw all the graphics with
        self.Batch = pyglet.graphics.Batch()

        # Create Title Label
        TitleLabel = pyglet.text.Label(text='Block Collision Simulator', x=self.width / 2, y=self.height - 20,
                                            batch=self.Batch, anchor_x='center', anchor_y='center', font_size=24,
                                            color=(0, 0, 0, 255))
        # Create collision counter and set it to 0
        self.Counter = 0
        self.CounterLabel = pyglet.text.Label('Collision Counter = 0'.format(self.Counter), x=self.width / 2,
                                              y=self.height - 60, anchor_x='center', anchor_y='center', font_size=24,
                                              color=(0, 0, 0, 255), batch=self.Batch)

        # Initiate space for Physics engine and set the collision handler
        self.Space = pymunk.Space()
        Handler = self.Space.add_default_collision_handler()
        Handler.begin = self.coll_begin

        # Create the ground in physics engine as a pymunk static body
        Ground = pymunk.Poly.create_box(self.Space.static_body, size=(self.width, 20))
        Ground.body.position = self.width / 2, 10
        Ground.id = 'Ground'
        self.Space.add(Ground)

        # Create the sprite for the ground
        GroundImg = pyglet.image.load('res/ground.png')
        GroundSprite = pyglet.sprite.Sprite(GroundImg, x=0, y=0, batch=self.Batch)

        # Create Wall in physics engine as a pymunk static body
        Wall = pymunk.Poly.create_box(self.Space.static_body, size=(20, self.height))
        Wall.body.position = 10, self.height / 2
        Wall.id = 'Wall'
        Wall.elasticity = 1
        self.Space.add(Wall)

        # Create the sprite for the wall
        WallImg = pyglet.image.load('res/wall.png')
        WallSprite = pyglet.sprite.Sprite(WallImg, x=0, y=0, batch=self.Batch)

        # List to store all the instances of the block class
        self.Blocks = []
        # Extract the number of blocks to be create from the data passed from the launcher
        NumberOfBlocks = len(Data['Blocks'])
        for BlockNumber, BlockData in enumerate(Data['Blocks']):
            # Add a new instance of the block class for each block
            # Blocks are evenly spaced across the width of the window
            self.Blocks.append(Block(BlockData['Mass'], BlockData['Elasticity'],
                                     (BlockNumber + 1) * (self.width / (NumberOfBlocks + 1)),
                                     45, self.Space, self.Batch))

        # The last block (furthest right) a velocity based on the data from the launcher
        self.Blocks[-1].give_velocity(-Data['StartVelocity'])

        pyglet.app.run()

    def coll_begin(self, arbiter, space, data):
        '''
        Function to be called when a collision begins follows format defined in pymunk API
        :param arbiter: Arbiter contains information about the colliding shapes and the data about the collision
        :param space: The space object in which the collision took place
        :param data: Dictionary containing
        :return: Returns a boolean. Return true for pymunk to process collision or false to ignore the collision
        '''
        # Check if the collision involves the ground as the counter should not increase from blocks hitting the ground
        InvolvesGround = False
        for Shape in arbiter.shapes:
            if Shape.id == 'Ground':
                InvolvesGround = True
        # If a block to block collision increase the counter
        if not InvolvesGround:
            self.Counter += 1
        self.CounterLabel.text = 'Collision Counter: {}'.format(self.Counter)
        return True

    def on_draw(self):
        # Called when window is created and draws all items in the batch
        self.clear()
        self.Batch.draw()

    def update(self, dt):
        """
        Called every clock cycle
        :param dt: The time elapsed since the last clock cycle
        """
        # Update the physics environment 2000x per cycle to prevent fast moving object from passing through statics
        for Step in range(2000):
            self.Space.step(dt/2000)
        # Update the sprite position to be in the same has the block in the physics space
        for IndividualBlock in self.Blocks:
            IndividualBlock.update()
