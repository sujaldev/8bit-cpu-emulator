from math_objs import Vector
from skia import Surface, Canvas
import skia
from ui_backend import Window


class BaseLogicGateRenderer:
    def __init__(self, electrical_obj, symbol_file: str, relative_origin: Vector, position: Vector,
                 size_multiplier: float, window: Window):
        self.electrical_obj = electrical_obj
        self.symbol = skia.Image.open(symbol_file)
        self.relative_origin = relative_origin
        self.position = position
        self.size_multiplier = size_multiplier
        self.window = window

    @property
    def absolute_position(self):
        return (self.relative_origin + self.position).xy

    def render(self):
        with self.window.skia_surface as canvas:
            canvas: Canvas
            canvas.drawImage(self.symbol, *self.absolute_position)
            self.window.update()


def event_loop(canvas, event):
    if event.window.data1 == 79:
        pass


win = Window(
    "Drawing Test", 500, 500
)

rel_origin = Vector(0, 0)
and_gate = BaseLogicGateRenderer(1, "../assets/and_gate.png", Vector(20, 20), Vector(20, 30), 1, win)
and_gate.render()

win.start()
