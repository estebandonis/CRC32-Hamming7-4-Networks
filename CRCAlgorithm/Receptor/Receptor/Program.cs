class Program
{

    static char XOR(char a, char b)
    {
        if (a == b)
        {
            return '0';
        }
        else
        {
            return '1';
        }
    }

    static string VerifyXOROperation(string polinomioBits, string OldMessage)
    {
        string NewMessage = "";

        for (int i = 0; i < OldMessage.Length; i++)
        {
            if (i < polinomioBits.Length)
            {
                char newBit = XOR(OldMessage[i], polinomioBits[i]);
                NewMessage += newBit;
            }
            else
            {
                NewMessage += OldMessage[i..];
                OldMessage = NewMessage;
                break;
            }
        }

        if (OldMessage != NewMessage)
        {
            OldMessage = NewMessage;
        }
        
        return OldMessage;
    }

    static string VerifyMessage(string polinomioBits, string OldMessage, int gradoPolinomio)
    {
        bool endFlag = false;
        bool start = false;

        while (!endFlag)
        {
            if (start == false)
            {
                start = true;
            } 
            else
            {
                int startIndex = OldMessage.IndexOf('1');
                if (startIndex == -1)
                {
                    break;
                }
                string tempOldMessage = OldMessage[startIndex..];;
                
                if (tempOldMessage.Length < polinomioBits.Length)
                {
                    tempOldMessage = OldMessage[^polinomioBits.Length..];
                }

                OldMessage = tempOldMessage;
            }

            if (OldMessage.Length == polinomioBits.Length)
            {
                endFlag = true;
            } 

            OldMessage = VerifyXOROperation(polinomioBits, OldMessage);
        }

        return OldMessage[^gradoPolinomio..];
    }

    static void Main()
    {
        string polinomioBits = "100000100110000010001110110110111";

        int gradoPolinomio = 32;

        Console.Write("Ingrese el mensaje: ");

        string message = Console.ReadLine() ?? "11010001";

        string verification = VerifyMessage(polinomioBits, message, gradoPolinomio);

        if (verification.Contains('1'))
        {
            Console.WriteLine("Error: Se descarta el mensaje por contener errores.");
        }
        else
        {
            Console.WriteLine($"El mensaje recibido: {message[..^gradoPolinomio]} no contiene errores.");
        }
    }
}