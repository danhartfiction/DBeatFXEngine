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
        self.next_beat = 0
        self.didBeat = False
        self.min_observed_volume = 100000
        self.max_observed_volume = -100000
        self.relative_volume = 0
        self.onset_list = [0]

    def fluffEffect(self, isBeat):
        if isBeat:
            print("Fluff BEAT!")

    def softEffect(self, isBeat):
        if isBeat:
            print("soft BEAT!")

    def hardEffect(self, isBeat):
        if isBeat:
            print("Hard BEAT!")

    def crispEffect(self, isBeat):
        if isBeat:
            print("Crisp BEAT!")
  
    def processEffect(self, isBeat, confidence):
        if confidence < 0.05:
            self.fluffEffect(isBeat)
        elif confidence < .1:
            self.softEffect(isBeat)
        elif confidence < .2:
            self.hardEffect(isBeat)
        else:
            self.crispEffect(isBeat)

    def mainLoop(self):
        now = time.time()
        # Basically, if beatProcessor hasn't initialized yet
        if self.beatProcessor.next_beat == 0:
            return 
        bpm = self.beatProcessor.tempo.get_bpm()
        confidence = self.beatProcessor.tempo.get_confidence()
        if now > self.next_beat:
            if self.beatProcessor.next_beat > now:
                self.next_beat = self.beatProcessor.next_beat
            if now - self.beatProcessor.next_beat > 30/bpm: # In this case let's just wait for the next beat
                self.processEffect(False, confidence)
                return
            # Do the beat
            if not self.didBeat:
                self.didBeat = True
                self.beat_num += 1
#                print("BEAT #{}!  BPM: {} Beat Confidence: {}".format(self.beat_num, bpm, self.beatProcessor.tempo.get_confidence()))
                self.processEffect(True, confidence)
                if self.inputProcessor.volume != 0:
                    self.min_observed_volume = self.inputProcessor.volume if self.inputProcessor.volume < self.min_observed_volume else self.min_observed_volume
                    self.max_observed_volume = self.inputProcessor.volume if self.inputProcessor.volume > self.max_observed_volume else self.max_observed_volume
                    if self.max_observed_volume > self.min_observed_volume:
                        self.relative_volume = (self.inputProcessor.volume - self.min_observed_volume) / abs(self.max_observed_volume - self.min_observed_volume)
#                print("Volume: {}  Min:  {}   Max: {}  Relative: {}".format(self.inputProcessor.volume, self.min_observed_volume, self.max_observed_volume, self.relative_volume))
                self.inputProcessor.volume = 0
        else:
            self.didBeat = False
            self.processEffect(False, confidence)
