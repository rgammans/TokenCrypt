Smartcard object Wrappers
=========================

This module provide pycrypto compatible proxies which use a 
crypto smartcard , (such as yubi key, or PKCS#11 token) to
process the actually cryptographic workload.

These a re normally consider 'secure' tokens and the private key is not 
extractable from the tokens.

A use case of this would be to use a yubikey to provide Oauth identity
services to python applications using requests-Oauth2 .

