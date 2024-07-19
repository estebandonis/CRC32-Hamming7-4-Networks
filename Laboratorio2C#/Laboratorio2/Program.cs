using System;

class Program
{



    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
        string name = Console.ReadLine() ?? "Unknown";
        Console.WriteLine($"Hello, {name}!");
    }
}