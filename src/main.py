from src.emulator.electrical_lib.components import *
from time import sleep


class SRLatch:
    def __init__(self):
        self.nand_gate_1 = NandGate()
        self.nand_gate_2 = NandGate()

        Wire(self.nand_gate_1.input_pin_2, self.nand_gate_2.output_pin)
        Wire(self.nand_gate_2.input_pin_1, self.nand_gate_1.output_pin)

    @property
    def input_pin_1(self):
        return self.nand_gate_1.input_pin_1

    @property
    def input_pin_2(self):
        return self.nand_gate_2.input_pin_2

    @property
    def output_pin_1(self):
        return self.nand_gate_1.output_pin

    @property
    def output_pin_2(self):
        return self.nand_gate_2.output_pin

    def __repr__(self):
        return f"[I1]: {self.input_pin_1.state} | [O1]: {self.output_pin_1.state}\n" \
               f"[I1]: {self.input_pin_2.state} | [O2]: {self.output_pin_2.state}"


p1 = PowerSource()
p2 = PowerSource()
p2.output_pin.off()

sr_latch = SRLatch()

Wire(p1.output_pin, sr_latch.input_pin_1)
Wire(p2.output_pin, sr_latch.input_pin_2)


def switch():
    if p1.output_pin.is_on:
        print("here")
        p1.output_pin.off()
        p2.output_pin.on()
    else:
        p1.output_pin.on()
        p2.output_pin.off()


print(sr_latch)
p2.output_pin.on()
print(sr_latch)

# while True:
#     eval(input(">>> "))
#     sleep(0.1)
