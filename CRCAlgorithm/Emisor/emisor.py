import random
import socket


class Transmision:
    def __init__(self, message, serverIp, serverPort):
        self.message = message
        self.serverIp = serverIp
        self.serverPort = serverPort

        self.sendMessage()
        print("Mensaje enviado: ", self.message)

    def sendMessage(self):
        # Step 1: Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Step 2: Connect the socket to the server
            client_socket.connect((self.serverIp, self.serverPort))
            
            # Step 3: Send the message
            client_socket.sendall(self.message.encode('utf-8'))
            
            # Step 4: Optionally, receive a response
            response = client_socket.recv(1024)
            print('Received from server:', response.decode('utf-8'))
        
        finally:
            # Step 5: Close the socket
            client_socket.close()


class Noise:
    
    def __init__(self, message):
        self.message = message

        if self.getNoiseChance():
            self.message = self.addNoise(self.message)
        
        Transmision(self.message)

    def addNoise(self, message):
        messageList = list(self.message)
        randomIndex = random.randint(0, len(messageList) - 1)
        messageList[randomIndex] = '1' if messageList[randomIndex] == '0' else '0'

        return ''.join(messageList)

    @staticmethod
    def getNoiseChance():
        return random.random() <= 0.1


class Link:

    def __init__(self, message):
        self.message = message

        self.polinomBits = '100000100110000010001110110110111'

        polinomGrade = 32

        for bit in message:
            if bit != '1' and bit != '0':
                print('El mensaje debe ser binario (1s y 0s solamente)')
                return

        self.extendedMessage = message + '0' * polinomGrade

        messageWithChecksum = message + self.addChecksum()

        print("Mensaje con checksum: ", messageWithChecksum)
    

    @staticmethod
    def XOR(a, b):
        if a == b:
            return '0'
        else:
            return '1'


    def verifyXOROperation(self):
        newMessage = []

        for id, bit in enumerate(self.oldMessage):
            if id < len(self.polinomBits):
                newBit = self.XOR(bit, self.polinomBits[id])
                newMessage.append(newBit)
            else:
                newMessage.extend(self.oldMessage[id:])
                self.oldMessage = newMessage.copy()
                break
        
        if (self.oldMessage != newMessage):
            self.oldMessage = newMessage.copy()


    def addChecksum(self):
        oldMessage = list(self.extendedMessage)
        endFlag = False
        start = False

        while not endFlag:
            if start == False:
                start = True
            else: # Agregar los 0s extras y separar el mensaje en bloques de 32 bits
                startIndex = oldMessage.index('1')
                tempOldmessage = oldMessage[startIndex:]
                if len(tempOldmessage) < len(self.polinomBits):
                    tempOldmessage = oldMessage[-len(self.polinomBits):]
                    
                oldMessage = tempOldmessage.copy()

            if len(oldMessage) == len(self.polinomBits):
                endFlag = True

            self.verifyXOROperation()

        return ''.join(oldMessage[-self.grado:])


class Presentation:

    def __init__(self):
        pass


class Application:
    def __init__(self):
        while True:
            print("Si quiere salir, escriba 'exit'")
            message = input("Ingrese el mensaje: ")
            if message == 'exit':
                break
            else:
                print("Mensaje: ", message)
                Presentation().receiveMessage(message)

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 65432 
    # Application()
    Transmision("Hola, mundo!", HOST, PORT)