import PyKCS11
class Algorithm:
    def __init__(self, *args, **kwargs):
        self.lib = PyKCS11.PyKCS11Lib()

        self.slot = kwargs.get('slot', None)
        if self.slot is None:
            self.slot = self._resolve_slot(**kwargs)

    def _resolve_slot(self, **data):
        slots = self.lib.get_slots()
        found = None
        for s in slots:
            inf = self.lib.get_tokeninfo(s)

        return found


