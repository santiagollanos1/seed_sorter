import serial
import time

class Arduino:
    def __init__(self, port="COM3", baudrate=9600, timeout=1):
        self.serial = None
        try:
            self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
            print(f"Conectado al puerto {port}")
            time.sleep(2) 
        except serial.SerialException as e:
            print(f"Error al conectar al puerto {port}: {e}")
            raise

    def send_command(self, command):
        if self.serial and self.serial.is_open:
            try:
                self.serial.write(f"{command}\r\n".encode())
                self.serial.flush()  
            except serial.SerialException as e:
                print(f"Error al enviar comando: {e}")
        else:
            print("No hay conexión serial")

    def get_data(self):
        if self.serial and self.serial.is_open:
            try:
                data = self.serial.readline().decode().strip()
                if data:
                    print(f"OK")
                    return data
                return None
            except serial.SerialException as e:
                print(f"Error al leer datos: {e}")
                return None
            except UnicodeDecodeError:
                print("Error: No se pudo decodificar los datos recibidos")
                return None
        else:
            print("No hay conexión serial")
            return None

    def close(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Conexión serial cerrada")



class SerialSimulator:
    """simulador de puerto serial por defecto COM3"""
    
    def __init__(self, port='COM3', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.is_open = False
        
    def open(self):
        self.is_open = True
        print(f"Simulador: Puerto {self.port} abierto a {self.baudrate} baudios")
        
    def close(self):
        self.is_open = False
        print(f"Simulador: Puerto {self.port} cerrado")
        
    def send_command(self, data):
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        
    def read(self, size=1):
        return b''
        
    def readline(self):
        return b'OK\n'
        
    @property
    def in_waiting(self):
        """simula datos disponibles en el buffer"""
        return 0


if __name__ == "__main__":
    print("COM3")
    ser = SerialSimulator('COM3', 9600)
    ser.open()
    

    ser.write(b"AT\n")
    
    print("Respuesta:", ser.readline().decode().strip())
    
    ser.close()