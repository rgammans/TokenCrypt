import unittest
import unittest.mock

import TokenCrypt.pkcs11 as mut


class PyKCSS11_Classtests(unittest.TestCase):


    def test_class_accepts_a_slot(self,):
        with unittest.mock.patch('PyKCS11.PyKCS11Lib' ):
            out = mut.Algorithm(slot = unittest.mock.sentinel.SLOT )
        self.assertEqual(out.slot, unittest.mock.sentinel.SLOT )

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


    @unittest.skip('nyi')
    def test_class_close_method_closes_session(self,):
        self.fail()

    @unittest.skip('nyi')
    def test_classes__enter__method_inits_session(self,):
        self.fail()

    @unittest.skip('nyi')
    def test_classes_sexit_method_calls_close(self,):
        self.fail()

