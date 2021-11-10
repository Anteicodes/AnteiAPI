import unittest

class Test(unittest.TestCase):
    def importt(self):
        try:
            from . import AnteiAPI, Login
            return True
        except Exception as e:
            print(e)
            return False
    def test_import(self):
        self.assertTrue(self.importt())

if __name__ == '__main__':
    unittest.main()