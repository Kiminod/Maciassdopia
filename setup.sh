#!/usr/bin/env bash

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    FILE=/etc/lsb-release
    if test -f "$FILE"; then
        echo "/etc/lsb-release exist"
        export DISTRIB=$(awk -F= '/^DISTRIB_ID/{print $2}' /etc/lsb-release | tr -d \")
    else
        export DISTRIB="Not Arch"
        echo "/etc/lsb-release doesn't exist"
    fi

    if [[ ${DISTRIB} = "Arch"* || ${DISTRIB} = "ManjaroLinux"* ]]; then
        sudo pacman -Syyu
        sudo pacman -S base-devel --needed
        sudo pacman -S yay --noconfirm
        yay -S python38
        sudo pacman -S python-pip --noconfirm
        sudo pip3 install -r requirements.txt
        sudo pacman -S wine --noconfirm
    else
        rm /var/lib/dpkg/lock
        rm /var/cashe/apt/archives/lock
        rm /var/lib/apt/lists/lock
        sudo dpkg --add-architecture i386
        sudo apt-get update
        sudo apt-get install python3.12 -y
        sudo apt-get install python3-pip -y
        sudo pip3 install -r requirements.txt
        sudo apt-get install -y wine
    fi

    FILE=python-3.12.6.exe
    if test -f "$FILE"; then
        echo "$FILE already exist."
    else
        sudo wget https://www.python.org/ftp/python/3.12.6/python-3.12.6.exe --no-check-certificate
    fi

    arg1=$1
    arg2="-s"
    if [ "$arg1" == "$arg2" ]; then
        echo "Begginning silent Python 3.12.6 Installation"
        sudo wine cmd /c python-3.12.6.exe /quiet InstallAllUsers=0
    else
        sudo wine cmd /c python-3.12.6.exe
    fi

    if [[ ${DISTRIB} = "Arch"* || ${DISTRIB} = "ManjaroLinux"* ]]; then
        sudo wine "/root/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python312-32/python.exe" -m pip install -r ./libraries/c2_requirements.txt
    elif [[ ${DISTRIB} = "Not Arch"* ]]; then
        FILE="/root/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python312-32/python.exe"
        if test -f "$FILE"; then
            sudo wine "/root/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python312-32/python.exe" -m pip install Pillow-10.0.0-cp38-none-any.whl
            sudo wine "/root/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python312-32/python.exe" -m pip install -r ./libraries/c2_requirements.txt
        else
            sudo wine "/root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python312-32/python.exe" -m pip install Pillow-10.0.0-cp38-none-any.whl
            sudo wine "/root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python312-32/python.exe" -m pip install -r ./libraries/c2_requirements.txt
        fi
    fi
fi

echo "Done"
