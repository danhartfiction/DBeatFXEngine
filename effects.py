import threading
import time
import numpy as np

class effectEngine(object):
    def __init__(self, config, inputProcessor, beatProcessor, outputProcessor):
        self.config = config
        self.inputProcessor = inputProcessor
        self.beatProcessor = beatProcessor
        self.outputProcessor = outputProcessor


class dranofx(effectEngine):
    def __init__(self, config, inputProcessor, beatProcessor, outputProcessor):
        super().__init__(config, inputProcessor, beatProcessor, outputProcessor)
        self.inputProcessor = inputProcessor
        self.beatProcessor = beatProcessor
        self.outputProcessor = outputProcessor
        self.beat_num = 0
        self.last_beat = 0
        self.last_delay = 0
        self.next_beat = 0
        self.errors = 0
        self.bpm_list = [100]
        self.min_observed_volume = 100000
        self.max_observed_volume = -100000
        self.relative_volume = 0
#        self.brightness_values = [25, 33, 50, 66, 75, 100]
#        self.brightness_levels = len(self.brightness_values)
#        self.volume_list = [0]
        self.onset_list = [0]

#    def addVolume(self, v):
#        self.volume_list.append(v)
#        if len(self.volume_list) > 32:
#            self.volume_list = self.volume_list[8:]
#        self.volume_momentum = np.mean(np.diff(self.volume_list))

    def mainLoop(self):
        print("Confidence: {}".format(self.beatProcessor.tempo.get_confidence()))
#        self.addVolume(self.inputProcessor.volume)
        if self.beatProcessor.tempo.get_confidence() > .1:
            now = time.time()
            bpm = self.beatProcessor.tempo.get_bpm()
            if now - self.last_beat < .33*60/bpm:
                print('Too soon')
                time.sleep(.01)
                return
            if now - self.beatProcessor.last_beat > 3*60/bpm:
                print('no beat')
                self.errors = 0
                time.sleep(.5)
                return
            self.beat_num += 1
            if self.inputProcessor.volume != 0:
                self.min_observed_volume = self.inputProcessor.volume if self.inputProcessor.volume < self.min_observed_volume else self.min_observed_volume
                self.max_observed_volume = self.inputProcessor.volume if self.inputProcessor.volume > self.max_observed_volume else self.max_observed_volume
                if self.max_observed_volume > self.min_observed_volume:
                    self.relative_volume = (self.inputProcessor.volume - self.min_observed_volume) / abs(self.max_observed_volume - self.min_observed_volume)
            print("Volume: {}  Min:  {}   Max: {}  Relative: {}".format(self.inputProcessor.volume, self.min_observed_volume, self.max_observed_volume, self.relative_volume))
            self.inputProcessor.volume = 0
            print("BEAT #{}!  BPM: {} Beat Confidence: {}".format(self.beat_num, bpm, self.beatProcessor.tempo.get_confidence()))
            self.last_beat = time.time()
#            self.outputProcessor.toggle()
            next_delta = self.beatProcessor.next_beat - time.time()
            if next_delta > .66*60/bpm:
                time.sleep(next_delta)
            else:
                time.sleep(60/bpm)
        else:
            self.errors = 0
            self.inputProcessor.volume = 0
            time.sleep(1)
