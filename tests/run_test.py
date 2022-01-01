import glob
from multiprocessing import Process
import subprocess


def execute_python(f):
    test = subprocess.run(["python3", f], capture_output=True)
    if test.stderr:
        print(f"{f}:\n{test.stderr}")
    else:
        print(f"{f}")


liste = glob.glob("test*.py")
liste += glob.glob("catriona*.py")
print(liste)
for f in liste:
    p = Process(target=execute_python, args=(f,))
    p.start()
