Smartcard object Wrappers
=========================

This module provide cryptography compatible proxy class for using 
a crypto smartcard , (such as yubi key, or PKCS#11 token) to
process the actually cryptographic workload.

These are normally considered to be 'secure' tokens and the private
key they are normally configured so the private key is not extractable
from the token's hardware. As a result you need to request the token
to do any cryptographic operation for which you would normally use the
private key.

In this module you will find a new abstraction of cryptography's 
`RSAPrivateKey` class called `RSAPrivateToken` which instead using
one the normal cryptography provided backend uses an hardware token 
directly.

Currently this means the PKCS#11 API, as provided on Linux by the
opensc-pkcs11 [1]_ package. TokenCrypt uses the PyKCS11 library
to wrap the opensc PKCS#11 library and needs a environment variable
set so the library can be found on debian that would be

.. code:: shell

    export PYKCS11LIB=/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so


A use case of this library would be to use a yubikey to provide Oauth
identity services to python applications which use the requests-Oauth2 
library.  This is quite common if you are accessing 3rd party APIs to
cloud service systems.

In this case a `RSAPrivateToken` can be provided to the library in the place
of the  usual `RSAPrivateKey`. 

Many library examples show providing an PEM encoded string, but they also
work with a subclass of cryptography's `RSAPrivateKey`, as shown below.


Example
-------

.. code:: python

    import TokenCrypt
    from ThierAPI import APIConection, PrivateCredentials # Not a working example.

    rsa_key = TokenCrypt.RSAPrivateToken(slot = 0 , key = 0, pin = '123456' )
    with rsa_key:
        credentials = PrivateCredentials(args.consumer_key, rsa_key)
        api = APIConection(credentials)

        do_something_with(api)



.. [1] This is the package name in debian Stretch, Buster, Bullseye(so far), your
      distribution may vary.


Current Status
--------------

This is an initial proof of concept release which is design to have enough
code to support working as an Oauth client. As a result the only action currently
implemented on the key is signing.


But there is a lot todo, Pull requests and bug reports welcome.

TODO
----

    - Implement `RSAPublicToken` .
    - Dynamically select the signing mechanism based to the provided 
      padding and hash.
    - Implement decrypt.
    - Implement certificate extraction.
