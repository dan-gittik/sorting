import opcodetracer


module = opcodetracer.compile_module('''
def add(x, y):
    return x + y
''', name='demo')


class Tracer(opcodetracer.OpcodeTracer):
    
    def on_start(self):
        print('starting')

    def on_stop(self):
        print('stopping')

    def trace(self):
        print(f'{self.frame.f_code.co_filename}:{self.frame.f_lineno} [{self.frame.f_lasti}] {self.opname}')


with Tracer():
    z = module.add(1, 2) # This is traced.
    print(f'z = {z}')    # This isn't!
