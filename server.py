#!/usr/bin/python3

import socket
import threading as th
import time
import json
import psycopg2 as pg

HOST = '0.0.0.0'
PORT = 65432

db_conn = pg.connect(dbname='postgres',
                     user='postgres',
                     host='localhost',
                     password='postgres')

db_cursor = db_conn.cursor()

def manage_client(conn, addr):
    db_cursor.execute("select * from spots")
    spots = []
    for spot in db_cursor.fetchall():
        spots.append(spot)
    with conn:
        data = conn.recv(1024)
        if data == b'GIVEDATA':
            conn.sendall(json.dumps(spots).encode())

def main():
    print('waiting')
    with socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            conn, addr = s.accept()
            print('found something')
            thread = th.Thread(target=manage_client,
                               args=(conn, addr),
                               daemon=True)
            thread.start()
            time.sleep(0.1)

if __name__ == '__main__':
    main()
