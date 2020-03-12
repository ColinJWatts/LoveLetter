import inspect
import sys

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print ("*** Method not implemented: %s at line %s of %s" % (method, line, fileName))
    sys.exit(1)


def raiseException(msg):
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print ("*** Exception thrown: %s at line %s of %s with message: %s" % (method, line, fileName, msg))
    sys.exit(1)