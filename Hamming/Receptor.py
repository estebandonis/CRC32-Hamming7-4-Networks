import socket

# Función para calcular los bits de paridad de Hamming(12,8)
def calculate_parity_bits(data_bits):
    d1, d2, d3, d4, d5, d6, d7, d8 = data_bits
    p1 = d1 ^ d2 ^ d4 ^ d5 ^ d7
    p2 = d1 ^ d3 ^ d4 ^ d6 ^ d7
    p3 = d2 ^ d3 ^ d4 ^ d8
    p4 = d5 ^ d6 ^ d7 ^ d8
    return [p1, p2, p3, p4]

# Función para decodificar y corregir datos usando Hamming(12,8)
def hamming_decode(received_bits):
    if len(received_bits) != 12:
        raise ValueError("El bloque debe tener exactamente 12 bits.")

    d8, d7, d6, d5, p4, d4, d3, d2, p3, d1, p2, p1 = received_bits

    # Calcular los bits de control
    c1 = p1 ^ d1 ^ d2 ^ d4 ^ d5 ^ d7
    c2 = p2 ^ d1 ^ d3 ^ d4 ^ d6 ^ d7
    c3 = p3 ^ d2 ^ d3 ^ d4 ^ d8
    c4 = p4 ^ d5 ^ d6 ^ d7 ^ d8

    error_pos = c1 + (c2 << 1) + (c3 << 2) + (c4 << 3)
    
    if error_pos > 0:
        if error_pos <= 12:
            received_bits[error_pos - 1] ^= 1
        else:
            print(f"Error: Posición de error ({error_pos}) fuera de rango.")
    
    # Extraer los bits de datos
    data_bits = [d8, d7, d6, d5, d4, d3, d2, d1]
    return data_bits

# Función para recibir datos a través de sockets
def receive_data(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Escuchando en el puerto {port}...")
        conn, addr = s.accept()
        with conn:
            print(f'Conectado por {addr}')
            data = conn.recv(1024)
            return data.decode()

# Función principal del receptor
def main():
    ip = '127.0.0.1'
    port = 65432
    received_message = receive_data(ip, port)
    
    # Capa de Transmisión
    bits = [int(bit) for bit in received_message]
    print(f"Mensaje recibido en bits: {''.join(map(str, bits))}")
    
    corrected_bits = []
    blocks = []
    parity_bits = []

    # Capa de Enlace
    for i in range(0, len(bits), 12):
        block = bits[i:i + 12]
        if len(block) == 12:
            blocks.append(block)
            corrected_block = hamming_decode(block)
            corrected_bits.extend(corrected_block)
            parity_bits.append(block[:4])  # Los primeros 4 bits son los de paridad
    
    # Imprimir bloques y bits de paridad
    print("\nBloques de 12 bits recibidos:")
    for i, block in enumerate(blocks):
        print(f"Bloque {i + 1}: {''.join(map(str, block))}")

    print("\nBits de paridad:")
    for i, pbits in enumerate(parity_bits):
        print(f"Bloque {i + 1} - Bits de paridad: {''.join(map(str, pbits))[:4]}")
    
    # Capa de Presentación
    if len(corrected_bits) % 8 != 0:
        print("Error en el mensaje recibido.")
    else:
        print("Mensaje recibido y corregido.")
    
    # Extraer bits de datos sin los bits de paridad y convertir a caracteres ASCII
    ascii_chars = []
    for i in range(0, len(corrected_bits), 8):
        byte = corrected_bits[i:i + 8]  # Extraer d8, d7, d6, d5, d4, d3, d2, d1
        if len(byte) == 8:
            char = chr(int(''.join(map(str, byte)), 2))
            ascii_chars.append(char)

    # Capa de Aplicación
    decoded_message = ''.join(ascii_chars)
    print(f"\nMensaje en bits concatenados: {''.join(map(str, corrected_bits))}")
    print(f"Mensaje decodificado: {decoded_message}")

if __name__ == '__main__':
    main()
