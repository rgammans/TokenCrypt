import PyKCS11

class MultipleMatchingTokens(LookupError):pass
class NoMatchingTokens(LookupError):pass

class Algorithm:
    def __init__(self, *args, **kwargs):
        self.lib = PyKCS11.PyKCS11Lib()
        self.lib.load()

        self.slot = kwargs.get('slot', None)
        if self.slot is None:
            self.slot = self._resolve_slot(kwargs.get('token',{}))

    def _resolve_slot(self, tokenspec):
        slots = self.lib.getSlotList()
        found = None
        for s in slots:
            inf = self.lib.get_tokeninfo(s)
            ## Search through all the 
            #  provided data for a match with the token
            #  specified.
            for key in tokenspec.keys():
                if inf.get(key,None) != tokenspec[key]:
                    break
            else:
                ## If we find a match; see if we a have
                #  already found one as we want a unique
                #  match
                if found is not None:
                    raise MultipleMatchingTokens(found,s)
                found = s

        #Check we have a match
        if found is None:
            raise NoMatchingTokens(tokenspec)
        return found


