#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <winsock2.h>
#include <time.h>

#pragma comment(lib, "ws2_32.lib")

void solicitarMensaje(char* mensaje) {
    printf("Ingrese el mensaje: ");
    scanf("%s", mensaje);
}

void codificarMensaje(const char* mensaje, char* mensajeBinario) {
    int len = strlen(mensaje);
    mensajeBinario[0] = '\0';
    for (int i = 0; i < len; i++) {
        char bin[9] = {0};
        unsigned char temp = mensaje[i];
        for (int j = 7; j >= 0; j--) {
            bin[j] = (temp & 1) + '0';
            temp >>= 1;
        }
        strcat(mensajeBinario, bin);
    }
}

void hammingEncoder(int* data_bits, int* hamming_code, int m, int n) {
    int parity_bits = n - m;
    int j = 0, k = 0;

    for (int i = 1; i <= n; i++) {
        if ((i & (i - 1)) == 0) {
            hamming_code[i-1] = 0; // Inicializamos los bits de paridad a 0
        } else {
            hamming_code[i-1] = data_bits[j++];
        }
    }

    for (int i = 0; i < parity_bits; i++) {
        int parity_pos = (1 << i);
        int parity = 0;

        for (int j = 1; j <= n; j++) {
            if (j & parity_pos) {
                parity ^= hamming_code[j-1];
            }
        }
        hamming_code[parity_pos-1] = parity;
    }
}

void calcularIntegridad(const char* mensajeBinario, char* mensajeConHamming) {
    int len = strlen(mensajeBinario);
    int m = 4; // bits de datos
    int n = 7; // bits de código Hamming

    int data[len];
    for (int i = 0; i < len; i++) {
        data[i] = mensajeBinario[i] - '0';
    }

    int num_blocks = (len + m - 1) / m;
    mensajeConHamming[0] = '\0';

    for (int i = 0; i < num_blocks; i++) {
        int start = len - m * (i + 1);
        int end = len - m * i;
        int segment[m];
        memset(segment, 0, m * sizeof(int));

        for (int j = 0; j < (end - start); j++) {
            if (start + j >= 0) {
                segment[m - (end - start) + j] = data[start + j];
            }
        }

        int hamming[n];
        hammingEncoder(segment, hamming, m, n);
        
        char block_output[n + 1];
        for (int k = 0; k < n; k++) {
            block_output[k] = hamming[k] + '0';
        }
        block_output[n] = '\0';
        strcat(mensajeConHamming, block_output);
    }
}

void aplicarRuido(char* mensaje, float probabilidadError) {
    int len = strlen(mensaje);
    srand(time(NULL));
    for (int i = 0; i < len; i++) {
        if ((float)rand() / RAND_MAX < probabilidadError) {
            mensaje[i] = (mensaje[i] == '0') ? '1' : '0';
        }
    }
}

void enviarInformacion(const char* mensaje, const char* direccionIP, int puerto) {
    WSADATA wsa;
    SOCKET s;
    struct sockaddr_in server;

    printf("\nInicializando Winsock...");
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        printf("Error. Codigo: %d", WSAGetLastError());
        return;
    }
    printf("Inicializado.\n");

    if ((s = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        printf("No se pudo crear el socket. Codigo: %d", WSAGetLastError());
        WSACleanup();
        return;
    }
    printf("Socket creado.\n");

    server.sin_addr.s_addr = inet_addr(direccionIP);
    server.sin_family = AF_INET;
    server.sin_port = htons(puerto);

    if (connect(s, (struct sockaddr*)&server, sizeof(server)) < 0) {
        printf("Conexión fallida\n");
        closesocket(s);
        WSACleanup();
        return;
    }
    printf("Conectado al servidor.\n");

    if (send(s, mensaje, strlen(mensaje), 0) < 0) {
        printf("No se pudo enviar el mensaje\n");
        closesocket(s);
        WSACleanup();
        return;
    }
    printf("Mensaje enviado.\n");

    closesocket(s);
    WSACleanup();
}

int main() {
    char mensaje[100];
    char mensajeBinario[800] = {0};
    char mensajeConHamming[1400] = {0};
    float probabilidadError;
    char direccionIP[20];
    int puerto;

    solicitarMensaje(mensaje);
    codificarMensaje(mensaje, mensajeBinario);
    calcularIntegridad(mensajeBinario, mensajeConHamming);

    printf("Mensaje codificado (en bits): %s\n", mensajeBinario);
    //printf("Mensaje con código Hamming: %s\n", mensajeConHamming);

    printf("Ingrese la probabilidad de error (ej. 0.01 para 1%%): ");
    scanf("%f", &probabilidadError);
    aplicarRuido(mensajeConHamming, probabilidadError);

    printf("Ingrese la dirección IP del receptor: ");
    scanf("%s", direccionIP);
    printf("Ingrese el puerto del receptor: ");
    scanf("%d", &puerto);

    enviarInformacion(mensajeConHamming, direccionIP, puerto);

    return 0;
}
