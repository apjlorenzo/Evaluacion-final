from dahuffman import HuffmanCodec as huffmancodec #importacion libreria para compresion de texto con huffman
import os
import rsa
import binascii

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

def main():
    # Variables globales para almacenar datos
    publickey = None
    privatekey = None
    hash_mensaje = None
    firma_digital = None
    mensaje_comprimido = None
    
    # Variables temporales para simular envio/recepcion
    mensaje_enviado = None
    firma_enviada = None
    clave_publica_enviada = None
    
    while True:
        os.system("cls")    
        mensaje = input("INGRESE UN MENSAJE DE TEXTO: ")

        while True:
            os.system("cls")
            print("TEXTO INGRESADO:", mensaje)
            print("\n--------MENU DE OPCIONES--------")
            print("1. Hashing (FNV-1)")
            print("2. Comprimir mensaje huffman")
            print("3. Firmar el hash con la clave privada RSA")
            print("4. Simular envio (mensaje comprimido + firma + clave publica)")
            print("5. Descomprimir y verificar firma (clave publica)")
            print("6. Mostrar si el mensaje es autentico o no")
            print("7. Regresar")
            opcion = input(" --> Seleccione una opcion: ")
            
            if opcion == "1":
                hash_mensaje = fnv1_64(mensaje)
                print(f"\nEl hash FNV-1 generado del mensaje es: {hash_mensaje}")
                print(f"Hash en hexadecimal: {hex(hash_mensaje)}")
                input("Presione Enter para continuar...")

            elif opcion == "2":
                codec = huffmancodec.from_data(mensaje)
                mensaje_comprimido = codec.encode(mensaje)
                
                print("Mensaje comprimido correctamente.")
                print("--------------------------------------------")
                
                tamaño_original = len(mensaje.encode('utf-8'))
                
                print(f"\nTamaño de mensaje original: {tamaño_original} bytes")
                print(f"Tamaño de mensaje comprimido: {len(mensaje_comprimido)} bytes")
                print(f"Tasa de compresion: {(1 - len(mensaje_comprimido)/tamaño_original)*100:.2f}%")
                input("Presione Enter para continuar...")
            
            elif opcion == "3":
                # Generar claves RSA
                print("\nGenerando claves RSA (2048 bits)...")
                print("Esto puede tomar unos segundos...")
                
                publickey, privatekey = rsa.newkeys(2048)
                
                # Calcular hash del mensaje
                if hash_mensaje is None:
                    hash_mensaje = fnv1_64(mensaje)
                
                # Convertir el hash a bytes para firmar
                hash_bytes = str(hash_mensaje).encode('utf-8')
                
                # Firmar el hash con la clave privada
                firma_digital = rsa.sign(hash_bytes, privatekey, 'SHA-256')
                
                print("\n" + "="*60)
                print("FIRMA DIGITAL EXITOSA")
                print("="*60)
                print(f"\nHash FNV-1 del mensaje: {hash_mensaje}")
                print(f"\nFirma Digital (primeros 100 caracteres):")
                print(binascii.hexlify(firma_digital).decode()[:100] + "...")
                
                print(f"\nTamaño de la firma: {len(firma_digital)} bytes")
                
                print("\n--- CLAVE PUBLICA ---")
                print(f"Exponente (e): {publickey.e}")
                print(f"Modulo (n): {str(publickey.n)[:100]}...")
                print(f"Tamaño de la clave publica: {len(str(publickey.n))} caracteres")
                
                print("\n--- CLAVE PRIVADA (NO TRANSMITIR) ---")
                print(f"Exponente (d): {str(privatekey.d)[:50]}...")
                print(f"[PRIVADA] No se muestra completa por seguridad")
                
                print("\n" + "="*60)
                input("Presione Enter para continuar...")
            
            elif opcion == "4":
                if firma_digital is None or publickey is None or mensaje_comprimido is None:
                    print("\n[ERROR] Debe completar los pasos anteriores primero:")
                    print("1. Opcion 1: Calcular hash")
                    print("2. Opcion 2: Comprimir mensaje")
                    print("3. Opcion 3: Generar claves y firmar")
                    input("Presione Enter para continuar...")
                    continue
                
                print("\n" + "="*60)
                print("SIMULANDO ENVIO DE DATOS")
                print("="*60)
                
                # Simular envio: almacenar en variables temporales
                mensaje_enviado = mensaje_comprimido
                firma_enviada = firma_digital
                clave_publica_enviada = publickey
                
                print("\n[*] Mensaje comprimido: ENVIADO")
                print(f"    Tamaño: {len(mensaje_enviado)} bytes")
                
                print("\n[*] Firma digital: ENVIADA")
                print(f"    Tamaño: {len(firma_enviada)} bytes")
                print(f"    Valor (primeros 50 caracteres): {binascii.hexlify(firma_enviada).decode()[:50]}...")
                
                print("\n[*] Clave publica: ENVIADA")
                print(f"    Exponente (e): {clave_publica_enviada.e}")
                print(f"    Modulo (n): {str(clave_publica_enviada.n)[:80]}...")
                
                print("\n[Clave privada: NO TRANSMITIDA (Segura)")
                
                print("\n" + "="*60)
                print("Los datos se encuentran en variables temporales")
                print("esperando ser recibidos y verificados...")
                print("="*60)
                
                input("Presione Enter para continuar...")
            
            elif opcion == "5":
                if mensaje_enviado is None or firma_enviada is None or clave_publica_enviada is None:
                    print("\nNo hay datos enviados. Debe realizar la opcion 4 primero")
                    input("Presione Enter para continuar...")
                    continue
                
                print("\n" + "="*60)
                print("SIMULANDO RECEPCION Y VERIFICACION")
                print("="*60)
                
                print("\n[*] Recibiendo datos...")
                print(f"    Mensaje comprimido: RECIBIDO ({len(mensaje_enviado)} bytes)")
                print(f"    Firma digital: RECIBIDA ({len(firma_enviada)} bytes)")
                print(f"    Clave publica: RECIBIDA")
                
                # Descomprimir mensaje
                print("\n[*] Descomprimiendo mensaje...")
                codec = huffmancodec.from_data(mensaje)  # Recrear codec del mensaje original
                try:
                    mensaje_descomprimido = codec.decode(mensaje_enviado)
                    print(f"    Mensaje descomprimido: '{mensaje_descomprimido}'")
                except:
                    print(" No se puede descomprimir sin el codec original")
                    input("Presione Enter para continuar...")
                    continue
                
                # Calcular hash del mensaje descomprimido
                print("\n[*] Calculando hash FNV-1 del mensaje recibido...")
                hash_recibido = fnv1_64(mensaje_descomprimido)
                print(f"Hash original: {hash_mensaje}")
                print(f"Hash recibido: {hash_recibido}")
                
                if hash_mensaje == hash_recibido:
                    print("Hashes coinciden")
                else:
                    print("Hashes NO coinciden - El mensaje fue modificado")
                
                # Verificar firma con clave publica
                print("\n[*] Verificando firma digital con clave publica...")
                hash_bytes = str(hash_recibido).encode('utf-8')
                
                try:
                    rsa.verify(hash_bytes, firma_enviada, clave_publica_enviada)
                    print(" Firma verificada exitosamente")
                    es_autentico = True
                except rsa.pkcs1.VerificationError:
                    print(" Firma NO valida - Autenticidad cuestionable")
                    es_autentico = False
                
                print("\n" + "="*60)
                
                input("Presione Enter para continuar...")
            
            elif opcion == "6":
                if mensaje_enviado is None or firma_enviada is None:
                    print("\nDebe realizar las opciones 4 y 5 primero")
                    input("Presione Enter para continuar...")
                    continue
                
                print("\n" + "="*60)
                print("RESULTADO DE AUTENTICIDAD")
                print("="*60)
                
                # Recrear el proceso de verificacion
                codec = huffmancodec.from_data(mensaje)
                try:
                    mensaje_descomprimido = codec.decode(mensaje_enviado)
                except:
                    print("\n[X] ERROR: No se puede descomprimir el mensaje")
                    input("Presione Enter para continuar...")
                    continue
                
                hash_recibido = fnv1_64(mensaje_descomprimido)
                hash_bytes = str(hash_recibido).encode('utf-8')
                
                try:
                    rsa.verify(hash_bytes, firma_enviada, clave_publica_enviada)
                    autenticidad = True
                except rsa.pkcs1.VerificationError:
                    autenticidad = False
                
                print(f"\nMensaje original: '{mensaje}'")
                print(f"Mensaje recibido: '{mensaje_descomprimido}'")
                print(f"\nHash original: {hash_mensaje}")
                print(f"Hash recibido: {hash_recibido}")
                
                if autenticidad and mensaje == mensaje_descomprimido:
                    print("\n" + "="*60)
                    print("MENSAJE AUTENTICO Y SIN MODIFICACIONES")
                    print("La firma digital es valida")
                    print("El contenido no fue alterado")
                    print("El remitente es verificable")
                    print("="*60)
                else:
                    print("\n" + "="*60)
                    print("MENSAJE NO AUTENTICO O MODIFICADO")
                    if not autenticidad:
                        print("La firma digital es INVALIDA")
                    if mensaje != mensaje_descomprimido:
                        print("El contenido FUE ALTERADO")
                    print("="*60)
                
                input("Presione Enter para continuar...")
            
            elif opcion == "7":
                break   

            else:
                print("Opcion no valida. Por favor seleccione una opcion valida.")
                input("Presione Enter para continuar...")
                
main()