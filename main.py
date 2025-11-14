# Importar libreria para compresion de texto con huffman
from dahuffman import HuffmanCodec as huffmancodec
import os

def fnv1_64(data: str) -> int:
    # Esta función se mueve para que esté definida ANTES de main(), permitiendo que main() la llame.
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
    # En Python, para asegurar estrictamente el límite de 64 bits:
    h = h & 0xFFFFFFFFFFFFFFFF 
    return h


def main():
    while True:
        os.system("cls")    
        mensaje = input("INGRESE UN MENSAJE DE TEXTO: ")

        while True:
            os.system("cls")
            print("TEXTO INGRESADO:", mensaje)
            print("\n--------MENU DE OPCIONES--------")
            print("1. Hashing (FNV-1 64-bit)")
            print("2. Compresion de texto")
            print("3. Regresar")
            opcion = input(" --> Seleccione una opcion: ")
            
            if opcion == "1":
                resultado_hash = fnv1_64(mensaje)
                print(f"El hash FNV-1 64-bit del mensaje es: {resultado_hash}")
                input("Presione Enter para continuar...")

            elif opcion == "2":
                codec = huffmancodec.from_data(mensaje) #Marca las frecuencias de los caracteres en el mensaje, crea el arbol y genera los codigos
                mensaje_comprimido = codec.encode(mensaje)
                
                print("Mensaje comprimido correctamente.")
                print("--------------------------------------------")
                
                tamaño_original = len(mensaje.encode('utf-8'))
                
                print(f"\nTamaño de mensaje original: {tamaño_original} bytes")
                print(f"Tamaño de mensaje comprimido: {len(mensaje_comprimido)} bytes")
                input("Presione Enter para continuar...")
            
            elif opcion == "3":
                break   

            else:
                print("Opcion no valida. Por favor seleccione 1 o 2.")
                print("Presiona una tecla para continuar...")
                
main()