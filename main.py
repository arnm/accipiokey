
if __name__ == '__main__':
    from accipiokey.app import AccipioKeyApp
    from mongoengine import connect
    connect('accipiokey')
    AccipioKeyApp().run()
