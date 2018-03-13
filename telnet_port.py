#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = '40kuai'
import socket, select, time


class check_port():
    def __init__(self, file_path):
        self.file_path = file_path
        self.sk_list = None
        self.connect()

    def connect(self):
        self.sk_list = list()
        with open('telnet_port', encoding='utf-8') as ip_port_file:
            ip_port_string = ip_port_file.read()
        for url in ip_port_string.split('\n'):
            ip, port = url.strip().split()
            sk = socket.socket()
            sk.setblocking(False)
            try:
                sk.connect((ip, int(port)))
            except BlockingIOError as e:
                pass
            self.sk_list.append(sk)

    def check(self, timeout=3):
        start_time = time.time()
        while True:
            if not self.sk_list:
                break
            rList, wList, eList = select.select([], self.sk_list, [], 0.5)
            for i in wList:
                # print('正常')
                i.close()
                self.sk_list.remove(i)
            if time.time() - start_time > timeout:
                break
        err_list = [i.getpeername() for i in self.sk_list]
        for i in self.sk_list: i.close()
        self.sk_list = None
        return err_list


class select_port():
    def __init__(self, ip, iteration):
        self.ip = ip
        self.sk_list = None
        self.connect(iteration)

    def connect(self,iteration):
        self.sk_list = list()
        for port in iteration:
            sk = socket.socket()
            sk.setblocking(False)
            try:
                sk.connect((self.ip, int(port)))
            except BlockingIOError as e:
                pass
            self.sk_list.append(sk)

    def check(self, timeout=0.5):
        start_time = time.time()
        success_list = list()
        while True:
            if not self.sk_list:
                break
            rList, wList, eList = select.select([], self.sk_list, [], 0.5)
            for i in wList:
                success_list.append(i.getpeername())
                i.close()
                self.sk_list.remove(i)
            if time.time() - start_time > timeout:
                break
        return success_list


if __name__ == '__main__':
    # obj = check_telnet('tilnet_port')
    # print(obj.check())
    iteration = (i for i in range(0,1000,2))
    obj = select_port('192.168.10.173',iteration)
    print(obj.check())
