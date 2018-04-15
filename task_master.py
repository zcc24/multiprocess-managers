# task_master.py
# coding=utf-8
import random, time, Queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support

#发送任务的队列
task_queue = Queue.Queue()
# 接收结果的队列:
result_queue = Queue.Queue()
def return_task_queue():
    global task_queue
    return task_queue  # 返回发送任务队列
def return_result_queue ():
    global result_queue
    return result_queue # 返回接收结果队列
# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
def test():
    # 把两个Queue都注册到网络上, callable参数关联了Queue对象,它们用来进行进程间通信，交换对象
    #QueueManager.register('get_task_queue', callable=lambda: task_queue)
    #QueueManager.register('get_result_queue', callable=lambda: result_queue)
    QueueManager.register('get_task_queue', callable=return_task_queue)
    QueueManager.register('get_result_queue', callable=return_result_queue)
    # 绑定端口5000, 设置验证码'abc':
    #manager = QueueManager(address=('', 5000), authkey=b'abc')
    # windows需要写ip地址
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
    manager.start()  # 启动Queue:
    # 获得通过网络访dd问的Queue对象:
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    for i in range(10):   # 放几个任务进去:
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)
    # 从result队列读取结果:
    print('Try get results...')
    for i in range(10):
        # 这里加了异常捕获
        try:
            r = result.get(timeout=5)
            print('Result: %s' % r)
        except Queue.Empty:
             print('result queue is empty.')
    # 关闭:
    manager.shutdown()
    print('master exit.')
if __name__=='__main__':
    freeze_support() #在一个冻结的可执行文件中检查这是否是一个伪造的派生进程
    print('start!')
    test()