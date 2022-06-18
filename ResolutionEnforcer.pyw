# Windows
from psutil import Process
from win32gui import GetWindowText, GetForegroundWindow
from win32process import GetWindowThreadProcessId
from win32api import ChangeDisplaySettings
from win32con import DM_PELSWIDTH, DM_PELSHEIGHT
from pywintypes import DEVMODEType

# Python
from time import sleep
from configparser import ConfigParser
from os import path, _exit, startfile

# Options


class options:
    file = f'{path.dirname(__file__)}/Options.ini'

    def get():
        config = ConfigParser()
        config.read(options.file)
        return config

    def exist():
        if path.exists(options.file) is False:
            with open(options.file, 'w') as f:
                f.write('''; Configuration file generated by Resolution Enforcer.

[General]
; Set the delay between application checks in seconds.
; Increase this value if you experience high CPU usage.
Delay = 0.1  

[Applications]
; Title or Executable Name = Resolution
Example.exe = 0x0''')
            startfile(options.file, 'open')
            _exit(0)

# Get the title and executable name from an active window.

def get_window():
    HWND = GetForegroundWindow()
    PID = GetWindowThreadProcessId(HWND)[1]
    title = GetWindowText(HWND)
    executable = path.split(path.abspath(Process(PID).exe()))[1]
    return (title, executable)

# Filter out applications to enforce resolutions on.

def enforce_resolution():
    enforce = False
    while True:
        try:
            config = options.get()
            sleep(float(config['General']['Delay']))

            title, executable = get_window()

            if executable == 'ApplicationFrameHost.exe':
                if title in config['Applications']:
                    if enforce is False:
                        resolution = config['Applications'][str(title)]
                        enforce = True

            elif executable in config['Applications']:
                if enforce is False:
                    resolution = config['Applications'][str(executable)]
                    enforce = True

            else:
                resolution = '0x0'

            height, width = resolution.split('x')
            resolution = DEVMODEType()
            resolution.PelsWidth, resolution.PelsHeight = int(
                height.strip()), int(width.strip())
            resolution.Fields = DM_PELSWIDTH | DM_PELSHEIGHT

            if enforce:
                ChangeDisplaySettings(resolution, 0)
                break
        except KeyboardInterrupt:
            _exit(1)
        except:
            pass    
    restore_resolution()

# Restore the default desktop resolution.

def restore_resolution():
    restore = False
    while True:
        try:
            config = options.get()
            sleep(float(config['General']['Delay']))

            try:
                title, executable = get_window()
            except:
                title, executable = None, None

            if executable == 'ApplicationFrameHost.exe':
                if title not in config['Applications']:
                    restore = True

            elif executable not in config['Applications']:
                restore = True

            if restore:
                ChangeDisplaySettings(None, 0)
                break
        except KeyboardInterrupt:
            _exit(1)
        except:
            pass       
    enforce_resolution()

def main():
    options.exist()
    enforce_resolution()


if __name__ == '__main__':
    main()
