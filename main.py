"""
Per session GetMute() SetMute() GetMasterVolume() SetMasterVolume() using
SimpleAudioVolume.
"""

from pycaw.pycaw import AudioUtilities
import time
import yaml
import serial

class AudioController:
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = self.process_volume()

    def set_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                print("Volume set to", self.volume)  # debug


def main():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    audio_controller = AudioController("Spotify.exe")

    port = config["port"]
    mapping = config["slider_mapping"]
    max_slider_value = config["max_slider_value"]
    baud_rate = config["baud_rate"]

    with serial.Serial(port, baud_rate) as ser:
        while(True):
            data = ser.readline().decode("ascii")
            audio_controller.set_volume((int(data) / max_slider_value)**4)
            print(data)
            


if __name__ == "__main__":
    main()
