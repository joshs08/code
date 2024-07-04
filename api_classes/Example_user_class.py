import sys
sys.path.insert(0, '/home/colin/Documents/GitHub/code/source/gui')
from api import Api
import time
#from multiprocessing import Process,Pipe

#new
# import multiprocessing
# from ctypes import c_char_p
# s = multiprocessing.Manager().Value(c_char_p, '')
# event = multiprocessing.Event()

# def update(arg1):
#     time.sleep(5)
#     s.value = arg1  # updates global variable s
#     event.set() # show we have a new value

# def send(child_conn):
#     event.wait() # wait for new s value
#     msg = s.value
#     child_conn.send(msg)
#     child_conn.close()

def f(child_conn):
    tt = time.time()
    msg = "Time is {}".format(tt)#prints with timestamp
    child_conn.send(msg)
    child_conn.close()


# This class should be have the same name as the file and inherit the API class
# look at gui/api.py to see what functions can be redefined and called
class Example_user_class(Api):
    def __init__(self):
        self.off_count = 0

    # this runs at the start of sessoin
    def run_start(self):
        self.print_to_log("\nAPI success")

    # use this function
    def process_data_user(self, data):
        imaging = [state.name == "imaging_on" for state in data["states"]]
        if imaging == [True]:
            tt = time.time()
            self.print_message("Time is {}".format(tt))#prints with timestamp
            #new
            # x = "Time is {}".format(tt)
            # p1 = multiprocessing.Process(target=update, args=(x,))
            # p2 = multiprocessing.Process(target=send)
            # p1.start()
            # p2.start()
            # p1.join()
            # p2.join()
            
    def run_stop(self):
        self.print_to_log("\nMessage from config/user_classes/Example_user_class.py at the end of the run")
