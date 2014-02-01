from PySide.QtGui import QApplication
import sys

class App(QApplication):

    def __init__(self, argv):
        super(App, self).__init__(argv)

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
