from primitives import *


class PowerSource:
    def __init__(self):
        self.output_pin = OutputPin(self)
        self.output_pin.state = ON


class BaseGateClass:
    def __init__(self):
        self.output_pin = OutputPin(self)

    def logic_func(self) -> bool:
        pass

    def update_output(self) -> None:
        output_is_on = self.logic_func()
        self.output_pin.on() if output_is_on else self.output_pin.off()


class NotGate(BaseGateClass):
    def __init__(self):
        super().__init__()
        self.input_pin = InputPin(self)

    def logic_func(self):
        return not self.input_pin


class OrGate(BaseGateClass):
    def __init__(self):
        super().__init__()
        self.input_pin_1 = InputPin(self)
        self.input_pin_2 = InputPin(self)

    def logic_func(self):
        return self.input_pin_1.state or self.input_pin_2.state


class NorGate(BaseGateClass):
    def __init__(self):
        super().__init__()
        self.input_pin_1 = InputPin(self)
        self.input_pin_2 = InputPin(self)

    def logic_func(self):
        return not (self.input_pin_1.state or self.input_pin_2.state)


class AndGate(BaseGateClass):
    def __init__(self):
        super().__init__()
        self.input_pin_1 = InputPin(self)
        self.input_pin_2 = InputPin(self)

    def logic_func(self):
        return self.input_pin_1.state and self.input_pin_2.state


class NandGate(BaseGateClass):
    def __init__(self):
        super().__init__()
        self.input_pin_1 = InputPin(self)
        self.input_pin_2 = InputPin(self)

    def logic_func(self):
        return not (self.input_pin_1.state and self.input_pin_2.state)


class XorGate(BaseGateClass):
    def __init__(self):
        super().__init__()
        self.input_pin_1 = InputPin(self)
        self.input_pin_2 = InputPin(self)

    def logic_func(self):
        return self.input_pin_1.state != self.input_pin_2.state
