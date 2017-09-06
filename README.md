# Sorting

A collection of sorting algorithms implemented in Python, with an absolute overkill of an infrastructure to
measure their runtime complexity.

## Usage

To run a specific algorithm, run ``main.py`` on a module with a ``sort(array)`` function and some input size.
For example:

```shell
$ python main.py bubble.py 100
.....................................................

NUMBER OF OPCODES
=================

Average: 64045
Worst:   100306
Best:    415

ELAPSED TIME
============

Average: 0.08
Worst:   0.13
Best:    0.00

Total:   4.35
```

So far I've implemented:

- [Bubble Sort](https://en.wikipedia.org/wiki/Bubble_sort)
- [Insertion Sort](https://en.wikipedia.org/wiki/Insertion_sort)
- [Selection Sort](https://en.wikipedia.org/wiki/Selection_sort)
- [Merge Sort](https://en.wikipedia.org/wiki/Merge_sort)
- [Quicksort](https://en.wikipedia.org/wiki/Quicksort)
- [Heap Sort](https://en.wikipedia.org/wiki/Heapsort)

## Runtime Complexity Measurement

The obvious thing to measure is runtime (in seconds), but I wanted a more robust metric: the number of opcodes
executed to perform the sort.

Unfortunately, Python's tracer (``sys.settrace``) works on source lines rather than opcodes, and if you've programmed
in Python for more than a couple months, you probably had that phase where you did everything with a one liner and know
that sources lines mean very little.

Instead, and with [Ned Batchelder's help](https://nedbatchelder.com/blog/200804/wicked_hack_python_bytecode_tracing.html),
I wrote a tracer that works on opcodes! 

Tracing opcodes only runs on specially compiled modules, so you'd have to run ``module = compiled_module(source)``
or ``module = import_module(path)``, and then trace that module's execution. To do that, subclass ``OpcodeTracer``
and implement the ``trace()`` method, which will be invoked for every opcode executed by specially compiled modules
in the traced context. For example:

```python
>>> module = compile_module('''
... def add(x, y):
...    return x + y
... ''')

>>> class Tracer(OpcodeTracer):
...     def trace(self):
...         print(self.opname)

>>> with Tracer():
...     module.add(1, 2)
LOAD_FAST
LOAD_FAST
BINARY_ADD
RETURN_VALUE
```

``compile_module(source, name='')``

Receives Python source code and optionally the module name, and returns the specially compiled module.

``import_module(path)``

Receives a path to a Python module, derives the module name from it, and returns the specially compiled module.

``OpcodeTracer(whitelist=[])``

Receives an optional whitelist of opcode names, and returns a context manager.
- When it starts, it calls ``on_start()``.
- When it stops, it calls ``on_stop()``.
- When it is active, it calls ``trace()`` for every opcode executed by specially compiled modules (if a whitelist
  was specified, only opcodes in the whitelist are traced). Several attributes are available to id: ``self.frame``
  is the current frame; ``self.event`` is the current event; ``self.arg`` is the current argument; ``self.opcode``
  is the current opcode; and ``self.opname`` is the current opcode name.
