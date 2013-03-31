# encoding: utf-8
import subprocess
import sys


class Platform(object):
    def __init__(self):
        self.darwin = sys.platform.startswith('darwin')
        self.windows = sys.platform.startswith('win')

    def copy_command(self):
        if self.darwin:
            return 'pbcopy'
        else:
            return 'xclip -selection clipboard'

    def copy(self, value):
        p = subprocess.Popen(self.copy_command(), stdin=subprocess.PIPE)
        p.stdin.write(value)
        p.stdin.close()
        return value

    def open_command(self):
        return 'start' if self.windows else 'open'

    def open(self, file_path):
        subprocess.call(
            [self.open_command(), file_path],
            stdout=subprocess.PIPE)
        return file_path

    def edit(self, file_path):
        return self.open(file_path)
