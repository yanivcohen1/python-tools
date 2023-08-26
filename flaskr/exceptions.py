import sys
import os
import traceback

def fun(ins):
    b = 5
    b/ins
    print('end fun')

try:
    fun(0)
except Exception as ex :
    print("error desc: ", ex)
    print("full error path:")
    traceback.print_exc()

print("********************")

try:
    ser = 5/0
    # raise Exception("can't divide by zero")
except Exception as ex:
    print("'exceptions' module: Error (%s)." % str(ex))
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    # for forword the error
    # raise Exception(str(ex))
