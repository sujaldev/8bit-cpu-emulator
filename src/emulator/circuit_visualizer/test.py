import arcade
from pyglet.math import Vec2
from renderers import *

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Platformer"


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color_from_hex_string("#222"))
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.keys_pressed = []
        self.gate1 = None
        self.gate2 = None
        self.wire = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.gate1 = RenderAndGate(AndGate(), 600, 600)
        power_source = PowerSource()
        Wire(power_source.output_pin, self.gate1.gate.input_pin_1)
        Wire(power_source.output_pin, self.gate1.gate.input_pin_2)
        self.gate2 = RenderAndGate(AndGate(), 900, 600)
        self.wire = RenderWire(
            Wire(self.gate1.gate.output_pin, self.gate2.gate.input_pin_2),
            ((120, 0), (0, "ey"))
        )

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Code to draw the screen goes here
        # self.camera.use()
        self.gate1.draw()
        self.gate2.draw()
        self.wire.draw()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
