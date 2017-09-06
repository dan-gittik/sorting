from . import compile_module, OpcodeTracer


module = compile_module('''
def add(x, y):
    return x + y
''', name='demo')


class Tracer(OpcodeTracer):
    
    def on_start(self):
        print('starting')

    def on_stop(self):
        print('stopping')

    def trace(self):
        print(f'{self.frame.f_code.co_filename}:{self.frame.f_lineno} [{self.instruction.offset}] {self.instruction.opname}' +
             (f' ({self.instruction.argrepr})' if self.instruction.arg is not None else ''))


with Tracer():
    z = module.add(1, 2) # This is traced.
    print(f'z = {z}')    # This isn't!
