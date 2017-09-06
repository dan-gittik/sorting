import opcode
import sys


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
