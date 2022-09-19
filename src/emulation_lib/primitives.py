from typing import List, Union

__all__ = [
    'Wire', 'InputPin', 'OutputPin', 'ON', 'OFF'
]

OFF = 0
ON = 1


class BasicPart:
    """
    Purpose of this class is just to remove some repetitive code common in InputPin, OutputPin and Wire class.
    """

    def __init__(self):
        self.state = OFF

    # The following properties are just syntactic sugar
    @property
    def is_on(self):
        return self.state == ON

    @property
    def is_off(self):
        return self.state == OFF

    def push_state_change(self) -> None:
        pass

    def off(self) -> None:
        self.state = OFF
        self.push_state_change()

    def on(self) -> None:
        self.state = ON
        self.push_state_change()


class Wire(BasicPart):
    def __init__(self, endpoint1: Union["OutputPin", "InputPin", "Wire"],
                 endpoint2: Union["OutputPin", "InputPin", "Wire"]):

        super().__init__()
        self.endpoint1 = endpoint1
        self.endpoint2 = endpoint2
        self.attach_parallel_wire_endpoints()

        self.parallel_wires: List[Wire] = []

    # Syntactic Sugar
    @property
    def endpoints(self):
        return self.endpoint1, self.endpoint2

    def attach_parallel_wire_endpoints(self):
        for endpoint in self.endpoints:
            if isinstance(endpoint, Wire):
                endpoint.parallel_wires.append(self)

    def calculate_state(self) -> None:
        """
        To calculate the state of the wire, it's endpoints take precedence over the parallel wires. That is, while
        calculating the state of this wire, it'll first check whether it has at least one endpoint of type either Output
        Pin or Wire with a power ON state, if it does, then it will not check the parallel wires as it can't change the
        state of the wire. In case there is no such endpoint, it will then check if any of the parallel wires are
        providing power to this wire.
        """

        # Check whether this wire is getting power from any of its endpoints, if it is, then turn it ON.
        for endpoint in self.endpoints:
            endpoint_can_provide_power = isinstance(endpoint, OutputPin) or isinstance(endpoint, Wire)
            if endpoint_can_provide_power and endpoint.is_on:
                self.on()
                return

        # If none of the endpoints are providing power, then this wire must turn OFF. (Unless there is a parallel wire
        # providing power)
        self.off()

        # The parallel wires that remained ON even after this wire turned OFF, they must be acting as power sources to
        # this wire and so this wire must turn ON again.
        for wire in self.parallel_wires:
            if wire.is_on:
                self.on()
                return

    def push_state_change(self):
        """
        This will push a state change to its endpoints if they are of type InputPin or Wire and not to OutputPin as a
        wire does not control the state of an OutputPin (it's controlled by the component it is bound to). It will also
        push a state change to all its parallel wires.
        """

        for endpoint in self.endpoints:
            if isinstance(endpoint, InputPin):
                endpoint.on() if self.is_on else endpoint.off()
            elif isinstance(endpoint, Wire):
                endpoint.calculate_state()

        for wire in self.parallel_wires:
            wire.calculate_state()


class InputPin(BasicPart):
    def __init__(self, parent_component, connected_wire: Wire = None):
        """
        An input pin is the type of pin which will never have internal power from the component it is bound to. This
        implies that the state of this type of pin relies solely on the wire it is attached to.

        :param connected_wire: A pin only has one wire connected to it. Pins can have multiple attached wires, but not
        directly, they should be attached parallel to the main wire rather than being attached to the pin, since it
        makes no difference in terms of physics as far as we are concerned for this project, and makes the code a lot
        easier to write and understand.

        :param parent_component: The component to which this pin is bound to.
        """

        super().__init__()
        self.parent_component = parent_component
        self.connected_wire = connected_wire

        is_connected = self.connected_wire is not None
        if is_connected:
            self.state = self.connected_wire.state

    def push_state_change(self):
        # Picture this as a push notification to the parent component, letting it know that the state of this pin has
        # changed, and it should update it's output accordingly
        self.parent_component.update_output()


class OutputPin(BasicPart):
    def __init__(self, parent_component, connected_wire: Wire = None):
        """
        An OutputPin is the type of pin whose state is controlled by its parent component rather than the wire it is
        attached to. This implies that the state of this type of pin relies solely on the logic of the component it is
        attached to.

        :param connected_wire: A pin only has one wire connected to it. Pins can have multiple attached wires, but not
        directly, they should be attached parallel to the main wire rather than being attached to the pin, since it
        makes no difference in terms of physics as far as we are concerned for this project, and makes the code a lot
        easier to write and understand.

        :param parent_component: The component to which this pin is bound to.
        """
        super().__init__()

        self.parent_component = parent_component
        self.connected_wire = connected_wire

    def push_state_change(self):
        # Picture this as a push notification to the connected wire, letting it know that the state of this pin has
        # changed, and it should update it's state accordingly
        self.connected_wire.calculate_state()
