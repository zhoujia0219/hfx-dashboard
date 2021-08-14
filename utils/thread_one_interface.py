# 对单接口需要采用多线程的类
import threading


class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

# 使用方法示例
# import time
# def demo(a):
#     global data
#     time.sleep(3)
#     return 123232323232323
#
# res = []
# data = []
# for i in range(4):
#     t=MyThread(demo,args=(i,))
#     res.append(t)
#     t.start()
# for j in res:
#     j.join()
#     data.append(j.get_result())
# print(data)
