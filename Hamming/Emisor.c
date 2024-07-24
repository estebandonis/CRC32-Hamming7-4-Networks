#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Función para convertir una cadena de bits a un array de enteros
void bitsToArray(const char* bits, int* array, int len) {
    for (int i = 0; i < len; i++) {
        array[i] = bits[i] - '0';
    }
}

// Función para convertir un array de enteros a una cadena de bits
void arrayToBits(int* array, char* bits, int len) {
    for (int i = 0; i < len; i++) {
        bits[i] = array[i] + '0';
    }
    bits[len] = '\0';
}

// Función para calcular los bits de paridad y formar el código Hamming de 7 bits
void hamming74Encoder(int* data_bits, int* hamming_code) {
    int d1 = data_bits[0];
    int d2 = data_bits[1];
    int d3 = data_bits[2];
    int d4 = data_bits[3];

    // Calcular bits de paridad
    int p1 = d1 ^ d2 ^ d3;
    int p2 = d1 ^ d2 ^ d4;
    int p3 = d1 ^ d3 ^ d4;

    // Construir el código Hamming de 7 bits
    hamming_code[0] = d1;
    hamming_code[1] = d2;
    hamming_code[2] = d3;
    hamming_code[3] = p1;
    hamming_code[4] = d4;
    hamming_code[5] = p2;
    hamming_code[6] = p3;
}

void processBits(char* input_bits) {
    int len = strlen(input_bits);
    int data[len];
    bitsToArray(input_bits, data, len);

    int num_blocks = (len + 3) / 4;
    char output_bits[20 * num_blocks];
    output_bits[0] = '\0';

    for (int i = 0; i < num_blocks; i++) {
        int start = len - 4 * (i + 1);
        int end = len - 4 * i;
        int segment[4] = {0, 0, 0, 0};

        for (int j = 0; j < (end - start); j++) {
            if (start + j >= 0) {
                segment[4 - (end - start) + j] = data[start + j];
            }
        }

        int hamming[7];
        hamming74Encoder(segment, hamming);
        
        // Imprimir los bits de paridad calculados
        printf("Bits de paridad: %d %d %d\n", hamming[3], hamming[5], hamming[6]);

        char block_output[8];
        arrayToBits(hamming, block_output, 7);
        strcat(output_bits, block_output);
    }

    printf("Codigo Hamming: %s\n", output_bits);
}

int main() {
    char input_bits[100];
    printf("Ingrese los bits de datos: ");
    scanf("%s", input_bits);

    processBits(input_bits);

    return 0;
}
