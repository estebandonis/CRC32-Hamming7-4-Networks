import socket

def hamming_7_4_decoder(hamming_code):
    if len(hamming_code) != 7:
        raise ValueError("Input must be a list of 7 bits.")
    
    if any(bit not in (0, 1) for bit in hamming_code):
        raise ValueError("Solo pueden ser bits 0 o 1.")
    
    d1, d2, d3, p1, d4, p2, p3 = hamming_code
    
    p1_calc = d1 ^ d2 ^ d3
    p2_calc = d1 ^ d2 ^ d4
    p3_calc = d1 ^ d3 ^ d4
    
    error_position = (p3 != p3_calc) * 1 + (p2 != p2_calc) * 2 + (p1 != p1_calc) * 4
    
    if error_position != 0:
        inverted_index = 7 - error_position
        hamming_code[inverted_index] ^= 1
    
    data_bits = [hamming_code[0], hamming_code[1], hamming_code[2], hamming_code[4]]
    
    return data_bits, [p1_calc, p2_calc, p3_calc], error_position

def bits_to_char(bits):
    return chr(int(''.join(map(str, bits)), 2))

def process_input_bits(input_bits):
    len_bits = len(input_bits)
    if len_bits % 8 != 0:
        raise ValueError("Debe ingresar un número de bits múltiplo de 8.")
    
    input_bits = list(map(int, input_bits))
    blocks = [input_bits[i:i + 8] for i in range(0, len_bits, 8)]

    corrected_bits = []
    original_message = []
    no_errors = True

    for i, block in enumerate(blocks):
        hamming_block = block[:7]
        parity_bit = block[7]
        data_bits, parities, error_position = hamming_7_4_decoder(hamming_block)
        data_bits.append(parity_bit)  # Adding the last parity bit from the original block
        block_status = "no hubo error" if error_position == 0 else f"error corregido en la posición {error_position}"
        
        if error_position != 0:
            no_errors = False
        
        corrected_block = hamming_block + [parity_bit]
        corrected_bits.extend(corrected_block)
        
        original_message.extend(data_bits)
        
        print(f"Bloque {i + 1} ({block_status}): {corrected_block}")

    if no_errors:
        print("El mensaje es: ", ''.join(bits_to_char(original_message[i:i + 8]) for i in range(0, len(original_message), 8)))
    else:
        print(f"Mensaje corregido: {corrected_bits}")

def receive_message():
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Esperando conexión...")

        conn, addr = s.accept()
        with conn:
            print(f"Conexión Entrante del proceso {addr}")
            data = b''
            while True:
                part = conn.recv(1024)
                if not part:
                    break
                data += part

            input_bits = data.decode()
            print(f"Bits recibidos: {input_bits}")
            process_input_bits(input_bits)

print("****************")
print("Bienvenido al algoritmo de Hamming (Receptor)")
print("****************")

receive_message()
