from ahk import ahk

ahk.start()
ahk.ready()
ahk.execute(u"something = 10")
ahk.get(u"something")