import random
import socket

class Transmision:
    """
    Class in charge of sending the message to the server
    """
    def __init__(self, message):
        """
        Constructor of the class

        :param message: Message to be sent
        """
        self.message = ' '.join(message)
        self.serverIp = "127.0.0.1"
        self.serverPort = 65432 

        self.sendMessage()
        print("Mensaje enviado: ", self.message)

    def sendMessage(self):
        """
        Function in charge of sending the message to the receiver
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            client_socket.connect((self.serverIp, self.serverPort))
            
            client_socket.sendall(self.message.encode('utf-8'))
            
            response = client_socket.recv(1024)
            print('Received from server:', response.decode('utf-8'))
        
        finally:
            client_socket.close()


class Noise:
    """
    Class in charge of adding noise to the message
    """
    def __init__(self, message):
        """
        Constructor of the class

        :param message: Message to be sent
        """
        self.message = message

        self.main()

    def main(self):
        """
        Executes the main functions of the class
        """
        self.AddNoise()
        Transmision(self.message)

    def AddNoise(self):
        """
        Function in charge of adding noise to the message
        """
        print("Enter the probability of noise (0-1): ")
        firstNum = int(input("Enter dividend: "))
        secondNum = int(input("Enter divisor: "))
        probability = firstNum/secondNum

        messageList = self.message

        error = False
        contador = 0

        # AI used to fix error when trying to replace a value in a string
        for indexBlock, block in enumerate(messageList):
            for indexBit, bit in enumerate(block):
                if self.getNoiseChance(probability):
                    contador += 1
                    if error == False:
                        error = True
                        print("Error introduced")

                    listBlock = list(self.message[indexBlock])
                    listBlock[indexBit] = '1' if bit == '0' else '0' 
                    self.message[indexBlock] = ''.join(listBlock)
        
        print("Error amount: ", contador)

    @staticmethod
    def getNoiseChance(probability):
        """
        Function in charge of determining if noise should be added to the message
        """
        return random.random() <= probability


class Link:
    """
    Class in charge of adding the checksum to the message
    """
    def __init__(self, message):
        """
        Constructor of the class

        :param message: Message to be sent
        """
        self.message = message
        self.main()
    
    def main(self):
        """
        Executes the main functions of the class
        """
        self.message = self.message

        self.polinomBits = '100000100110000010001110110110111'

        self.polinomGrade = 32

        newMessage = []

        for block in self.message:
            self.extendedMessage = block + '0' * self.polinomGrade

            checksum = self.addChecksum()

            newMessage.append(block)
            newMessage.append(checksum)

        Noise(newMessage)

    @staticmethod
    def XOR(a, b):
        """
        Function in charge of performing the XOR operation between two bits

        :param a: First bit
        :param b: Second bit
        :return: Result of the XOR operation
        """
        if a == b:
            return '0'
        else:
            return '1'

    def verifyXOROperation(self):
        """
        Function in charge of verifying the XOR operation between the message and the polynomial
        """
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
        """
        Function in charge of adding the checksum to the message

        :return: Checksum
        """
        self.oldMessage = list(self.extendedMessage)
        endFlag = False
        start = False

        while not endFlag:
            if start == False:
                start = True
            else:
                startIndex = self.oldMessage.index('1')
                tempOldmessage = self.oldMessage[startIndex:]
                if len(tempOldmessage) < len(self.polinomBits):
                    tempOldmessage = self.oldMessage[-len(self.polinomBits):]
                    
                self.oldMessage = tempOldmessage.copy()

            if len(self.oldMessage) == len(self.polinomBits):
                endFlag = True

            self.verifyXOROperation()

        return ''.join(self.oldMessage[-self.polinomGrade:])


class Presentation:
    """
    Class in charge of managing the enconding of the message and the separation of the message into blocks
    """
    def __init__(self, message):
        """
        Constructor of the class

        :param message: Message to be sent
        """
        self.message = message
        self.encodeMessage()
        Link(self.message)

    def encodeMessage(self):
        """
        Function in charge of encoding the message to binary
        """
        # AI helped with encoding the message
        byte_array = self.message.encode('utf-8')

        self.message = ''.join(format(byte, '08b') for byte in byte_array)

        self.checkMessageSize()

    def checkMessageSize(self):
        """
        Function in charge of checking if the message is a multiple of 32, if not, it adds zeros to the message
        """
        if len(self.message) % 32 != 0:
            self.message = '0' * (32 - len(self.message) % 32) + self.message
        
        if len(self.message) > 32:
            self.message = self.split_into_blocks()
        else: 
            self.message = [self.message]

    def split_into_blocks(self, block_size=32):
        """
        Function in charge of splitting the message into blocks of 32 bits

        :param block_size: Size of the blocks
        :return: List of blocks
        """
        return [self.message[i:i + block_size] for i in range(0, len(self.message), block_size)]  


class Application:
    """
    Class in charge of managing the application and requesting the message to be sent
    """
    def __init__(self):
        self.main()

    def main(self):
        """
        Main function of the application, in charge of requesting the message to be sent and sending it to the next layer
        """
        while True:
            print("Si quiere salir, escriba 'exit'")
            message = input("Ingrese el mensaje: ")
            if message == 'exit':
                break
            elif message == '':
                print("No se ingresó ningún mensaje")
            else:
                print("Mensaje: ", message)
                Presentation(message)


if __name__ == "__main__":
    Application()