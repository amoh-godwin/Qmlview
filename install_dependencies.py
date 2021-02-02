import sys
import os

_, os_name = sys.argv

if os_name == 'windows-latest':
    # install github cli
    cmd0 = 'powershell Set-ExecutionPolicy Bypass -Scope Process -Force; .\ChocolateyInstallNonAdmin.ps1 choco --version'
    cmd = "choco install gh -y"
    os.system(cmd0)
    os.system(cmd)
elif os_name == 'ubuntu-latest':
    # install github cli
    cmd0 = "sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0"
    cmd1 = "sudo apt-add-repository https://cli.github.com/packages"
    cmd2 = "sudo apt update"
    cmd3 = "sudo apt install gh"
    os.system(cmd0)
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
else:
    cmd = "brew install gh"
    os.system(cmd)
