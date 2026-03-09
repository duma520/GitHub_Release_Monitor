cls
rmdir /s /q build
rmdir /s /q dist

pyinstaller --windowed  --noconfirm  --icon=icon.ico --add-data "icon.ico;." GitHub_Release_Monitor.py