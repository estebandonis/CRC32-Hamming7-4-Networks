#include <stdio.h>

void hamming_7_4_decoder(int code[7]) {
    int p1, p2, p3, error_pos;

    // Extraer bits de paridad y datos
    int d1 = code[0];
    int d2 = code[1];
    int d3 = code[2];
    int p1_received = code[3];
    int d4 = code[4];
    int p2_received = code[5];
    int p3_received = code[6];

    // Calcular los bits de paridad esperados
    p1 = d1 ^ d2 ^ d3;
    p2 = d1 ^ d2 ^ d4;
    p3 = d1 ^ d3 ^ d4;

    printf("Bits de paridad calculados: p1: %d, p2: %d, p3: %d\n", p1, p2, p3);
    printf("Bits de paridad recibidos:  p1: %d, p2: %d, p3: %d\n", p1_received, p2_received, p3_received);

    // Calcular la posición del error
    error_pos = (p3_received ^ p3) << 2 | (p2_received ^ p2) << 1 | (p1_received ^ p1);

    if (error_pos == 0) {
        printf("No hubo errores en los datos.\n");
    } else {
        printf("Se detecto un error en la posicion %d.\n", error_pos);

        // Corregir el error
        code[error_pos - 1] = !code[error_pos - 1];
        printf("El codigo corregido es: ");
        for (int i = 0; i < 7; i++) {
            printf("%d", code[i]);
        }
        printf("\n");
    }

    // Mostrar los datos decodificados
    printf("Datos decodificados: %d%d%d%d\n", code[0], code[1], code[2], code[4]);
}

int main() {
    int code[7];

    printf("Ingrese 7 bits de datos codificados (separados por espacios, e.g., '1 0 1 1 0 1 0'): ");
    for (int i = 0; i < 7; i++) {
        scanf("%d", &code[i]);
    }
    printf("****************************************************");
    printf("**********Mensaje recibido del receptor*************");
    printf("****************************************************");
    printf("Mensaje recibido del receptor: ");
    for (int i = 0; i < 7; i++) {
        printf("%d", code[i]);
    }
    printf("\n");

    hamming_7_4_decoder(code);

    return 0;
}
