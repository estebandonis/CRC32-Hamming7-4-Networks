﻿using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Receptor
{

    class Aplication
    {
        public static void PrintDecodedMessage(string message)
        {
            Console.WriteLine($"Message decoded: {message}");
        }
    }


    class Presentation()
    {

        public static void DecodeMessage(string message)
        {
            string decodedMessage = "";
            for (int i = 0; i < message.Length; i += 8)
            {
                string byteString = message[i..(i + 8)];
                byte byteValue = Convert.ToByte(byteString, 2);
                decodedMessage += (char)byteValue;
            }

            Aplication.PrintDecodedMessage(decodedMessage);
        }
    }


    class Link
    {
        private string[] _message = [];

        public string[] Message
        {
            get => _message;
            set => _message = value;
        }

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
                    if (startIndex <= -1)
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

        public void Execute()
        {
            string polinomioBits = "100000100110000010001110110110111";

            int gradoPolinomio = 32;

            string verifyMessage = "";

            bool errorFlag = false;

            foreach (string word in _message)
            {
                string verification = VerifyMessage(polinomioBits, word, gradoPolinomio);

                if (verification.Contains('1'))
                {
                    Console.WriteLine("Error: Found errors during verification.");
                    errorFlag = true;
                    break;
                }
                else
                {
                    verifyMessage += word[..^gradoPolinomio];
                }   
            }

            if (errorFlag == false)
            {
                Console.WriteLine("Message received has no errors.");
                Presentation.DecodeMessage(verifyMessage);
            }
        }
    }


    class Transmision
    {
        const string HOST = "127.0.0.1";
        const int PORT = 65432;

        private string[]? _message;

        public void Execute()
        {
            // Create a TCP listener
            TcpListener listener = new(IPAddress.Parse(HOST), PORT);
            Link link = new();

            // Bind the listener to the specified host and port
            listener.Start();
            Console.WriteLine($"Server listening on {HOST}:{PORT}");

            while (true)
            {
                TcpClient client = listener.AcceptTcpClient();

                HandleClient(client);

                link.Message = _message?? [];
                link.Execute();
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
                    string receivedMessage = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    Console.WriteLine($"Message received: " + receivedMessage);
                    _message = receivedMessage.Split(' ');

                    List<string> joinedMessage = [];
                    for (int i = 0; i < _message.Length; i += 2)
                    {
                        if (i + 1 < _message.Length)
                        {
                            joinedMessage.Add(_message[i] + _message[i + 1]);
                        }
                        else
                        {
                            joinedMessage.Add(_message[i]);
                        }
                    }

                    _message = [.. joinedMessage];

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
            Transmision transmision = new();
            transmision.Execute();
        }
    }
}