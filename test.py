from pymodbus.client import ModbusTcpClient
import time

# Modbus parameters
host = "192.168.1.215"  # IP address of the ADAM-6060 device
port = 502               # Modbus TCP port (default is 502)
relay_address = 16       # Modbus register address for relay (adjust this as per documentation)
unit_id = 1              # Modbus unit ID (usually 1 for ADAM-6060)

# Create a Modbus client and connect
client = ModbusTcpClient(host=host, port=port)
connection = client.connect()

if connection:
    print("Connection successful!")
    rr = client.read_coils(relay_address)
    print('Coil initial state:', rr)

    # Open relay (Set register value to 1)
    print("Opening relay...")
    client.write_coil(relay_address, True)
    rr = client.read_coils(relay_address)
    print('Coil after opening:', rr)

    time.sleep(5)  # Keep the relay open for 5 seconds

    # Close relay (Set register value to 0)
    print("Closing relay...")
    client.write_coil(relay_address, False)
    rr = client.read_coils(relay_address)
    print('Coil after closing:', rr)


    # Close the connection
    client.close()
else:
    print("Connection failed.")