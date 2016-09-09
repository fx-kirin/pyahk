"""Test AutoHotKey script wrappers."""
import os, time, random
import unittest
try:
    # The mock library was accepted as part of the Python Std. Library in V3.3
    from unittest import mock
except ImportError:
    # Fall back to the back-ported version
    import mock
try:
    import ahk
except ImportError:
    # Try adding parent folder to front of path
    import sys
    sys.path = [os.path.abspath("../")] + sys.path
    import ahk

class Test_Function(unittest.TestCase):
    """Test ahk function wrapper object."""

    def test_00_Function(self):
        """Testing Function wrapper object."""
        tests = (
            (1, 1),
            ('2', 2),
            ('3', '4'),
            (10, 11),
            (100, 1000),
        )
        # Startup
        ahk.start()
        ahk.ready()
        # Define our function
        add = ahk.Function('add', int, '(x, y)', 'return x + y')
        # Test with an assortment of values
        for x, y in tests:
            result = add(x, y)
            expect = int(x) + int(y)
            self.assertEqual(result, expect,
                             msg="Unexpected result {0}, expected {1}!".format(
                             result, expect))

        with self.assertRaises(ValueError):
            # Error during type conversion
            add('abc', 'efg')
        # Cleanup
        ahk.terminate()

# The methods of the Script class are not well suited to unit-tests as by their
# nature they interact with the windowing environment they are run in.
class Test_Script(unittest.TestCase):
    """Test ahk script wrapper object."""

    def setUp(self):
        """Configure test environment."""
        pass

    def test_00_init(self):
        """Testing that script was initialized correctly."""
        scr = ahk.Script()
        self.assertTrue(ahk.ready(nowait=True),
            msg="AHK not ready after init?")
        self.assertIsNotNone(scr.Clipboard, 
            msg="Special Clipboard variable not initialized!")
        self.assertIsNotNone(scr.ErrorLevel, 
            msg="Special ErrorLevel variable not initialized!")

    def test_01_ScriptFunction(self):
        """Testing creating and using a Function through a Script object."""
        tests = (
            (1, 1),
            ('2', 2),
            ('3', '4'),
            (10, 11),
            (100, 1000),
        )
        script = ahk.Script()
        # Define our good function
        add = script.function('add', int, '(x, y)', 'return x + y')
        self.assertIsInstance(add, ahk.Function,
                              msg="Non-function {0} returned!".format(add))
        # Test expected exceptions
        with self.assertRaises(AttributeError):
            script.function('_badname')
            script.function('function')
            script.function('add')
        # Test with an assortment of values
        for x, y in tests:
            result = script.add(x, y)
            expect = int(x) + int(y)
            self.assertEqual(result, expect,
                             msg="Unexpected result {0}, expected {1}!".format(
                             result, expect))

        with self.assertRaises(ValueError):
            # Error during type conversion
            script.add('abc', 'efg')

    def test_02_ScriptVariable(self):
        """Testing creating and using variables through a Script object."""
        value = 5
        script = ahk.Script()
        # Define our good variable
        script.variable('test', int, value)
        # Test expected exceptions
        with self.assertRaises(AttributeError):
            script.function('_badname')
            script.function('function')
            script.function('test')
        # Test getting variable value
        self.assertEqual(script.test, value,
             msg="Variable value {0} doesn't match expected {1}!".format(
                 script.test, value))
        # Test setting variable value
        value = 10
        script.test = 10
        self.assertEqual(script.test, value,
             msg="Variable value {0} doesn't match expected {1}!".format(
                 script.test, value))
        # Test outside modification
        ahk.execute("test := test+5\n")
        self.assertEqual(script.test, value+5,
             msg="Variable value {0} doesn't match expected {1}!".format(
                 script.test, value+5))

    def test_03_convert_color(self):
        """Testing conversion of hex color."""
        scr = ahk.Script()
        for i in range(10):
            t = tuple([random.randint(0, 255) for i in range(3)])
            h = '0x' + ''.join('{0:02x}'.format(c) for c in t)
            res = scr.convert_color(h)
            #print res, t, h
            self.assertEqual(res, t,
                msg="Re-converted color {0} doesn't match {1} ({2})!".format(
                    res, t, h))

    def test_04_waitPixel(self):
        """Testing waiting for a pixel."""
        # Test waiting for a specific pixel value
        with mock.patch.object(ahk.Script, 'getPixel') as getpx:
            target = (10, 10, 10)
            threshold = 0.005 # 0.5% threshold
            interval = 0.01 # no wait since values are canned
            # Setup getpx with canned return values for our test
            getpx.side_effect = [
                (50, 50, 50), # Far away
                (20, 20, 20), # Closer
                (13, 13, 13), # Just outside threshold
                (11, 11, 11), # Within threshold
                (10, 10, 10), # Extra equal value
            ]
            # Test our object
            scr = ahk.Script()
            scr.waitPixel(color=target, threshold=threshold, interval=interval)
            self.assertTrue(getpx.called, msg="Mock wasn't called?")
            self.assertEqual(getpx.call_count, 4,
                msg="getPixel mock called {0} times instead of 4.".format(
                    getpx.call_count))

        # Next test waiting for any different pixel value
        with mock.patch.object(ahk.Script, 'getPixel') as getpx:
            threshold = 0.008 # 0.8% threshold
            interval = 0.01 # no wait since values are canned
            # Setup getpx with canned return values for our test
            getpx.side_effect = [
                (10, 10, 10), # Extra equal value
                (11, 11, 11), # Within threshold
                (12, 12, 12), # Within threshold
                (13, 13, 13), # Just outside threshold
                (50, 50, 50), # Far away
            ]
            # Test our object
            scr = ahk.Script()
            scr.waitPixel(threshold=threshold, interval=interval)
            self.assertTrue(getpx.called, msg="Mock wasn't called?")
            self.assertEqual(getpx.call_count, 4,
                msg="getPixel mock called {0} times instead of 4.".format(
                    getpx.call_count))

    def test_05_winActive(self):
        """Testing IfWinActive wrapper."""
        script = ahk.Script()
        # Test that non-existent window isn't found
        name = "non-existent-{0}".format(time.time())
        result = script.winActive(name)
        self.assertEqual(result, None,
                         msg="Found unexpected window with name \"{0}\"!".format(
                             name))
        # Test that an active window is findable
        result = script.winActive("A") # "A" is the current active window
        self.assertNotEqual(result, None,
                            msg="Can't find an active window?")

    def test_06_winExist(self):
        """Testing IfWinExist wrapper."""
        script = ahk.Script()
        # Test that non-existent window isn't found
        name = "non-existent-{0}".format(time.time())
        result = script.winExist(name)
        self.assertEqual(result, None,
                         msg="Found unexpected window with name \"{0}\"!".format(
                             name))
        # Test that an active window is findable
        result = script.winExist("A") # "A" is the current active window
        self.assertNotEqual(result, None,
                            msg="Can't find an active window?")

    def tearDown(self):
        """Clean test environment."""
        pass

# Assemble test suites
function_suite = unittest.TestLoader().loadTestsFromTestCase(Test_Function)
script_suite = unittest.TestLoader().loadTestsFromTestCase(Test_Script)
all_tests = unittest.TestSuite([
                                function_suite, 
                                script_suite, 
                              ])
if __name__ == "__main__":
    # Run tests
    unittest.TextTestRunner(verbosity=2).run(all_tests)
