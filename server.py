import socket
import pickle
import random
import threading

class SnakeServer:
    def __init__(self):
        self.running = False
        self.s = None

    def GameSession(self, Connections):
        food_pos = []
        data_snake_1 = []
        data_snake_2 = []
        no_food = True
        while self.running:
            data_snake_1 = Connections[0].recv(1024)
            data_snake_2 = Connections[1].recv(1024)
            if not data_snake_1 or not data_snake_2:
                break

            data_snake_1 = pickle.loads(data_snake_1)
            data_snake_2 = pickle.loads(data_snake_2)

            if not food_pos:
                no_food = True
            else:
                no_food = False

            while not food_pos:
                x = random.randint(2, 28) * 20
                y = random.randint(2, 28) * 20
                if not [x, y] in data_snake_1 and not [x, y] in data_snake_2:
                    food_pos = [x, y]
                    data_snake_1.append(food_pos)
                    data_snake_2.append(food_pos)

            if data_snake_1[-2] == food_pos or data_snake_2[-2] == food_pos:
                food_pos = []
                data_snake_1.append([-20, -20])
                data_snake_2.append([-20, -20])

            if food_pos and not no_food:
                data_snake_1.append(food_pos)
                data_snake_2.append(food_pos)

            data_snake_1 = pickle.dumps(data_snake_1)
            data_snake_2 = pickle.dumps(data_snake_2)

            Connections[0].sendall(data_snake_2)
            Connections[1].sendall(data_snake_1)

    def Start(self):
        self.running = True
        HOST = '127.0.0.1'
        PORT = 65432

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.s.bind((HOST, PORT))
        self.s.listen(5)
        conn_list = []
        threads = []
        print("Server is Running")
        while self.running:
            for i in range(2):
                try:
                    if i:
                        print("Waiting for 2nd Player to connect")
                    conn, addr = self.s.accept()
                    print('Connected by', addr[0])
                    conn_list.append(conn)
                except Exception as e:
                    print("Error accepting connection:", str(e))
                    self.running = False

            if len(conn_list) == 2:
                threads.append(threading.Thread(
                    target=self.GameSession, args=(conn_list,)))
                threads[-1].start()
                conn_list = []

    def Stop(self):
        if self.s:
            self.s.close()
        self.running = False


if __name__ == "__main__":
    server = SnakeServer()
    try:
        server.Start()
    except KeyboardInterrupt:
        print("\nServer Stopped by User")
    finally:
        server.Stop()
        print("Server Stopped")
