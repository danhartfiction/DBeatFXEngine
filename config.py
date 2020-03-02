

class Config(object):
    def __init__(self):
        self.inputDevice = 0
        self.inputChannels = 1
        self.sampleRate = 44100 
        self.bufferSize = 512
        self.fftSize = 1024

        self.mainLoopTick = 0.01
