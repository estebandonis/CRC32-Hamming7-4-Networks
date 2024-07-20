def XOR(a, b):
    if a == b:
        return '0'
    else:
        return '1'
    
def verifyXOROperation(polinomioBits, oldMessage, newMessage):
    for id, bit in enumerate(oldMessage):
        if id < len(polinomioBits):
            newBit = XOR(bit, polinomioBits[id])
            newMessage.append(newBit)
        else:
            newMessage.extend(oldMessage[id:])
            oldMessage = newMessage.copy()
            newMessage = []
            break
    
    return oldMessage, newMessage

def addChecksum(message, polinomioBits, grado):
    oldMessage = list(message)
    newMessage = []
    endFlag = False
    start = False

    while not endFlag:
        if start == False:
            start = True
        else:
            startIndex = oldMessage.index('1')
            oldMessage = oldMessage[startIndex:]

        if len(oldMessage) == len(polinomioBits):
            endFlag = True

        oldMessage, newMessage = verifyXOROperation(polinomioBits, oldMessage, newMessage)

    return ''.join(newMessage[-grado:])


def main():
    polinomio = '1001'
    gradoPolinomio = 3

    mensaje = input("Ingrese el mensaje: ")

    mensajeExtendido = mensaje + '0' * gradoPolinomio

    messageWithChecksum = mensaje + addChecksum(mensajeExtendido, polinomio, gradoPolinomio)

    print(messageWithChecksum)


if __name__ == "__main__":
    main()