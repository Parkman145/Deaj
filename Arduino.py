class Arduino:
    def __init__(self, port, baud_rate):
        self.ser = serial.Serial(port, baud_rate)

    def get_values(self)->list:
        data = [int(x) for x in self.ser.readline().decode("ascii").split("|")]
        return data