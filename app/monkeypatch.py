import sys
import types
class DummyTorchClasses:
    def __getattr__(self, attr):
        return types.SimpleNamespace()

sys.modules['torch.classes'] = DummyTorchClasses()