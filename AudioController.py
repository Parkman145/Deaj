from pycaw.pycaw import AudioUtilities


class NoiseSuppressor:
    def __init__(self, threshold):
        self._last = 0
        self._threshold = threshold

    def get(self, x):
        if abs(x-self._last) > self._threshold:
            # Use new value
            self._last = x
            return x, True
        else:
            # Use old Value
            return self._last, False
        
    def set_threshold(self, threshold):
        self._threshold = threshold

class AudioController:
    def __init__(self, process_name, suppression_threshold = 0.01):
        self.process_name = process_name
        self.volume = self.process_volume()
        self.suppressor = NoiseSuppressor(suppression_threshold)

    def process_volume(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # print("Volume:", interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()

    def set_volume(self, decibels):
        volume, update_volume = self.suppressor.get(decibels)
        if update_volume:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                interface = session.SimpleAudioVolume
                if session.Process and session.Process.name() == self.process_name:
                    # only set volume in the range 0.0 to 1.0
                    self.volume = min(1.0, max(0.0, decibels))
                    interface.SetMasterVolume(self.volume, None)
                    # print("Volume set to", self.volume)  # debug