import unittest

import TokenCrypt.pkcs11 as mut


class PyKCSS11_Classtests(unittest.TestCase):


    def test_class_accepts_a_slot(self,):
         out = mut.PyKCS11(slot = unittest.mock.sentinel.SLOT )

    def test_class_accepts_a_dict_to_match_info_agaisnt(self,):
        self.fail()

    def test_class_searches_for_slor_if_givev_a_dict(self,):
        self.fail()

    def test_class_raises_an_exeption_if_slot_not_matched(self,):
        self.fail()


    def test_class_close_method_closes_session(self,):
        self.fail()

    def test_classes__enter__method_inits_session(self,):
        self.fail()

    def test_classes_sexit_method_calls_close(self,):
        self.fail()

