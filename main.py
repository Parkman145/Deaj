"""
Per session GetMute() SetMute() GetMasterVolume() SetMasterVolume() using
SimpleAudioVolume.
"""

from pycaw.pycaw import AudioUtilities
import yaml
from Arduino import Arduino



class AudioController:
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = self.process_volume()

    def process_volume(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # print("Volume:", interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()

    def set_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                # print("Volume set to", self.volume)  # debug


def main():
    # Open and load config
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    port = config["port"]
    max_slider_value = config["max_slider_value"]
    baud_rate = config["baud_rate"]
    arudino = Arduino(port, baud_rate)

    # Setup audio controllers
    audio_controllers = []
    for process_name in config["slider_mapping"].values():
        audio_controllers.append(AudioController(process_name))

    
    while(True):
        slider_values = arudino.get_values()
        # print(data)
        for slider_value, audio_controller in zip(slider_values, audio_controllers):
            # print(audio_controller.process_name)
            audio_controller.set_volume((slider_value / max_slider_value)**4)
                        
            

# If main, run main
if __name__ == "__main__":
    main()
