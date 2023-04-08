import serial

# Configure UART port
ser = serial.Serial(
    port='Com5',# Change this to the port number of your UART device
    baudrate=9600,      # Change this to your desired baudrate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# Send data via UART
data = bytearray(b"Hello World\r\n") # Change this to the data you want to send
ser.write(data)