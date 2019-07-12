import unittest
import unittest.mock

import TokenCrypt.pkcs11 as mut


class PyKCSS11_Classtests(unittest.TestCase):


    def test_class_accepts_a_slot(self,):
        out = mut.Algorithm(slot = unittest.mock.sentinel.SLOT )
        self.assertEqual(out.slot, unittest.mock.sentinel.SLOT )

    def test_class_accepts_zero_as_valid_slot(self,):
        with unittest.mock.patch.object(mut.Algorithm,'_resolve_slot', 
            return_value=unittest.mock.sentinel.SLOT ) as x:

            out = mut.Algorithm(slot = 0 )
        self.assertEqual(out.slot, 0)
        x.assert_not_called()


    def test_class_creates_its_own_libary_handle(self,):
        with unittest.mock.patch('PyKCS11.PyKCS11Lib') as x:
            out = mut.Algorithm(slot=0 )

        x.assert_called_once()

    def test_class_accepts_a_token_argument_to_match_info_against(self,):
        with unittest.mock.patch.object(mut.Algorithm, '_resolve_slot', return_value=unittest.mock.sentinel.SLOTX ):
            out = mut.Algorithm(token = unittest.mock.sentinel.TOKEN1 )
        self.assertEqual(out.slot, unittest.mock.sentinel.SLOTX )

    def test_dunder_resolve_slot_gets_list_of_slots_the_slot_data(self,):
        lib =  unittest.mock.MagicMock()
        with unittest.mock.patch('PyKCS11.PyKCS11Lib', return_value = lib):
            out = mut.Algorithm(token = unittest.mock.sentinel.TOKEN2 )
        lib.get_slots.assert_called_once()



    @unittest.skip('nyi')
    def test_class_searches_for_slor_if_givev_a_dict(self,):
        self.fail()

    @unittest.skip('nyi')
    def test_class_raises_an_exeption_if_slot_not_matched(self,):
        self.fail()


    @unittest.skip('nyi')
    def test_class_close_method_closes_session(self,):
        self.fail()

    @unittest.skip('nyi')
    def test_classes__enter__method_inits_session(self,):
        self.fail()

    @unittest.skip('nyi')
    def test_classes_sexit_method_calls_close(self,):
        self.fail()

