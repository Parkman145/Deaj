"""
Per session GetMute() SetMute() GetMasterVolume() SetMasterVolume() using
SimpleAudioVolume.
"""

import yaml
from Arduino import Arduino
from AudioController import AudioController






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
