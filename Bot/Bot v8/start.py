import subprocess

if __name__ == "__main__":
	subprocess.Popen("main.py", shell=True)
	print("True")
	subprocess.Popen("menu.py", shell=True)
	subprocess.Popen("supmenu.py", shell=True)
	subprocess.Popen("dialog.py", shell=True)
	subprocess.Popen("getOrders.py", shell=True)
	raise SystemExit(1)