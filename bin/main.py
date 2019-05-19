import multiprocessing

from setup_cython.bootstrap import app

if __name__ == '__main__':
    multiprocessing.freeze_support()
    app.run()
