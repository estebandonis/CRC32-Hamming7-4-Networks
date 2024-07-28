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
    float probabilidadError;
    const char* direccionIP = "127.0.0.1";
    const int puerto = 65432;

    solicitarMensaje(mensaje);
    codificarMensaje(mensaje, mensajeBinario);

    printf("Mensaje codificado (en bits): %s\n", mensajeBinario);

    printf("Ingrese la probabilidad de error (ej. 0.01 para 1%%): ");
    scanf("%f", &probabilidadError);
    aplicarRuido(mensajeBinario, probabilidadError);

    enviarInformacion(mensajeBinario, direccionIP, puerto);

    return 0;
}
