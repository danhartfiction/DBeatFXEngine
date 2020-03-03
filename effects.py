import threading
import time
import random
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
#        self.min_observed_volume = 100000
#        self.max_observed_volume = -100000
        self.relative_volume = 0
        self.lastSparkleChange = 0
        self.lastFadeChange = 0
        self.lastFadeColorChange = 0
        self.fadeIntensity = 0
        self.fadeDirection = True
        self.fadeHalf = False
        self.fade_offset = 0
        self.fade_i = 0
        self.hardFactor = 0
        self.crisp_mode = 0

    def fluffEffect(self, isBeat):
        # Soft sparkle effect
        now = time.time()
        if now - self.lastSparkleChange > .2:
            self.lastSparkleChange = now
            for output in self.outputProcessor.outputs:
                for pixel in range(output.num_pixels):
                    if random.random() > .9:
                        if random.random() > .5:
                            output.pixels[pixel] = [0, 255, 255]
                        else:
                            output.pixels[pixel] = [255, 0, 255]
        else:
            for output in self.outputProcessor.outputs:
                for pixel in range(output.num_pixels):
                    for i in range(3):
                       output.pixels[pixel][i] = output.pixels[pixel][i] - 8 if output.pixels[pixel][i] > 8 else 0

    def softEffect(self, isBeat):
        # Fade in / fade out with BPM
        now = time.time()
        bpm = self.beatProcessor.tempo.get_bpm()
#        print("fadeIntensity: {} BPM: {} Volume: {}".format(self.fadeIntensity, bpm, self.relative_volume))
        if isBeat:
            if self.fadeHalf:
                self.fadeDirection = False if self.fadeDirection else True
            self.fadeHalf = False if self.fadeHalf else True
        if now - self.lastFadeChange > 12/bpm:
            self.lastFadeChange = now
            if self.fadeDirection:
                self.fadeIntensity += 0.2 if self.fadeIntensity <= 0.9 else 0
            else:
                self.fadeIntensity -= 0.2 if self.fadeIntensity >= 0.1 else 0
            if now - self.lastFadeColorChange > 240/bpm and self.fadeIntensity < 0.2: # 60*4
                self.lastFadeColorChange = now
                self.fade_offset = 1 if self.fade_offset == 0 else 0
            v = round(self.fadeIntensity * 255, 4)
            self.fade_i = 1 if self.fade_i == 0 else 0
            self.fade_i += self.fade_offset
            for output in self.outputProcessor.outputs:
                for pixel in range(output.num_pixels):
                    if self.fade_i % 2:
                        output.pixels[pixel] = [0, v, v]
                    else:
                        output.pixels[pixel] = [v, 0, v]
                self.fade_i+=1

    def hardEffect(self, isBeat):
        now = time.time()
        bpm = self.beatProcessor.tempo.get_bpm()
        if isBeat:
            self.crisp_mode = 0 if self.crisp_mode == 1 else 1
            self.hardFactor = 1
        else:
            self.hardFactor -= .1 if self.hardFactor >= .1 else 0
        v = round(self.hardFactor * 255, 4)
        i = self.crisp_mode
        for output in self.outputProcessor.outputs:
            for pixel in range(output.num_pixels):
                if i % 2:
                    output.pixels[pixel] = [0, v, v]
                else:
                    output.pixels[pixel] = [v, 0, v]
            i+=1 

    def crispEffect(self, isBeat):
        if isBeat:
            self.crisp_mode = 0 if self.crisp_mode == 1 else 1
#        v = round(self.relative_volume * 255, 4)
        v = 255
        i = self.crisp_mode
        for output in self.outputProcessor.outputs:
            for pixel in range(output.num_pixels):
                if i % 2:
                    output.pixels[pixel] = [0, v, v]
                else:
                    output.pixels[pixel] = [v, 0, v]
            i+=1
        
  
    def processEffect(self, isBeat, confidence):
        if confidence < 0.05:
            self.fluffEffect(isBeat)
        elif confidence < .13:
            self.softEffect(isBeat)
        elif confidence < .21:
            self.hardEffect(isBeat)
        else:
            self.crispEffect(isBeat)
        self.outputProcessor.update()

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
#                if self.inputProcessor.volume != 0:
#                    self.min_observed_volume = self.inputProcessor.volume if self.inputProcessor.volume < self.min_observed_volume else self.min_observed_volume
#                    self.max_observed_volume = self.inputProcessor.volume if self.inputProcessor.volume > self.max_observed_volume else self.max_observed_volume
#                    if self.max_observed_volume > self.min_observed_volume:
#                        self.relative_volume = (self.inputProcessor.volume - self.min_observed_volume) / abs(self.max_observed_volume - self.min_observed_volume)
#                print("Volume: {}  Min:  {}   Max: {}  Relative: {}".format(self.inputProcessor.volume, self.min_observed_volume, self.max_observed_volume, self.relative_volume))
                self.inputProcessor.volume = 0
        else:
            self.didBeat = False
            self.processEffect(False, confidence)
