import threading
import time
import random

import socket

def root_server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    data_from_server=csockid.recv(100).decode('utf-8')
    search_result = search_dns_rec(data_from_server, dic)
    if(search_result != 'NS'):
        msg = '{} {} A'.format(data_from_server, search_result)
    else:
        msg = '{} NS'.format(data_from_server)

    csockid.send(msg.encode('utf-8'))
    # Close the server socket
    ss.close()
    exit()



def client():
    #   create socket
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Define the port on which you want to connect to the server (current machine)
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)# need to be changed to server address when run in different machine
    cs.connect(server_binding)

    msg = "www.ibm.com"
    cs.send(msg.encode('utf-8'))
    # Receive data from the server
    data_from_server=cs.recv(100).decode('utf-8').split(' ')

    addr = data_from_server[0]
    ip = data_from_server[1]
    method = data_from_server[2]

    print('What I got is: {}, {}, {}\n', format(addr, ip, method))
    # close the client socket
    cs.close()
    exit()


"""read in existing dns record, and parse into a dictionary
    Args:
        param1 (str): Address of dns record file.
    Returns:
        Dict: {domain, ip}
    """

def read_dns_rec(addr):
    result = {}
    with open(addr, encoding = 'utf-8') as fp:
        line_list = fp.readlines()
        for line in line_list:
            line = line.rstrip() # get rid of trailing space
            elems = line.split(' ')
            if(str(elems[2]) == 'A'):
                result[elems[0]] = elems[1]
    return result

def search_dns_rec(domain, dict):
    try:
        return dic.get(domain)
    except KeyError:
        return 'NS'



if __name__ == "__main__":
    th_rs = threading.Thread(name='rs', target=root_server)
    th_rs.start()

    #time.sleep(random.random() * 5)
    #th_ts = threading.Thread(name='ts', target=top_server)
    #th_ts.start()

    time.sleep(random.random() * 5)
    th_cl = threading.Thread(name='cl', target=client)
    th_cl.start()

    time.sleep(5)
    print("Done.")
