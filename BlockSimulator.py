import pyglet
import pymunk

Window = pyglet.window.Window(1280, 720, 'Block Collision Simulator', resizable=True)

@Window.event
def OnDraw():
    Window.clear()

def Update(dt):
    pass


def Main():
    pyglet.clock.schedule_interval(Update, 1/60)
    pyglet.app.run()


if __name__ == '__main__':
    Main()
