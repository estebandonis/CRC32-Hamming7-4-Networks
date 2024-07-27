import random
import socket


class Transmision:
    def __init__(self, message):
        self.message = message
        self.serverIp = "127.0.0.1"
        self.serverPort = 65432 

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

        # if self.getNoiseChance():
        #     self.message = self.addNoise()
        
        Transmision(self.message)

    def addNoise(self):
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
        self.main()
    
    def main(self):
        self.message = self.message

        self.polinomBits = '100000100110000010001110110110111'

        self.polinomGrade = 32

        self.extendedMessage = self.message + '0' * self.polinomGrade

        self.addChecksum()

        Noise(self.message)

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
        self.oldMessage = list(self.extendedMessage)
        endFlag = False
        start = False

        while not endFlag:
            if start == False:
                start = True
            else: # Agregar los 0s extras y separar el mensaje en bloques de 32 bits
                startIndex = self.oldMessage.index('1')
                tempOldmessage = self.oldMessage[startIndex:]
                if len(tempOldmessage) < len(self.polinomBits):
                    tempOldmessage = self.oldMessage[-len(self.polinomBits):]
                    
                self.oldMessage = tempOldmessage.copy()

            if len(self.oldMessage) == len(self.polinomBits):
                endFlag = True

            self.verifyXOROperation()

        self.message = self.message + ''.join(self.oldMessage[-self.polinomGrade:])

        if len(self.message) % 32 != 0:
            self.message = '0' * (32 - len(self.message) % 32) + self.message


class Presentation:
    def __init__(self, message):
        self.message = message
        self.encodeMessage()
        Link(self.message)

    def encodeMessage(self):
        byte_array = self.message.encode('utf-8')
        print("Mensaje en bytes: ", byte_array)

        self.message = ''.join(format(byte, '08b') for byte in byte_array)
        print("Mensaje en bits: ", self.message)


class Application:
    def __init__(self):
        self.main()

    def main(self):
        while True:
            print("Si quiere salir, escriba 'exit'")
            message = input("Ingrese el mensaje: ")
            if message == 'exit':
                break
            else:
                print("Mensaje: ", message)
                Presentation(message)


if __name__ == "__main__":
    Application()