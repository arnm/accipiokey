import os
from subprocess import call

ui_dir = './ui/'
output_dir = '/home/alexei/Dev/python/workspace/accipiokey/accipiokey/gui/ui/'
files = os.listdir(ui_dir)

for file in files:
    if '.ui' in file:
        print('File:', file)
        name = os.path.splitext(file)[0]
        call(['pyside-uic', ui_dir + file, '-o', output_dir + name + '.py'])
