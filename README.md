# 8-Bit CPU Emulator

I'll be revisiting the book "How do it know?" except this time
I want to build an 8-bit cpu virtually without having to spend
money on buying the components required. I plan on creating an
assembler for this CPU and then once that's done I'll try to
create a tiny compiler for a c like language in it then after
that I'll try to rewrite the compiler in this new language
itself. If all goes well then I'll proceed to writing a simple
operating system.

# Roadmap

- [ ] __Phase 1: Creating the soft-hard-ware__ <br>
  Playground development Phase

Before I start creating anything, I'll need a virtual playground
to build my CPU. I'll start with writing a simple GUI to show
the processor's circuitry working in real-time, memory, registers,
etc. For the sake of simplicity, I'll try not to create this
emulator as general purpose rather it is meant to be just for
this CPU only, any generality will be just a by-product. Once
the emulator is finished the circuitry for the CPU can be
finalized, also finalizing the instruction set.

---

- [ ] __Phase 2: Talking to the computer__ <br>
  Language Development Phase

First we'll be creating an assembler, either in assembly
itself or in python. Once the assembler is finished,
I'll begin writing a very simple and tiny compiler for
a new c like language for this CPU. Once it has enough
features to make writing a kernel a bit easier, I'll
rewrite the compiler in the language itself.


---

- [ ] __Phase 3: I'd like to speak to the manager!__ <br>
  Operating System Phase

If I reach this phase, maybe I'll finally be satisfied
with how my life is turning out in general. In this
phase, I will write a tiny operating system for this CPU.
I don't know how it'll display to the screen maybe this
will require changes in the emulator later on.


---

- [ ] __Phase 4: I see no god up here, other than me__ <br>
  The optional phase

Will try to implement more features in previous phases.
For example, I might implement networking.