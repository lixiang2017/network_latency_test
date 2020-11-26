import socket
import time
import select
import pickle
from argparse import ArgumentParser
import json
import sys

def recv_resp(sock, t1):
    sock.setblocking(0)
    RETURN_TIMEOUT = 5
    ready = select.select([sock], [], [], RETURN_TIMEOUT)
    print('ready: ', ready)
    if ready[0]:
        resp, addr = sock.recvfrom(1024)
        t4 = time.time()
        time_data = json.loads(resp)
        print('time_data: ', time_data)
        t2 = time_data.get('t2')
        t3 = time_data.get('t3')
        return (t1, t2, t3, t4)
    else:
        print("connetion failed")
        return "failed"


def send_req(sock, ip, port, req):
    t1 = time.time()
    print('sending request...')
    print('sending to ', ip, port)
    sock.sendto(pickle.dumps(req), (ip, port))
    print('request sent.')
    return t1

def main():
    args = getArguments()

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP

    for f in range(3):
        MESSAGE = "request_time"
        t1 = send_req(sock, args.ip, int(args.port), MESSAGE)

        times = recv_resp(sock, t1)

        if times == "failed":
                print("timed out, reattempting connection")
        else:
            print("Client send time:    " + str(times[0]))
            print("Server receive time: " + str(times[1]))
            print("Server send time:    " + str(times[2]))
            print("Client receive time: " + str(times[3]))
            print("Client delta:        " + str(times[3] - times[0]))
            print("Server delta:        " + str(times[2] - times[1]))
            rtt = (times[3] - times[0]) - (times[2] - times[1])
            print("RTT:                 " + str(rtt))
            print("Offset:              " + str((times[0] + rtt/2) - times[1]))
            return



def getArguments():
    parser = ArgumentParser('server')
    parser.add_argument('--ip', '-ip', dest='ip', help='server ip', default='127.0.0.1')
    parser.add_argument('--port', '-port', dest='port', help='server port', default=8090)
    return parser.parse_args()


if __name__ == "__main__":
    main()











