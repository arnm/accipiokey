#! /usr/bin/env python

from accipiokey import AccipioKeyAppController
import sys


if __name__ == '__main__':
    app = AccipioKeyAppController(sys.argv)
    sys.exit(app.exec_())
