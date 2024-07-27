using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Receptor
{

    class Aplication
    {
        
    }


    class Presentation
    {
        
    }


    class Link(string message)
    {
        private string _message = message;

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
                    Console.WriteLine(OldMessage);
                    int startIndex = OldMessage.IndexOf('1');
                    if (startIndex <= -1)
                    {
                        break;
                    }
                    string tempOldMessage = OldMessage[startIndex..];;
                    Console.WriteLine(tempOldMessage);
                    Console.WriteLine(tempOldMessage.Length);
                    Console.WriteLine(polinomioBits.Length);
                    
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

        public void Execute()
        {
            string polinomioBits = "100000100110000010001110110110111";

            int gradoPolinomio = 32;

            Console.Write("Ingrese el mensaje: ");

            string verification = VerifyMessage(polinomioBits, _message, gradoPolinomio);

            if (verification.Contains('1'))
            {
                Console.WriteLine("Error: Se descarta el mensaje por contener errores.");
            }
            else
            {
                Console.WriteLine($"El mensaje recibido: {_message[..^gradoPolinomio]} no contiene errores.");
            }
        }
    }


    class Transmision
    {
        const string HOST = "127.0.0.1";
        const int PORT = 65432;

        private string? _message;

        public void Execute()
        {
            // Create a TCP listener
            TcpListener listener = new(IPAddress.Parse(HOST), PORT);

            // Bind the listener to the specified host and port
            listener.Start();
            Console.WriteLine($"Server listening on {HOST}:{PORT}");

            while (true)
            {
                // Accept incoming connections
                TcpClient client = listener.AcceptTcpClient();

                // Handle the connection in a separate method
                HandleClient(client);
            }
        }

        private void HandleClient(TcpClient client)
        {
            NetworkStream stream = client.GetStream();
            try
            {
                byte[] buffer = new byte[1024];
                int bytesRead;

                while ((bytesRead = stream.Read(buffer, 0, buffer.Length)) != 0)
                {
                    // Convert the received bytes to a string
                    _message = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    Console.WriteLine($"Message received: \n{_message}");
                    

                    // Send a response back to the client
                    string response = "Message received correctly";
                    byte[] responseBytes = Encoding.UTF8.GetBytes(response);
                    stream.Write(responseBytes, 0, responseBytes.Length);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }
            finally
            {
                stream.Close();
                client.Close();
            }
        }
    }


    class Program
    {
        static void Main(string[] args)
        {
            // Transmision transmision = new();
            // transmision.Execute();
            Link link = new("1010101011011110101001011000000011011");
            link.Execute();
        }
    }
}