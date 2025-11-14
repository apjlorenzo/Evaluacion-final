def fnv1_64(data: str) -> int:
    # Constantes para FNV-1 64-bit
    FNV_PRIME_64 = 1099511628211
    FNV_OFFSET_BASIS_64 = 1469598103934665603

    # Asegurarse de que la entrada es una cadena y convertirla a bytes
    if not isinstance(data, str):
        data = str(data)
    data_bytes = data.encode('utf-8')

    # Inicializar el hash
    h = FNV_OFFSET_BASIS_64

    # Aplicar el algoritmo FNV-1
    for byte in data_bytes:
        h = (h * FNV_PRIME_64) ^ byte
    h = h & 0xFFFFFFFFFFFFFFFF 
    return h