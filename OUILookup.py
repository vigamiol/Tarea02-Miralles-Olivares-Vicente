import subprocess
import getopt
import sys
            
global contenido,computadorIP
computadorIP="192.168.1.30"
with open('manuf','r',encoding='utf-8') as archivo:
    contenido=archivo.readlines()


# Función para obtener los datos de fabricación de una tarjeta de red por IP
def obtener_datos_por_ip(ip):
    #"aplica la mascara" a la direcicon ip del computador
    aux=computadorIP.split('.')
    compa='.'.join(aux[:3])
    #"aplica la mascara" a la direccion ip que se quiere buscar para comprobar si pertenecen a la misma red
    prueba=ip.split('.')
    comprobacion='.'.join(prueba[:3])
    if compa==comprobacion:
        try:
            # Ejecutar el comando ARP para obtener la dirección MAC
            resultado = subprocess.check_output(["arp", "-a", ip])
            # Decodificar la salida en una cadena
            resultado = resultado.decode("ISO-8859-1")
            # Buscar la dirección MAC en la salida
            partes = resultado.split()
            mac = partes[11] 
              
            return mac
        except Exception as e:
            print("Error al obtener la dirección MAC:", str(e))
    else:
        print("Error: ip is outside the host network")
        sys.exit(2)
    return None

# Función para obtener los datos de fabricación de una tarjeta de red por MAC
def obtener_datos_por_mac(mac):
    # Implementa la lógica para obtener los datos por MAC aquí
    fabricantes={}
    for linea in contenido:
        partes = linea.strip().split('\t')
        if len(partes) >= 2:
            macs = partes[0]
            fabricante = partes[1]
            fabricantes[macs] = fabricante
    if mac in fabricantes:
        print(f"MAC Adress: {mac} \nFabricante   : {fabricantes[mac]}")
    else:
        print(f"MAC Adress: {mac} \nFabricante   : Not found")
        

# Función para obtener la tabla ARP.
def obtener_tabla_arp():
    try:
        arp_output = subprocess.getoutput("arp -a").split('\n')[3:]
        arp_entries = [line.split() for line in arp_output if line.strip()]

        print("IP/MAC/Fabricante:")
        for entry in arp_entries:
            ip = entry[0]
            mac = entry[1].upper()
            mac_prefix = mac.replace(':', '').upper()[:6]

            fabricante = "Not found"
            
            for line in contenido:
                if line.startswith(mac_prefix):
                        parts = line.strip().split('\t')
                        if len(parts) >= 2:
                            fabricante = parts[1].strip()
                            break

            print(f"{ip} / {mac} / {fabricante}")
        
    except Exception as e:
        print(f"Error: {e}")


def main(argv):
    

    try:
        opts, args = getopt.getopt(argv, "", ["ip=","mac=","arp","help"])

    except getopt.GetoptError:
        print("Use: python OUILookup.py --ip <IP> | --mac <IP> | --arp | [--help] \n --ip : IP del host a consultar. \n --mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.  \n --arp: muestra los fabricantes de los host disponibles en la tabla arp. \n --help: muestra este mensaje y termina.")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("--ip"):
            resultado=obtener_datos_por_ip(arg)
            resultado=resultado.upper()
            obtener_datos_por_mac(resultado)
            sys.exit()
        elif opt in ("--mac"):
            obtener_datos_por_mac(arg)
            sys.exit()
        elif opt in ("--arp"):
            obtener_tabla_arp()
            sys.exit()
        elif opt in ("--help"):
            print("Use: python OUILookup.py --ip <IP> | --mac <IP> | --arp | [--help] \n --ip : IP del host a consultar. \n --mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.  \n --arp: muestra los fabricantes de los host disponibles en la tabla arp. \n --help: muestra este mensaje y termina.")
            sys.exit()
    print("Use: python OUILookup.py --ip <IP> | --mac <IP> | --arp | [--help] \n --ip : IP del host a consultar. \n --mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.  \n --arp: muestra los fabricantes de los host disponibles en la tabla arp. \n --help: muestra este mensaje y termina.")
    sys.exit()
if __name__ == "__main__":
    main(sys.argv[1:])
