import argparse, socket, zmq, time, random

def checkBingo(clientList, currentList):
    check = [False] * 25
    for i in range(25):
        for j in range(25):
            if currentList[i] == clientList[j]:
                check[j] = True
    line = 0

    for i in range(5):
        true = True
        for j in range(5):
            if check[j*5+i] == False:
                true = False
            if true == False:
                break
        if true == True:
            line+=1

    for j in range(5):
        true = True
        for i in range(5):
            if check[j*5+i] == False:
                true = False
            if true == False:
                break
        if true == True:
            line+=1

    true = True
    for i in range(5):
        if check[i*5+i] == False:
            true = False
        if true == False:
            break
    if true == True:
        line+=1

    true = True
    for i in range(5):
        if check[(4-i)*5+i] == False:
            true = False
        if true == False:
            break
    if true == True:
        line+=1
    #print("You already have {} lines.".format(line))
    if line >= 5:
        return True
    else:
        return False
def check_port_available(interface, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((interface, port))
    except socket.error as e:
        if e.errno == 98:     #already in use
            return False
    finally:
        s.close()
    return True

def server(interface, port):

    if not check_port_available(interface, port):
        print(f"Port {port} is already in use. Please choose another port.")
        return
    if not check_port_available(interface, port + 1):
        print(f"Port {port + 1} is already in use. Please choose another port.")
        return

    # REP
    url = "tcp://{}:{}".format(interface, port)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(url)
    # PUB
    pub_socket = context.socket(zmq.PUB)
    pub_url = f"tcp://{interface}:{port+1}"
    pub_socket.bind(pub_url)
    
    numbers=0
    maps = {}
    names = {}
    thisMap =[]
    delay = 20
    start = time.time()
    
    print("Server start ...")
    while True:
        socket.setsockopt(zmq.RCVTIMEO, int(delay * 1000))
        try:
            data = socket.recv_string()
            numbers+=1
            splitText = data.split(',')
            thisMap = list(map(int,splitText[1:]))
            maps[splitText[0]] = thisMap  #this
            names[splitText[0]] = splitText[0]
            #print(maps)
        
            message = "{},{:.2f}".format(numbers, delay - time.time() + start)
            socket.send_string(message)
            print(' "{}" chooses: {}'.format(names[splitText[0]], maps[splitText[0]]))   #{!r}
        
        except zmq.error.Again as e:
            print("Game Start")
            pub_socket.send_string("Start !")
            break

    List = list(range(1,26))
    random.shuffle(List)
    i=0
    end = False
    while i<25:
        if end:
            break
        pub_socket.send_string(str(List[i]))
        print('Number is {}'.format(List[i]))
        i+=1
        socket.setsockopt(zmq.RCVTIMEO, int(2 * 1000))
        bingoStr = ''
        try:
            while True:
                data = socket.recv_string()
                bingoStr = data.split(',')
                if bingoStr[0]=='Bingo':
                    tempList = [0]*25
                    for a in range(i):
                        tempList[a] = List[a]
                    if checkBingo(maps[bingoStr[1]],tempList):
                        socket.send_string("You are correct !")
                        end = True
                        break
                    else:
                        socket.send_string('You are wrong!')
        except zmq.error.Again as e:
            continue
        except zmq.error.ZMQError:
            socket.send_string("The game has started.\n You are late.")

    if bingoStr and bingoStr[1] in names:
        mes = 'Bingo, from {}'.format(names[bingoStr[1]])
        pub_socket.send_string(mes)
        print(mes)
    else:
        print("no player !")

    pub_socket.close()
    socket.close()
    
def client(network, port):
    # REQ
    context = zmq.Context()
    sock = context.socket(zmq.REQ)
    sock.connect(f"tcp://{network}:{port}")
    # SUB
    sub_sock = context.socket(zmq.SUB)
    sub_url = f"tcp://{network}:{port+1}"
    sub_sock.connect(sub_url)
    sub_sock.setsockopt_string(zmq.SUBSCRIBE,'')

    while True:
        text = input("Please enter your name, and 25 different numbers from 1 to 25 in random order, seperated by ','\n")
        textList = text.split(',')
        if len(textList) != 26:
            print ("Invalid input.\n You must enter your name followed by 25 numbers.")
            continue
        try:
            num = list(map(int, textList[1:]))
        except ValueError:
            print("Invalid input.\n numbers must be integers.")
            continue
        if len(num) != 25 or not all(1 <= n <= 25 for n in num):
            print("Invalid input.\n numbers must be unique between 1 to 25.")
            continue
        break

    sock.send_string(text)
    
    chessboard = list(map(int,textList[1:]))
    print("\nThis is your chessboard:")
    for i in range(25):
        print('%2d' %chessboard[i], end=' ')
        if i%5==4:
            print('')
    data = sock.recv_string()
    
    w_data = ''
    if data.find("late") != -1:
        w_data = data
        print(w_data)
    else:
        mesList = data.split(',')
        print("You are the {} players.\nThe game will start in {} seconds.".format(mesList[0],mesList[1]))
        

        data = sub_sock.recv_string()
        print(data)     #game start
    currentList =[0] * 25
    i = 0
    while i < 25:
        data = sub_sock.recv_string()    # reccive random num
        text = data
        if w_data != '':
           break

        if text.startswith('Bingo'): 
            for i in range(25):
                if chessboard[i] in currentList:
                    print('\033[35m%2d\033[0m' %chessboard[i], end=' ')
                else:
                    print('%2d' %chessboard[i], end=' ')
                if i%5==4:
                    print('')
            if not checkBingo(chessboard, currentList):
                print("You are failed in bingo !")
            print(text)
            break
        number = int(text)
        currentList[i] = number
        i+=1
        print("Number is {}".format(str(number)))
        if checkBingo(chessboard, currentList):
            sock.setsockopt(zmq.RCVTIMEO, int(2 * 1000))
            try:
                sock.send_string(f"Bingo,{textList[0]}")
                data = sock.recv_string()
                print(data)
                print(f"use {i} numbers")
                print("You are bingo !")
            except zmq.error.Again:
                print("you are late !")
    sub_sock.close()
    sock.close()

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send, receive UDP broadcast')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                               ' network the client sends to')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)

