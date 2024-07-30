#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <time.h>

#pragma comment(lib, "ws2_32.lib")

// Función para solicitar el mensaje al usuario
void solicitarMensaje(char* mensaje) {
    printf("Ingrese el mensaje: ");
    scanf("%s", mensaje);
}

// Función para codificar un byte usando Hamming(12,8)
void codificarHamming128(unsigned char byte, char* hamming) {
    // Bits de datos
    int d1 = (byte >> 0) & 1;
    int d2 = (byte >> 1) & 1;
    int d3 = (byte >> 2) & 1;
    int d4 = (byte >> 3) & 1;
    int d5 = (byte >> 4) & 1;
    int d6 = (byte >> 5) & 1;
    int d7 = (byte >> 6) & 1;
    int d8 = (byte >> 7) & 1;

    // Calcular bits de paridad
    int p1 = d1 ^ d2 ^ d4 ^ d5 ^ d7; // Paridad para la posición 1
    int p2 = d1 ^ d3 ^ d4 ^ d6 ^ d7; // Paridad para la posición 2
    int p3 = d2 ^ d3 ^ d4 ^ d8;      // Paridad para la posición 4
    int p4 = d5 ^ d6 ^ d7 ^ d8;      // Paridad para la posición 8

    // Formatear en la cadena Hamming(12,8)
    hamming[0] = d8 + '0';  // p1
    hamming[1] = d7 + '0';  // p2
    hamming[2] = d6 + '0';  // d1
    hamming[3] = d5 + '0';  // p3
    hamming[4] = p4 + '0';  // d2
    hamming[5] = d4 + '0';  // d3
    hamming[6] = d3 + '0';  // d4
    hamming[7] = d2 + '0';  // p4
    hamming[8] = p3 + '0';  // d5
    hamming[9] = d1 + '0';  // d6
    hamming[10] = p2 + '0'; // d7
    hamming[11] = p1 + '0'; // d8
}

// Función para codificar el mensaje entero en Hamming(12,8)
void codificarMensajeHamming(const char* mensaje, char* mensajeHamming) {
    int len = strlen(mensaje);
    mensajeHamming[0] = '\0';
    for (int i = 0; i < len; i++) {
        char hamming[13] = {0};
        unsigned char temp = mensaje[i];
        codificarHamming128(temp, hamming);
        strcat(mensajeHamming, hamming);
    }
}

// Función para aplicar ruido al mensaje
void aplicarRuido(char* mensaje, float probabilidadError) {
    int len = strlen(mensaje);
    srand(time(NULL));
    for (int i = 0; i < len; i++) {
        if ((float)rand() / RAND_MAX < probabilidadError) {
            mensaje[i] = (mensaje[i] == '0') ? '1' : '0';
        }
    }
}

// Función para enviar la información a través de sockets
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
    char mensajeHamming[1200] = {0}; // Ajusta el tamaño según el número de caracteres y bits generados
    float probabilidadError;
    const char* direccionIP = "127.0.0.1";
    const int puerto = 65432;

    solicitarMensaje(mensaje);
    codificarMensajeHamming(mensaje, mensajeHamming);

    printf("Mensaje codificado en Hamming (en bits): %s\n", mensajeHamming);

    printf("Ingrese la probabilidad de error (ej. 0.01 para 1%%): ");
    scanf("%f", &probabilidadError);
    aplicarRuido(mensajeHamming, probabilidadError);

    enviarInformacion(mensajeHamming, direccionIP, puerto);

    return 0;
}
