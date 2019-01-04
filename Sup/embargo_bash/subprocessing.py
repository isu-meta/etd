import subprocess

def bash_command(cmd):
     subprocess.Popen(cmd, shell=True, executable='/bin/bash')

