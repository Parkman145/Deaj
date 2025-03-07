import serial

class Arduino:
    def __init__(self, port, baud_rate):
        self.ser = serial.Serial(port, baud_rate)

    def get_values(self)->list:
        self.ser.reset_output_buffer()
        sucess = False
        while not sucess:
            try:
                data = [int(x) for x in self.ser.read_until().decode("ascii").split("|")]
                sucess = True
            except ValueError:
                pass

        return data
    
    def reset_output_buffer(self):
        self.ser.reset_output_buffer()