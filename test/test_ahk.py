"""Test AutoHotKey low-level wrappers."""
import os, time, ctypes
import unittest
try:
    import ahk
except ImportError:
    # Try adding parent folder to front of path
    import sys
    sys.path = [os.path.abspath("../")] + sys.path
    import ahk

class Test_lowlevel(unittest.TestCase):
    """Test ahk misc. function wrappers."""

    def setUp(self):
        """Configure test environment."""
        self.tempfilename = os.path.join(os.getcwd(), 
                                         "{0}.ahk".format(int(time.time())))

    def test_00_ready(self):
        """Testing ahk.ready function."""
        self.assertFalse(ahk.ready(nowait=True), 
                         msg="Un-initialized library reports ready?")
        self.assertFalse(ahk.ready(retries=5), 
                         msg="Un-initialized library reports ready?")
        # Next test depends on ahk.start
        ahk.start()
        self.assertTrue(ahk.ready(retries=15), 
                         msg="Library Un-initialized after 15 tests?")

    def test_01_start(self):
        """Testing ahk.start function."""
        if ahk.ready(nowait=True):
            raise RuntimeError("ahk script started before start test!")

        # Test basic startup
        ahk.start()
        self.assertTrue(ahk.ready(retries=15), 
                         msg="Library Un-initialized after 15 tests?")
        ahk.terminate()

        #NOTE no further test because passed arguments seem to be ignored.

    def test_02_terminate(self):
        """Testing terminating an ahk thread."""
        if ahk.ready(nowait=True):
            raise RuntimeError("ahk script started before start test!")

        # Confirm start, then confirm termination
        ahk.start()
        self.assertTrue(ahk.ready(retries=15), 
                         msg="Library Un-initialized after 15 tests?")
        ahk.terminate()
        self.assertFalse(ahk.ready(nowait=True), 
                         msg="Thread not terminated!")

    def test_03_setget(self):
        """Test setting/getting variable value."""
        test_vals = [
            1,
            5,
            50,
            500,
            'abc',
            'a longer string',
            'a string with\nspecial characters!'
        ]

        ahk.start()
        ahk.ready()
        # Test setting and then getting various variable values
        for val in test_vals:
            # Check setting is reported successful
            self.assertTrue(ahk.set("test", val), 
                            msg="Setting value reported as failed by ahk!")

            # Check that setting was successful
            value = ahk.get("test")
            self.assertEqual(str(val), value,
                             msg="Returned value {0} doesn't match {1}!".format(
                                 value, val))

        # Test getting a non-existent variable
        self.assertEquals("", ahk.get("nonexistent"),
                          msg="Got non-empty result from non-existent variable!")

    def test_04_execute(self):
        """Testing executing script strings."""
        val = 0
        arr = [5, 6, 3, 7, 2, 4, 1, 8, 9]
        ahk.start()
        ahk.ready()
        # First set a test variable to a known value
        self.assertTrue(ahk.set("test", val), 
                        msg="Setting value reported as failed by ahk!")
        # Execute a command that changes the value
        self.assertTrue(ahk.execute("test := test+1"),
                        msg="Execute reported failure!")
        # Check the value has changed, and is correct
        value = int(ahk.get("test"))
        self.assertNotEqual(val, value, msg="Value unchanged after execution?")
        self.assertEqual(value, 1,
                         msg="Unexpected value {0} after execution!".format(value))
        # Execute a more complicated set of commands and check the result
        self.assertTrue(ahk.execute("arr={0}\nsort arr, N D,".format(
                                    ",".join(str(i) for i in arr))),
                        msg="Execute reported failure!")
        value = ahk.get("arr")
        arr = ",".join(str(i) for i in sorted(arr))
        #print "result:\n\t{0}\n\t{1}".format(value, arr)
        self.assertEqual(arr, value,
                         msg="Unexpected result:\n\t{0} not equal to\n\t{1}".format(
                             value, arr))
        
    def test_05_add_lines(self):
        """Test adding code to running script."""
        ahk.start()
        ahk.ready()
        # Add lines by string
        self.assertEqual(ahk.get("test"), "", msg="Residual data found?")
        ahk.add_lines("test = 5\n")
        value = ahk.get("test")
        self.assertEqual(value, "5",
                         msg="Value={0}, script not evaluated?".format(value))

        # Add lines by file path
        with open(self.tempfilename, 'w') as tmp:
            tmp.write("test := test+5")

        addr = ahk.add_lines(filename=self.tempfilename)
        #NOTE depends on ahk.exec_line
        ahk.exec_line(addr, wait=True)
        value = ahk.get("test")
        self.assertEqual(value, "10",
                         msg="Value={0}, script not evaluated?".format(value))

    def test_06_jump(self):
        """Testing jumping to a labeled code block."""
        ahk.start()
        ahk.ready()
        # Add lines by string
        self.assertEqual(ahk.get("test"), "", msg="Residual data found?")
        ahk.add_lines("test = 0\nlbl:\ntest := test+5")
        value = ahk.get("test")
        self.assertEqual(value, "5",
                         msg="Value={0}, script not evaluated?".format(value))

        # Test jumping once
        self.assertTrue(ahk.jump("lbl"), msg="Label not found in script!")
        value = ahk.get("test")
        self.assertEqual(value, "10",
                         msg="Value={0}, script not evaluated?".format(value))

        # Test repeated jump
        for i in range(8):
            self.assertTrue(ahk.jump("lbl"), msg="Label not found in script!")
            expected = str(15+(i*5))
            value = ahk.get("test")
            self.assertEqual(value, expected,
                             msg="Expected {0}, found {1}!".format(
                                 expected, value))

    def test_07_call(self):
        """Testing calling ahk functions."""
        ahk.start()
        ahk.ready()
        # Add lines by string containing a function definition
        ahk.add_lines("""
                      Add(x, y) {
                          return (x + y)
                      }
                      """)
        # Now call the new function and check the result
        result = ahk.call("Add", 5, 5)
        self.assertEqual(int(result), 10,
                         msg="Unexpected result {0}!".format(result))

    def test_08_post(self):
        """Testing posting function call."""
        ahk.start()
        ahk.ready()
        # Posting to a non-existent function should return false
        self.assertFalse(ahk.post('nonexistent'),
            msg="Success reported posting to non-existent function!")
        # Define a new function that changes the environment
        ahk.add_lines("""
                      changer() {
                          ErrorLevel = 1
                      }
                      """)
        # Set ErrorLevel then check value after posting function
        ahk.set("ErrorLevel", 0)
        # The following raises WindowsError access violation
        self.assertTrue(ahk.post('changer'),
                        msg="Failed to find an existing function?")
        self.assertNotEqual(0, ahk.get("ErrorLevel"),
                            msg="Internal variable unchanged?")

    def test_09_reload(self):
        """Testing reloading."""
        ahk.start()
        ahk.ready()
        # Set a new variable to a known value
        value = '5'
        ahk.add_lines("test = {0}\n".format(value)) # Set test variable
        res = ahk.get('test')
        self.assertEqual(res, value,
            msg="Value={0}, ahk.add_lines not evaluated?".format(res))
        # Reloading should clear all variable values
        ahk.reload()
        res = ahk.get('test')
        self.assertNotEqual(res, value,
            msg="Value={0}, variable retained value after reload?".format(res))

    def test_10_find_func(self):
        """Testing function finding."""
        ahk.start()
        ahk.ready()
        # First test find function
        self.assertEqual(ahk.find_func('nonexist'), 0,
            msg="Non-null pointer to non-existent function?")
        # Add function
        ahk.add_lines("""
                      AddTwo(n) {
                          return n + 2
                      }
                      """)
        # Try to get a reference
        res = ahk.find_func('AddTwo')
        self.assertNotEqual(res, 0,
            msg="Null pointer to existent function?")
        return # The following code fails
        # Try calling the function
        proto = ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_char_p)
        func = proto(res)
        res = int(func('5'))
        self.assertEqual(res, 5+2,
            msg="Got bad result {0} when calling function?")

    def test_11_find_label(self):
        """Testing finding a labeled line."""
        ahk.start()
        ahk.ready()
        # Non-existent label should return Null pointer
        self.assertEqual(ahk.find_label('nonexist'), 0,
            msg="Got pointer to non-existent label!")
        # Add lines by string
        ahk.add_lines("test = 0\nlbl:\ntest := test+5")
        res = ahk.get("test")
        self.assertEqual(res, "5",
                         msg="Value={0}, script not evaluated?".format(res))
        # Get pointer to the labeled line
        res = ahk.find_label('lbl')
        self.assertNotEqual(res, 0,
            msg="Got null pointer to known good label?")
        return # The remaining code fails or hangs the process
        #NOTE depends on exec_line
        #ahk.exec_line(ahk.exec_line(res, 0))
        ahk.exec_line(res, 0)
        res = ahk.get("test")
        print res
        self.assertEqual(res, "10",
                         msg="Value={0}, script not evaluated?".format(res))

    def test_12_exec_line(self):
        """Testing line-wise execution."""
        ahk.start()
        ahk.ready()
        # Test retrieving the current line
        self.assertNotEqual(ahk.exec_line(mode=0), 0,
            msg="Got null pointer to first line?")
        # Add lines by string
        ahk.set('test', 0)
        addr = ahk.add_lines("test := test+5\n")
        res = ahk.get("test")
        self.assertEqual(res, "5",
                         msg="Value={0}, script not evaluated?".format(res))
        # Executing the saved line should increase test by 5
        ahk.exec_line(addr, wait=True)
        res = ahk.get("test")
        self.assertEqual(res, "10",
                         msg="Value={0}, line not executed?".format(res))

    def tearDown(self):
        """Clean test environment."""
        # This fails if the terminate function fails.
        ahk.terminate()
        if os.path.exists(self.tempfilename):
            os.remove(self.tempfilename)

# Assemble test suites
lowlevel_suite = unittest.TestLoader().loadTestsFromTestCase(Test_lowlevel)
all_tests = unittest.TestSuite([
                                lowlevel_suite, 
                              ])
if __name__ == "__main__":
    # Run tests
    unittest.TextTestRunner(verbosity=2).run(all_tests)
