import threading
import time
import random
import socket
from sys import argv


def dns_server(rec_file, nx_server, port):
    dic = read_dns_rec(rec_file)
    rs_socket = establish_socket('', port, True)
    
    while(True):
        rs_socket.listen(1)
        csockid, addr = rs_socket.accept()
        
        req_dns=csockid.recv(200).decode('utf-8')
        if(req_dns == 'quit'):break
        search_result = search_dns_rec(req_dns, dic)
        msg = msg_format(req_dns, search_result, nx_server)
        csockid.send(msg.encode('utf-8'))
        
    rs_socket.close()
    exit()
        

def client(rec_file, dns_addr, rs_p, ts_p):
    addrs = read_input(rec_file)
   
    for addr in addrs:
        # try with rs
        cs = establish_socket(dns_addr, rs_p, False)
        cs.send(addr.encode('utf-8'))                
        recv_data=cs.recv(200).decode('utf-8').split(' ')
        cs.close()
        #try with ts
        if(recv_data[1] == 'NS'):
            cs = establish_socket(recv_data[0], ts_p, False)
            cs.send(addr.encode('utf-8'))                
            recv_data=cs.recv(200).decode('utf-8').split(' ')
            cs.close()
        #generate result
        if(recv_data[1] == 'NS'):
            rst_str = '{} - Error:HOST NOT FOUND\n'.format(addr)
        else:
            rst_str = '{} {} {}\n'.format(addr, recv_data[1], recv_data[2])
        file_append('./RESOLVED.txt', rst_str)
    
    cs = establish_socket(dns_addr, rs_p, False)
    cs.send('quit'.encode('utf-8'))
    cs.close()
    
    cs = establish_socket(dns_addr, ts_p, False)
    cs.send('quit'.encode('utf-8'))
    cs.close()
    
    exit()


def file_append(file_addr, text):
    with open(file_addr, 'a+') as f:
        f.write(text)
    return


def msg_format(dns_dic, search_result, nx_server):
    if(search_result != 'NS'):
        msg = '{} {} A'.format(dns_dic, search_result)
    else:
        msg = '{} NS'.format(nx_server)
    return msg



def establish_socket(addr, port, is_server):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    server_binding = (addr, port)
    
    if(is_server):
        sock.bind(server_binding)
    else:
        sock.connect(server_binding)
    return sock

     

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

def read_input(addr):
    result = []
    with open(addr, encoding = 'utf-8') as fp:
        line_list = fp.readlines()
        for line in line_list:
            line = str(line.rstrip().lower())
            result.append(line)
    return result

def search_dns_rec(domain, dic):
    return dic.get(domain, 'NS')


def main():
    #dns_server('PROJI-DNSRS.txt', socket.gethostbyname(socket.gethostname()), int(argv[1]))
    dns_server('PROJI-DNSTS.txt', socket.gethostbyname(socket.gethostname()), int(argv[1]))
    #client('PROJI-HNS.txt', socket.gethostbyname(argv[1]), int(argv[2]), int(argv[3]))

if __name__ == "__main__":
    main()
    
    '''
    th_rs = threading.Thread(name='rs', target=dns_server, args=('./rs', socket.gethostbyname(socket.gethostname()), 50007))
    th_ts = threading.Thread(name='ts', target=dns_server, args=('./ts', '', 50008))
    th_cl = threading.Thread(name='cl', target=client, args=('./cl',socket.gethostbyname(socket.gethostname())))

    th_ts.start()
    th_rs.start()
    time.sleep(random.random() * 5)
    th_cl.start()
    
    print("Done.")
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
