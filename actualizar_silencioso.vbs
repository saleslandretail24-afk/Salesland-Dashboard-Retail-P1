Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\Lenovo\Documents\Mi dashboard"
WshShell.Run "python ""C:\Users\Lenovo\Documents\Mi dashboard\actualizar_datos.py""", 0, False
