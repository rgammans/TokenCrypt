import unittest
import unittest.mock
import os

import PyKCS11
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

import TokenCrypt.pkcs11 as mut


## Use the opensc-pkcs11 library for testing.,
#  in the few tests which hit the backend.
#
# ( It's useful that some do; as that validates
#   the API rather than assuming our mocking is
#   correct
#  )
#
PyKCSS11_SOLIB='/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so'

class PyKCSS11_Classtests(unittest.TestCase):


    def test_class_accepts_a_slot(self,):
        with unittest.mock.patch('PyKCS11.PyKCS11Lib' ):
            out = mut.Algorithm(slot = unittest.mock.sentinel.SLOT )
        self.assertEqual(out.slot, unittest.mock.sentinel.SLOT )

    def test_class_is_subclassed_from_crypto(self,):
        self.assertTrue(issubclass( mut.Algorithm , RSAPrivateKey ))

    def test_class_default_key_index_is_zero(self,):
        with unittest.mock.patch('PyKCS11.PyKCS11Lib' ):
            out = mut.Algorithm(slot = unittest.mock.sentinel.SLOT )
        self.assertEqual(out.key, 0 )


    def test_class_accept_alternate_lokup_key_for_provkey(self,):
        with unittest.mock.patch('PyKCS11.PyKCS11Lib' ):
            out = mut.Algorithm(key = unittest.mock.sentinel.KEY ,slot = 0)
        self.assertEqual(out.key, unittest.mock.sentinel.KEY )


    def test_class_accepts_a_pin_for_unlocking_thekey(self,):
        with unittest.mock.patch('PyKCS11.PyKCS11Lib' ):
            out = mut.Algorithm(pin = unittest.mock.sentinel.PIN ,slot = 0)
        self.assertEqual(out.pin, unittest.mock.sentinel.PIN )


    def test_class_accepts_zero_as_valid_slot(self,):
        with unittest.mock.patch('PyKCS11.PyKCS11Lib' ) as x,\
             unittest.mock.patch.object(mut.Algorithm,'_resolve_slot',
            return_value=unittest.mock.sentinel.SLOT ) as x:

            out = mut.Algorithm(slot = 0 )
        self.assertEqual(out.slot, 0)
        x.assert_not_called()


    def test_class_creates_its_own_libary_handle(self,):
        with unittest.mock.patch('PyKCS11.PyKCS11Lib') as x:
            out = mut.Algorithm(slot=0 )

        x.assert_called_once()

    def test_class_accepts_a_token_argument_to_match_info_against(self,):
        with unittest.mock.patch('PyKCS11.PyKCS11Lib' ) as x,\
             unittest.mock.patch.object(mut.Algorithm, '_resolve_slot', return_value=unittest.mock.sentinel.SLOTX ):
            out = mut.Algorithm(token = unittest.mock.sentinel.TOKEN1 )
        self.assertEqual(out.slot, unittest.mock.sentinel.SLOTX )

    def test_dunder_resolve_slot_gets_list_of_slots_the_slot_data(self,):
        lib =  unittest.mock.MagicMock()
        with unittest.mock.patch('PyKCS11.PyKCS11Lib', return_value = lib):
            try:
                out = mut.Algorithm(token = unittest.mock.sentinel.TOKEN2 )
            except LookupError:pass
        lib.getSlotList.assert_called_once()

    def test_dunder_resolve_slot_gets_token_info_from_all_slots_the_slot_data(self,):
        avail_slots = list(range(10))

        lib =  unittest.mock.MagicMock()
        lib.get_tokeninfo = unittest.mock.MagicMock(return_value ={})
        lib.getSlotList = unittest.mock.MagicMock(return_value = avail_slots)
        with unittest.mock.patch('PyKCS11.PyKCS11Lib', return_value = lib):
            try:
                out = mut.Algorithm(token = {'x':unittest.mock.sentinel.TOKEN2} )
            except LookupError:pass
        lib.get_tokeninfo.assert_has_calls([ unittest.mock.call(s) for s in  avail_slots] )

    def test_dunder_resolve_slot_choses_a_slot_if_only_the_index_one_matches(self,):

        slot_data =  [ {'xyzzy':1}, {'serialnr':'123','manufacturer':'acme'} ]
        avail_slots = range(len(slot_data))

        lib =  unittest.mock.MagicMock()
        lib.getSlotList = unittest.mock.MagicMock(return_value = avail_slots)
        lib.get_tokeninfo = unittest.mock.MagicMock( side_effect = slot_data )
        with unittest.mock.patch('PyKCS11.PyKCS11Lib', return_value = lib):
            out = mut.Algorithm(token = {'serialnr':'123','manufacturer':'acme'} )

        lib.get_tokeninfo.assert_has_calls([ unittest.mock.call(s) for s in  avail_slots] )
        self.assertEqual(out.slot, 1 )


    def test_dunder_resolve_slot_choses_slot_0_if_only_index_zero_matches(self,):

        slot_data =  [{'serialnr':'456','manufacturer':'acme'}, {'serialnr':'123','manufacturer':'acme'} ]
        avail_slots = range(len(slot_data))

        lib =  unittest.mock.MagicMock()
        lib.getSlotList = unittest.mock.MagicMock(return_value = avail_slots)
        lib.get_tokeninfo = unittest.mock.MagicMock( side_effect = slot_data )
        with unittest.mock.patch('PyKCS11.PyKCS11Lib', return_value = lib):
            out = mut.Algorithm(token = {'serialnr':'456','manufacturer':'acme'} , )

        lib.get_tokeninfo.assert_has_calls([ unittest.mock.call(s) for s in  avail_slots] )
        self.assertEqual(out.slot, 0 )

    def test_dunder_resolve_slot_raises_if_there_are_mutiple_matches(self,):

        slot_data =  [{'serialnr':'456','manufacturer':'acme'}, {'serialnr':'456','manufacturer':'acme'} ]
        avail_slots = range(len(slot_data))

        lib =  unittest.mock.MagicMock()
        lib.getSlotList = unittest.mock.MagicMock(return_value = avail_slots)
        lib.get_tokeninfo = unittest.mock.MagicMock( side_effect = slot_data )
        with unittest.mock.patch('PyKCS11.PyKCS11Lib', return_value = lib):
            with self.assertRaises(mut.MultipleMatchingTokens):
                out = mut.Algorithm(token = {'serialnr':'456','manufacturer':'acme'} , )

    def test_dunder_resolve_slot_raises_if_there_are_No_matches(self,):
        slot_data =  [{'serialnr':'456','manufacturer':'acme'}, {'serialnr':'456','manufacturer':'acme'} ]
        avail_slots = range(len(slot_data))

        lib =  unittest.mock.MagicMock()
        lib.getSlotList = unittest.mock.MagicMock(return_value = avail_slots)
        lib.get_tokeninfo = unittest.mock.MagicMock( side_effect = slot_data )
        with unittest.mock.patch('PyKCS11.PyKCS11Lib', return_value = lib):
            with self.assertRaises(mut.NoMatchingTokens):
                out = mut.Algorithm(token = {'serialnr':'12','manufacturer':'acme'} , )


    def test_dunder_resolve_slot_choses_slot_1_0_only_the_index_zero_an_obsuce_tag(self,):

        slot_data =  [ {'xyzzy':1}, {'serialnr':'123','manufacturer':'acme'} ]
        avail_slots = range(len(slot_data))

        lib =  unittest.mock.MagicMock()
        lib.getSlotList = unittest.mock.MagicMock(return_value = avail_slots)
        lib.get_tokeninfo = unittest.mock.MagicMock( side_effect = slot_data )
        with unittest.mock.patch('PyKCS11.PyKCS11Lib', return_value = lib):
            out = mut.Algorithm(token = {'xyzzy':1} )

        lib.get_tokeninfo.assert_has_calls([ unittest.mock.call(s) for s in  avail_slots] )
        self.assertEqual(out.slot, 0 )


    def test_class_ctor_loads_the_wrapped_library(self,):
         lib  = unittest.mock.MagicMock()
         with unittest.mock.patch('PyKCS11.PyKCS11Lib', return_value = lib) as x:
            out = mut.Algorithm(slot=0 )

         lib.load.assert_called_once()



class PyKCSS11_InstanceTests(unittest.TestCase):

    def setUp(self,):
        self.slot = 0
        self.pin = unittest.mock.sentinel.PIN
        try:
            os.environ['PYKCS11LIB']
        except KeyError:
            os.environ['PYKCS11LIB'] = PyKCSS11_SOLIB
        self.out = mut.Algorithm(slot  = self.slot )

    def test_classes__enter__method_calls_open(self,):
        self.out.pin = self.pin
        with unittest.mock.patch.object(self.out,'open') as opensession:
            rv = self.out.__enter__()

        opensession.assert_called_once()
        self.assertIs(rv,self.out)


    def test_open_method_creates_a_session_and_unlocks_with_a_pin(self,):
        session  = unittest.mock.MagicMock()
        with unittest.mock.patch.object(self.out.lib,'openSession',
                                       return_value = session) as openSes:

           rv = self.out.open(self.pin)

        openSes.assert_called_with( self.slot, PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION )
        session.login.assert_called_with(self.pin)

    def test_open_method_call_a_s_second_time_raises_an_exception(self,):
        session  = unittest.mock.MagicMock()
        with unittest.mock.patch.object(self.out.lib,'openSession',
                                       return_value = session) as openSes:

            rv = self.out.open(self.pin)
            with self.assertRaises(mut.SessionAlreadyOpen):
                rv = self.out.open(self.pin)

        openSes.assert_called_with( self.slot, PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION )
        session.login.assert_called_with(self.pin)
        session.login.assert_called_once()


    def test_classes_exit_method_calls_close(self,):
        with unittest.mock.patch.object(self.out,'close') as closesession:
            rv = self.out.__exit__(None,None,None)

        closesession.assert_called_once()
        self.assertEqual(bool(rv), False)


    def test_class_close_method_raises_if_session_not_open(self,):
        with self.assertRaises(mut.SessionNotOpen):
            self.out.close()


    def test_class_close_method_closes_session(self,):
        session = unittest.mock.MagicMock()
        self.out.session = session
        self.out.close()
        session.logout.assert_called_once()
        session.closeSession.assert_called_once()
        self.assertIs(self.out.session, None)
        self.assertIs(self.out._privkey, None)


    def test__private_getprivkey_gets_the_asked_for_key_when_called_the_first_time(self,):
        session = unittest.mock.MagicMock()
        session.findObjects = unittest.mock.MagicMock(return_value = [ unittest.mock.sentinel.PRIVKEY])
        self.out.session = session
        rv = self.out.privkey
        session.findObjects.assert_called_with([(PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY)])
        self.assertEqual(rv, unittest.mock.sentinel.PRIVKEY)
        self.assertEqual(self.out._privkey, unittest.mock.sentinel.PRIVKEY)


    def test__private_getprivkey_gets_the_asked_for_key_when_called_the_first_time(self,):
        session = unittest.mock.MagicMock()
        session.findObjects = unittest.mock.MagicMock(return_value = [ unittest.mock.sentinel.PRIVKEY])
        self.out.session = session
        rv = self.out.privkey
        rv = self.out.privkey
        session.findObjects.assert_called_once()
        self.assertEqual(rv, unittest.mock.sentinel.PRIVKEY)



    def test__private_getprivkey_gets_the_asked_for_key_when_its_Not_idx_0(self,):
        session = unittest.mock.MagicMock()
        self.out.key = 1
        session.findObjects = unittest.mock.MagicMock(return_value = [None, unittest.mock.sentinel.PRIVKEY])
        self.out.session = session
        rv = self.out.privkey
        self.assertEqual(rv, unittest.mock.sentinel.PRIVKEY)
        self.assertEqual(self.out._privkey, unittest.mock.sentinel.PRIVKEY)
