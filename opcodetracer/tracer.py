import dis
import opcode
import sys


class OpcodeTracer:
    
    def __init__(self, whitelist=None):
        self.whitelist = whitelist

    def __call__(self, frame, event, argument):
        if not frame.f_globals.get('__patched__') or frame.f_lasti == -1:
            return self
        self.frame, self.event, self.argument = frame, event, argument
        self.offset = self.frame.f_lasti
        self.opcode = self.frame.f_code.co_code[self.offset]
        self.opname = opcode.opname[self.opcode]
        if self.whitelist and self.opname not in self.whitelist:
            return self
        self._instruction = None
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

    @property
    def instruction(self):
        if not self._instruction:
            for instruction in dis.get_instructions(self.frame.f_code):
                if instruction.offset == self.offset:
                    self._instruction = instruction
                    break
        return self._instruction
