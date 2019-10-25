from multiprocessing import Process, Pipe
from datetime import datetime


def timing(counter):
    return f'(time vector: {counter}, local time: {datetime.now()})'


def send(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('test', counter))
    print('Message sent from ' + str(pid) + timing(counter))
    return counter


def event_on_current(pid, counter):
    counter[pid] += 1
    print(f'Internal event on process {pid} | {timing(counter)}')
    return counter


def receive(pipe, pid, counter):
    msg, timestamp = pipe.recv()
    counter = ptimestamp(pid, timestamp, counter)
    print(f'Process {str(pid)} has receive a new msg! {timing(counter)}')
    return counter


def ptimestamp(pid, received, counter):
    out = []
    for i in range(len(received)):
        out.append(max(received[i], counter[i]))
    out[pid] += 1
    return out

def process_a(pipe12):
    pid = 0
    counter = [0, 0, 0]
    counter = send(pipe12, pid, counter)  # a0
    counter = send(pipe12, pid, counter)  # a1
    counter = event_on_current(pid, counter)  # a2
    counter = receive(pipe12, pid, counter)  # a3
    counter = event_on_current(pid, counter)  # a4
    counter = event_on_current(pid, counter)  # a5
    counter = receive(pipe12, pid, counter)  # a6

    print(f'Process A({pid}): {counter}')


def process_b(pipe21, pipe23):
    pid = 1
    counter = [0, 0, 0]

    counter = receive(pipe21, pid, counter)  # b0
    counter = receive(pipe21, pid, counter)  # b1
    counter = send(pipe21, pid, counter)  # b2
    counter = receive(pipe23, pid, counter)  # b3
    counter = event_on_current(pid, counter)  # b4
    counter = send(pipe21, pid, counter)  # b5
    counter = send(pipe23, pid, counter)  # b6
    counter = send(pipe23, pid, counter)  # b7

    print(f'Process B({pid}): {counter}')


def process_c(pipe32):
    pid = 2
    counter = [0, 0, 0]

    counter = send(pipe32, pid, counter)
    counter = receive(pipe32, pid, counter)
    counter = event_on_current(pid, counter)
    counter = receive(pipe32, pid, counter)

    print(f'Process C({pid}): {counter}')


if __name__ == '__main__':
    a_to_b, b_to_a = Pipe()
    b_to_c, c_to_b = Pipe()

    processA = Process(target=process_a,
                       args=(a_to_b, ))
    processB = Process(target=process_b,
                       args=(b_to_a, b_to_c))
    processC = Process(target=process_c,
                       args=(c_to_b,))

    processA.start()
    processB.start()
    processC.start()

    processA.join()
    processB.join()
    processC.join()

