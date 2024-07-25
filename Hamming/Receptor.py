def hamming_7_4_decoder(hamming_code):
    """
    Decodifica un código Hamming de 7 bits y corrige un único error si es necesario.
    
    :param hamming_code: Lista de 7 bits (0 o 1) Hamming code
    :return: Lista de 4 bits de datos, bits de paridad calculados y posición del error (0 si no hay error)
    """
    if len(hamming_code) != 7:
        raise ValueError("Input must be a list of 7 bits.")
    
    # Verificar que los bits sean 0 o 1
    if any(bit not in (0, 1) for bit in hamming_code):
        raise ValueError("Solo pueden ser bits 0 o 1.")
    
    # Asignar bits de datos y paridad a sus posiciones
    d1, d2, d3, p1, d4, p2, p3 = hamming_code
    
    # Calcular bits de paridad
    p1_calc = d1 ^ d2 ^ d3
    p2_calc = d1 ^ d2 ^ d4
    p3_calc = d1 ^ d3 ^ d4
    
    # Determinar la posición del error
    error_position = (p3 != p3_calc) * 1 + (p2 != p2_calc) * 2 + (p1 != p1_calc) * 4
    
    # Corregir el error si es necesario
    if error_position != 0:
        inverted_index = 7 - error_position
        hamming_code[inverted_index] ^= 1
    
    # Extraer bits de datos corregidos
    data_bits = [hamming_code[0], hamming_code[1], hamming_code[2], hamming_code[4]]
    
    return data_bits, [p1_calc, p2_calc, p3_calc], error_position

def process_input_bits(input_bits):
    len_bits = len(input_bits)
    if len_bits not in [7, 14]:
        raise ValueError("Debe ingresar exactamente 7 o 14 bits.")
    
    input_bits = list(map(int, input_bits))
    blocks = [input_bits[i:i + 7] for i in range(0, len_bits, 7)]

    corrected_bits = []
    original_message = []
    no_errors = True

    for i, block in enumerate(blocks):
        data_bits, parities, error_position = hamming_7_4_decoder(block)
        block_status = "no hubo error" if error_position == 0 else f"error corregido en la posición {error_position}"
        
        if error_position != 0:
            no_errors = False
        
        corrected_block = block[:]
        corrected_bits.extend(corrected_block)
        
        original_message.extend(data_bits)
        
        print(f"Bloque {i + 1} ({block_status}): {corrected_block}")

    if no_errors:
        print(f"El mensaje es: {''.join(map(str, original_message))}")
    else:
        print(f"Mensaje corregido: {corrected_bits}")

# Solicitar al usuario que ingrese los bits de datos
print("****************")
print("Bienvenido al algoritmo de Hamming (Receptor)")
print("****************")
input_bits = input("Ingresa los bits de datos recibidos del emisor: ")

process_input_bits(input_bits)