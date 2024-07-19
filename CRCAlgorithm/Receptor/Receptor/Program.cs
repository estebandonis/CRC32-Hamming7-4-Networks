using System;
class Program
{
    static void Main()
    {
        Console.WriteLine("Hello, World!");
        string message = Console.ReadLine() ?? "Default message";
        Console.WriteLine($"Hola {message}!");
    }
}