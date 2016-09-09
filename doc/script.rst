Function and Script wrappers
============================
These are higher-level wrappers representing an AHK function and an AHK script.
A Function object instance is transparently callable from either Python or AHK.
A Script object handles initialization automatically, provides transparent
variable access, and convenience wrappers around some AHK commands.

classes
-------
   * :class:`.Function`
   * :class:`.Script`
       * :meth:`.Script.variable`
       * :meth:`.Script.function`
       * :meth:`.Script.send`
       * :meth:`.Script.click`
       * :meth:`.Script.winActivate`
       * :meth:`.Script.winActive`
       * :meth:`.Script.winExist`
       * :meth:`.Script.waitActive`
       * :meth:`.Script.waitWindow`
       * :meth:`.Script.convert_color`
       * :meth:`.Script.getPixel`
       * :meth:`.Script.waitPixel`
       * :meth:`.Script.message`
       * :meth:`.Script.msgResult`

Function
^^^^^^^^
.. autoclass:: ahk.Function
    :members:

Script
^^^^^^
.. autoclass:: ahk.Script
    :members:

