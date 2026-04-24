import subprocess

def restart_service(command):
    subprocess.Popen(command)