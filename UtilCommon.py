import logging
logger = logging.getLogger(__name__)

import subprocess, os, shutil

def Which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def RunCommand(command):
    logger.debug('Command : "{0}"'.format(command))
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = p.communicate()
    map(lambda l : logger.debug(l), output.splitlines())
    map(lambda l : logger.error(l), error.splitlines())

def Delete(filepath):
    if os.path.exists(filepath):
        if os.path.isdir(filepath):
            shutil.rmtree(filepath)
            logger.debug('Remove directory : {0}'.format(filepath))
        else:
            os.remove(filepath)
            logger.debug('Remove file : {0}'.format(filepath))
