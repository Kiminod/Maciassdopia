if ($IsWindows) {
    Write-Host "Running on Windows"

    $python_version = python --version
    if ($python_version -match "Python 3.12") {
        Write-Host "Python 3.12 is already installed."
    } else {
        $python_installer = "python-3.12.6-amd64.exe"
        if (-not (Test-Path $python_installer)) {
            Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe" -OutFile $python_installer
        }
        
        if ($args -contains "-s") {
            Write-Host "Starting silent installation of Python 3.12.6"
            Start-Process -FilePath $python_installer -ArgumentList "/quiet InstallAllUsers=0" -Wait
        } else {
            Start-Process -FilePath $python_installer -Wait
        }
    }

    python -m ensurepip
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

    python -m pip install Pillow-10.0.0-cp38-none-any.whl
} else {
    Write-Host "Running on Linux (WSL)"

    $distro = (cat /etc/os-release | grep "^ID=" | cut -d'=' -f2).Trim()

    if ($distro -eq "arch" -or $distro -eq "manjaro") {
        sudo pacman -Syyu
        sudo pacman -S base-devel --needed
        sudo pacman -S yay --noconfirm
        yay -S python38
        sudo pacman -S python-pip --noconfirm
        sudo pip3 install -r requirements.txt
        sudo pacman -S wine --noconfirm
    } else {
        sudo rm -f /var/lib/dpkg/lock /var/cache/apt/archives/lock /var/lib/apt/lists/lock
        sudo dpkg --add-architecture i386
        sudo apt-get update
        sudo apt-get install python3.12 -y
        sudo apt-get install python3-pip -y
        sudo pip3 install -r requirements.txt
        sudo apt-get install -y wine
    }

    $python_installer = "python-3.12.6.exe"
    if (-not (Test-Path $python_installer)) {
        sudo wget "https://www.python.org/ftp/python/3.12.6/python-3.12.6.exe" --no-check-certificate
    }

    if ($args -contains "-s") {
        Write-Host "Starting silent installation of Python 3.12.6"
        sudo wine cmd /c "python-3.12.6.exe /quiet InstallAllUsers=0"
    } else {
        sudo wine cmd /c "python-3.12.6.exe"
    }

    $wine_python = "/root/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python312-32/python.exe"
    if (Test-Path $wine_python) {
        sudo wine $wine_python -m pip install Pillow-10.0.0-cp38-none-any.whl
        sudo wine $wine_python -m pip install -r ./libraries/c2_requirements.txt
    } else {
        $wine_python_alt = "/root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python312-32/python.exe"
        sudo wine $wine_python_alt -m pip install Pillow-10.0.0-cp38-none-any.whl
        sudo wine $wine_python_alt -m pip install -r ./libraries/c2_requirements.txt
    }
}

Write-Host "Setup complete"
