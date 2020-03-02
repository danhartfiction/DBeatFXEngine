import aubio
import time
import numpy as np

class beatEngine(object):
    def __init__(self, config):
        self.config = config

class aubioBeats(beatEngine):
    def __init__(self, config):
        super().__init__(config)
        self.epoch = time.time()
        self.volume = 0
        self.tempo = aubio.tempo("default", self.config.fftSize, self.config.bufferSize, self.config.sampleRate)
    
    def processBeat(self, in_data):
        aubio_audio_sample = np.frombuffer(in_data, dtype=aubio.float_type)
        self.volume += np.sum(aubio_audio_sample**2)/len(aubio_audio_sample)
        if self.tempo(aubio_audio_sample):
            self.last_beat = self.epoch + self.tempo.get_last_s()
            self.next_beat = self.last_beat + 60/self.tempo.get_bpm() 
        return aubio_audio_sample
