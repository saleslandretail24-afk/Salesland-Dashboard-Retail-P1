Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\Lenovo\Documents\Mi dashboard"
WshShell.Run "node server.js", 0, False
