import dis
import opcode
import os
import struct
import sys
import types


def compile_module(source, name=None):
    if name is None:
        name = ''
    code   = compile(source, name, 'exec')
    code   = _patch_line_numbers(code)
    module = types.ModuleType(name)
    module.__patched__ = True
    exec(code, vars(module), vars(module))
    return module


def import_module(path):
    name = os.path.basename(os.path.splitext(path)[0])
    with open(path) as reader:
        source = reader.read()
    return compile_module(source, name)


def _patch_line_numbers(code):
    new_lnotab = []
    for instruction in list(dis.get_instructions(code))[1:]:
        new_lnotab.append(struct.pack('bb', 1 if instruction.arg is None else 2, 1))
    new_lnotab = b''.join(new_lnotab)
    new_consts = []
    for const in code.co_consts:
        new_consts.append(_patch_line_numbers(const) if isinstance(const, types.CodeType) else const)
    return types.CodeType(
        code.co_argcount,
        code.co_kwonlyargcount,
        code.co_nlocals,
        code.co_stacksize,
        code.co_flags,
        code.co_code,
        tuple(new_consts),
        code.co_names,
        code.co_varnames,
        code.co_filename,
        code.co_name,
        code.co_firstlineno,
        new_lnotab,
    )  


class OpcodeTracer:
    
    def __init__(self, whitelist=None):
        self.whitelist = whitelist

    def __call__(self, frame, event, arg):
        if not frame.f_globals.get('__patched__') or frame.f_lasti == -1:
            return self
        self.frame  = frame
        self.event  = event
        self.arg    = arg
        self.opcode = frame.f_code.co_code[frame.f_lasti]
        self.opname = opcode.opname[self.opcode]
        if not self.whitelist or self.opname in self.whitelist:
            self.trace()
        return self

    def __enter__(self):
        self.on_start()
        self.old = sys.gettrace()
        sys.settrace(self)
        return self

    def __exit__(self, exception, error, traceback):
        sys.settrace(self.old)
        self.on_stop()

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def trace(self):
        pass
