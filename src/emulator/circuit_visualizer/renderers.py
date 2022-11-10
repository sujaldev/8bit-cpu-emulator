from src.emulator.electrical_lib.components import *
import arcade
import ast


def verify_safe_expression(expression):
    # https://stackoverflow.com/a/72834811/15007549
    expr = ast.parse(expression, mode="eval")
    for node in ast.walk(expr):
        if not isinstance(node, (
                ast.Expression, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.BinOp,
                ast.USub, ast.UAdd, ast.UnaryOp
        )):
            raise Exception("Unsafe expression found in anchor expression")


class RenderGate(arcade.Sprite):
    IMAGE_PATH = ""

    def __init__(self, gate, x: float, y: float):
        super().__init__(self.IMAGE_PATH)
        self.left = x
        self.top = y
        self.gate = gate
        self.set_endpoint_locations()

    def set_endpoint_locations(self):
        self.gate.input_pin_1.x = self.left
        self.gate.input_pin_2.x = self.left
        self.gate.output_pin.y = self.center_y


class RenderAndGate(RenderGate):
    IMAGE_PATH = "../assets/and_gate.png"

    def set_endpoint_locations(self):
        super().set_endpoint_locations()
        self.gate.output_pin.x = self.left + self.width
        self.gate.input_pin_1.y = self.top - 20
        self.gate.input_pin_2.y = self.top - 58.5


class RenderWire:
    ON_COLOR = (0, 255, 0)
    OFF_COLOR = (255, 255, 255)

    def __init__(self, wire: Wire, anchors: tuple[tuple[int | str, int | str], ...] = (), stroke=3):
        """
        RenderWire can be instantiated without a Wire object, but it will not render unless the bind() method is called
        to bind it to an actual Wire object so that it can access the endpoint's locations. If no anchors are supplied,
        it will just draw a line from one endpoint to the other.

        :param wire: The wire that this wire renderer is bound to.

        :param anchors: Anchors are the points through which the wire will pass in the order they are specified. Anchors
        are specified relative to the last point, i.e., the first anchor's position is specified relative to the first
        endpoint's position whereas the second anchor's position is specified relative to the first anchor's position
        and so on. example: ((2, 0), (0, 10)) or more generally -> ((x1, y1), (x2, y2), ..., (xn, yn)). Moreover, you
        can use expressions in place of x and y like: ((2, 0), (0, "ey + 2")) where ey is the distance from your last
        anchor's y position to the second endpoint's y position. Similarly, you have ex available to use.
        """
        self.wire = wire
        self.endpoint1 = self.wire.endpoint1
        self.endpoint2 = self.wire.endpoint2
        self.anchors = anchors
        self.stroke = stroke
        self.parse_anchors()

    def parse_anchors(self):
        parsed_anchors = [(self.endpoint1.x, self.endpoint1.y)]

        for x, y in self.anchors:
            parsed_anchors.append((
                self.__parse_anchor_value(x, parsed_anchors[-1][0]),
                self.__parse_anchor_value(y, parsed_anchors[-1][1]),
            ))

        self.anchors = tuple(parsed_anchors[1:])

    def __parse_anchor_value(self, value, reference_value):
        if type(value) == str:
            new_value = self.__parse_anchor_expression(value)
            return new_value
        if type(value) == int:
            new_value = reference_value + value
            return new_value
        raise Exception("Invalid Anchor Value")

    def __parse_anchor_expression(self, expr):
        # noinspection PyUnusedLocal
        ex, ey = self.endpoint2.x, self.endpoint2.y
        expr = expr.replace("ex", str(ex)).replace("ey", str(ey))
        verify_safe_expression(expr)
        return eval(expr)

    def draw(self):
        color = self.ON_COLOR if self.wire.state == 1 else self.OFF_COLOR

        # If no anchors just draw a line connecting the two endpoints
        if not self.anchors:
            arcade.draw_line(
                self.endpoint1.x, self.endpoint1.y,
                self.endpoint2.x, self.endpoint2.y,
                color, self.stroke
            )
            return

        # draw from first endpoint to the first anchor
        arcade.draw_line(
            self.endpoint1.x, self.endpoint1.y,
            self.anchors[0][0], self.anchors[0][1],
            color, self.stroke
        )
        # draw all in between anchors
        for i in range(len(self.anchors) - 1):
            arcade.draw_line(
                self.anchors[i][0], self.anchors[i][1],
                self.anchors[i + 1][0], self.anchors[i + 1][1],
                color, self.stroke
            )
        # draw from last anchor to the second endpoint
        arcade.draw_line(
            self.anchors[-1][0], self.anchors[-1][1],
            self.endpoint2.x, self.endpoint2.y,
            color, self.stroke
        )
