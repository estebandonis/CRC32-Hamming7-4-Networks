# Lab #2 - Networks

A series of programs written in Python, C# and C++ that simulate the funcionality of two algorithms, CRC-32 and Hamming. 
They give an insight in what goes behind the art of checking for errors and misplaced bits when sending messages through a network.

## Requirements

In order to run the following programs we need to have the following programming languages install: C#, Python and C++. 

### Python

Make sure you have Python 3 or above to run the following programs, then run:
```shell
python 3 nameOfMainFile.py
```

### C++

Make sure you have C++ 21 and above to run emisor program in Hamming folder, then compile the program using command:
```shell
gcc Emisor.c -o Emisor -lws2_32
```

and run it using command:
```shell
./Emisor
```

### C#

Make sure you have C# and its framework .NET version 8 to run receptor program in CRC - 32 folder, 
then compile using the following command:

IT IS ADVISE TO USE VISUAL STUDIO CODE AND RUN IT USING THE C# EXTENSION, SINCE THE FOLLOWING METHOD WASN'T TESTED.

```shell
dotnet build
```

Then run it using command:
```shell
dotnet run
```
