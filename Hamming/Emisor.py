def hamming_7_4_encoder(data_bits):
    """
    Encode 4 data bits into 7-bit Hamming code.
    
    :param data_bits: List of 4 bits (0 or 1)
    :return: List of 7 bits (0 or 1) Hamming code
    """
    if len(data_bits) != 4:
        raise ValueError("Input must be a list of 4 bits.")
    
    # Ensure the data bits are either 0 or 1
    if any(bit not in (0, 1) for bit in data_bits):
        raise ValueError("Bits must be 0 or 1.")
    
    # Assign data bits to their positions
    d1, d2, d3, d4 = data_bits
    
    # Calculate parity bits
    p1 = d1 ^ d2 ^ d3
    p2 = d1 ^ d2 ^ d4
    p3 = d1 ^ d3 ^ d4
    
    # Construct the 7-bit Hamming code
    hamming_code = [d1, d2, d3, p1, d4, p2, p3]
    
    return hamming_code

# Ejemplo de uso
data_bits = [1, 1, 0, 0]  # Por ejemplo, estos son los bits de datos
encoded_bits = hamming_7_4_encoder(data_bits)
print(f"Bits de datos: {data_bits}")
print(f"Bits de paridad: {encoded_bits[4:]}")
print(f"Bits codificados: {encoded_bits}")
