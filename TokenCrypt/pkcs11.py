import PyKCS11

class MultipleMatchingTokens(LookupError):pass
class NoMatchingTokens(LookupError):pass
class SessionAlreadyOpen(RuntimeError):pass
class SessionNotOpen(RuntimeError):pass

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

class RSAPrivateToken(RSAPrivateKey):
    def __init__(self, *args, **kwargs):
        self.lib = PyKCS11.PyKCS11Lib()
        self.lib.load()

        self.slot = kwargs.get('slot', None)
        self.key  = kwargs.get('key', 0)
        self.pin  = kwargs.get('pin', None )

        self.session = None
        self._privkey = None

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

    def close(self, ):
        if self.session is None:
            raise SessionNotOpen()
        self.session.logout()
        self.session.closeSession()
        self.session = None


    def __exit__(self, et,ev, tb):
        self.close()

    def open(self, pin = None):
        if self.session is not None:
            raise SessionAlreadyOpen(self.session)

        if pin is None:
            pin = self.pin


        self.session = self.lib.openSession( self.slot , PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION)
        self.session.login( pin )

    def __enter__(self, ):
        self.open(self.pin)
        return self


    @property
    def privkey(self,):
        if self._privkey is None:
            keys  = self.session.findObjects([(PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY)])
            self._privkey  = keys[self.key]
        return self._privkey

    def signer(self, padding, algorithm):
        """
        Returns an AsymmetricSignatureContext used for signing data.
        """
        raise NotImplementedError()

    def decrypt(self, ciphertext, padding):
        """
        Decrypts the provided ciphertext.
        """
        raise NotImplementedError()

    def key_size(self):
        """
        The bit length of the public modulus.
        """
        self.privkey.to_dict()['CKA_MODULUS_BITS']

    def public_key(self):
        """
        The RSAPublicKey associated with this private key.
        """
        raise NotImplementedError()

    def sign(self, data, padding, algorithm):
        """
        Signs the data.
        """
        if self.session is None:
            raise SessionNotOpen()

        ## WE only support SHA1/PKCS1v15 at the moment.
        #  and have no sanity checking
        #  FIXME
        mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA1_RSA_PKCS, None)
        signature = self.session.sign(self.privkey, data, mechanism )


        return bytes(signature)

