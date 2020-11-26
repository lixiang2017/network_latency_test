import socket
import time
import pickle
from argparse import ArgumentParser
import json


def listen(ip="0.0.0.0", port=8090):
    print('type of port: ', type(port))
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((ip, port))
    print('server is listening on port: ', ip, port)

    while True:
        req_data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        t2 = time.time()
        print("t2: ", t2)
        req = pickle.loads(req_data)
        ret_addr = addr[0]
        ret_port = addr[1]

        print ("received request: ", req, " from ", ret_addr, " on port", ret_port)

        if(req == "request_time"):
            data_sent = json.dumps({"t2": t2, "t3": time.time()})
            print("data sending...")
            print("data: ", data_sent)
            print('ret: ', (ret_addr, ret_port))

            sendto_ret = sock.sendto(data_sent.encode(), (ret_addr, ret_port))
            print 'sendto_ret: ', sendto_ret
            print("data sent.")



def getArguments():
    parser = ArgumentParser('server')
    parser.add_argument('--ip', '-ip', dest='ip', help='server ip', default='0.0.0.0')
    parser.add_argument('--port', '-port', dest='port', help='server port', default=8090)
    return parser.parse_args()


def main():
    args = getArguments()

    listen(args.ip, int(args.port))

if __name__ == "__main__":
    main()



