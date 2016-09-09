"""Test AutoHotKey Control wrapper."""
import os, time#, random
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

# The methods of the Control class are not well suited to unit-tests as by their
# nature they interact with the windowing environment they are run in.
class Test_Control(unittest.TestCase):
    """Test ahk control access wrapper object."""

    def setUp(self):
        """Configure test environment."""
        self.script = ahk.Script()

    def test_00_delay(self):
        """Testing control delay decorator."""
        ctl = ahk.Control(self.script, store=False)
        # Set the control delay and check that it is set
        delay = 50
        ctl.set_delay(control=delay)
        self.assertEqual(ctl._cdelay, delay, msg="Set delay not stored?")
        # Mock out ahk.execute in the control module so no commands actually run
        with mock.patch('ahk.control.execute') as exc:
            outer_delay = ahk.get("A_ControlDelay")
            inner_delay = list() # Object in outer scope
            def store(cmd):
                """execute replacement for mock."""
                # Object in outer scope used in closure to store a value
                inner_delay.append(int(ahk.get("A_ControlDelay")))
                if 'send' not in cmd.lower():
                    #print cmd, inner_delay
                    ahk.execute(cmd)

            exc.side_effect = store # set store to be called when execute is
            # Call a delayed method and ensure that the stored delay is
            # in effect only in the method call
            ctl.send()
            inner_delay = inner_delay[-1] # Unwrap inner value
            self.assertNotEqual(outer_delay, inner_delay,
                msg="Inner delay {0} is the same as outer {1}!".format(
                    inner_delay, outer_delay))
            self.assertEqual(inner_delay, delay,
                msg="Inner delay {0} different than previously set {1}!".format(
                    inner_delay, delay))

    def test_01_init(self):
        """Testing control initialization."""
        # Mock out script instance
        scr = mock.Mock(spec=self.script)
        # Set winExist return to known value
        def effect(title, *args, **kwargs):
            if 'error' in title.lower():
                return None
            return 42
        scr.winExist.side_effect = effect
        # First test no store and parameter set
        inparams = ('title', 'text', 'extitle', 'extext')
        ctl = ahk.Control(scr, *inparams, store=False)
        outparams = ctl._params() #NOTE use of private method could break!
        self.assertEqual(inparams, outparams,
            msg="Retrieved params {0} don't match input {1}!".format(
                outparams, inparams))
        # Next check HWND storage behavior
        with self.assertRaises(NameError):
            ctl = ahk.Control(scr, title='error') # store=True but window doesn't exist
        scr.reset_mock()
        ctl = ahk.Control(scr, *inparams)
        self.assertEqual(ctl.hwnd, 42, msg="Wrong HWND stored?")
        outparams = ctl._params() #NOTE use of private method could break!
        title = outparams[0].lower()
        self.assertTrue('ahk_id' in title and '42' in title,
            msg="HWND param \"{0}\" incorrectly formatted!".format(title))
        self.assertFalse(''.join(outparams[1:]), # Extra params are set to ''
            msg="Retrieved params {0} contain unexpected value!".format(
                outparams[1:]))

    def tearDown(self):
        """Clean test environment."""
        self.script = None

# Assemble test suites
control_suite = unittest.TestLoader().loadTestsFromTestCase(Test_Control)
all_tests = unittest.TestSuite([
                                control_suite, 
                              ])
if __name__ == "__main__":
    # Run tests
    unittest.TextTestRunner(verbosity=2).run(all_tests)
