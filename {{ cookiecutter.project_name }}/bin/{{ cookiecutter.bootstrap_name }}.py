from logzero import logger
import multiprocessing
import os
import sys
import click

try:
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

if sys.platform.startswith('win'):
    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    forking.Popen = _Popen


@click.command()
@click.option("--cmd", default='server', help="Run Server")
def run(cmd):
    if 'server' == cmd:
        logger.info('Server Started')
    if 'agent' == cmd:
        logger.info('Agent Started')


if __name__ == '__main__':
    multiprocessing.freeze_support()
    logger.info('Application Started')
    run()
