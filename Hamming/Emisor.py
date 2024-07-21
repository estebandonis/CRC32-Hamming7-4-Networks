def hamming_7_4_encoder(data_bits):
    """
    Codifica 4 bits de datos en un código Hamming de 7 bits.
    
    :param data_bits: Lista de 4 bits (0 o 1) para codificar
    :return: Lista de 7 bits (0 o 1) Hamming code
    """
    if len(data_bits) != 4:
        raise ValueError("Input must be a list of 4 bits.")
    
    # Verificar que los bits sean 0 o 1
    if any(bit not in (0, 1) for bit in data_bits):
        raise ValueError("Bits must be 0 or 1.")
    
    # Asignar bits de datos a sus posiciones
    d1, d2, d3, d4 = data_bits
    
    # Calcular bits de paridad (p1, p2, p3)
    p1 = d1 ^ d2 ^ d3 
    p2 = d1 ^ d2 ^ d4
    p3 = d1 ^ d3 ^ d4
    
    # Construir el código Hamming de 7 bits
    hamming_code = [d1, d2, d3, p1, d4, p2, p3]
    
    return hamming_code

# Ejemplo de uso mensaje del emisor
data_bits = [0, 1, 1, 0]  # Solo se puede poner 4 bits de datos (0 o 1)
encoded_bits = hamming_7_4_encoder(data_bits)
print("************************************************")
print("************ ALGORITMO DE HAMMING **************")
print("************************************************")
print("Mensaje del emisor:", data_bits)
print(f"Bit de paridad p1: {encoded_bits[3]}")
print(f"Bit de paridad p2: {encoded_bits[5]}")
print(f"Bit de paridad p3: {encoded_bits[6]}")
print(f"Bits de paridad: {encoded_bits[4:]}")
print(f"Bits codificados: {encoded_bits}")
print("************************************************")
