import random
import sys
import time

from opcodetracer import OpcodeTracer, import_module


class Tracer(OpcodeTracer):

    def on_start(self):
        self.opcodes    = 0
        self.start_time = time.time()

    def on_stop(self):
        self.stop_time = time.time()

    def trace(self):
        self.opcodes += 1

    @property
    def elapsed(self):
        return self.stop_time - self.start_time


def generate_arrays(array_size):
    for _ in range(50):
        yield [random.randint(-100, 100) for _ in range(array_size)]
    yield list(range(array_size))           # Sorted.
    yield list(reversed(range(array_size))) # Reversed.
    yield [1]*array_size                    # Identical.


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: python {argv[0]} <sorting-module-path> <array-size>')
        sys.exit(1)
    module  = import_module(argv[1])
    arrays  = generate_arrays(int(argv[2]))
    tracers = []
    for array in arrays:
        print('.', end='', flush=True) # Show progress.
        with Tracer() as tracer:
            module.sort(array)
        assert array == sorted(array), f'{array} != {sorted(array)}'
        tracers.append(tracer)
    print(f'''

NUMBER OF OPCODES
=================

Average: {sum(tracer.opcodes for tracer in tracers) / len(tracers):.0f}
Worst:   {max(tracer.opcodes for tracer in tracers)}
Best:    {min(tracer.opcodes for tracer in tracers)}

ELAPSED TIME
============

Average: {sum(tracer.elapsed for tracer in tracers) / len(tracers):.02f}
Worst:   {max(tracer.elapsed for tracer in tracers):.02f}
Best:    {min(tracer.elapsed for tracer in tracers):.02f}

Total:   {sum(tracer.elapsed for tracer in tracers):.02f}''')


if __name__ == '__main__':
    sys.exit(main(sys.argv))
