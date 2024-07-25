def XOR(a, b):
    if a == b:
        return '0'
    else:
        return '1'
    
def verifyXOROperation(polinomioBits, oldMessage):
    newMessage = []

    for id, bit in enumerate(oldMessage):
        if id < len(polinomioBits):
            newBit = XOR(bit, polinomioBits[id])
            newMessage.append(newBit)
        else:
            newMessage.extend(oldMessage[id:])
            oldMessage = newMessage.copy()
            break
    
    if (oldMessage != newMessage):
        oldMessage = newMessage.copy()
    
    return oldMessage

def addChecksum(message, polinomioBits, grado):
    oldMessage = list(message)
    endFlag = False
    start = False

    while not endFlag:
        if start == False:
            start = True
        else:
            startIndex = oldMessage.index('1')
            tempOldmessage = oldMessage[startIndex:]
            if len(tempOldmessage) < len(polinomioBits):
                tempOldmessage = oldMessage[-len(polinomioBits):]
                
            oldMessage = tempOldmessage.copy()

        if len(oldMessage) == len(polinomioBits):
            endFlag = True

        oldMessage = verifyXOROperation(polinomioBits, oldMessage)

    return ''.join(oldMessage[-grado:])


def main():
    polinomioBits = '100000100110000010001110110110111'

    gradoPolinomio = 32

    mensaje = input("Ingrese el mensaje: ")

    for bit in mensaje:
        if bit != '1' and bit != '0':
            print('El mensaje debe ser binario (1s y 0s solamente)')
            return

    mensajeExtendido = mensaje + '0' * gradoPolinomio

    messageWithChecksum = mensaje + addChecksum(mensajeExtendido, polinomioBits, gradoPolinomio)

    print("Mensaje Extendido: ", messageWithChecksum)


if __name__ == "__main__":
    main()