import threading
import time

class effectEngine(threading.Thread):
    def __init__(self, config, beatProcessor, outputProcessor):
        self.config = config
        self.beatProcessor = beatProcessor
        self.outputProcessor = outputProcessor
        threading.Thread.__init__(self)


class dranofx(effectEngine):
    def __init__(self, config, beatProcessor, outputProcessor):
        super().__init__(config, beatProcessor, outputProcessor)
        self.beatProcessor = beatProcessor
        self.outputProcessor = outputProcessor
        self.beat_num = 0
        self.last_beat = 0
        self.last_delay = 0
        self.next_beat = 0
        self.errors = 0

    def run(self):
        while True:
            print("Confidence: {}".format(self.beatProcessor.tempo.get_confidence()))
            if self.beatProcessor.tempo.get_confidence() > .1:
                now = time.time()
                bpm = self.beatProcessor.tempo.get_bpm()
                if now - self.last_beat < .33*60/bpm:
                    print('Too soon')
                    time.sleep(.01)
                    continue
                if now - self.beatProcessor.last_beat > 3*60/bpm:
                    print('no beat')
                    self.errors = 0
                    time.sleep(.5)
                    continue
                self.beat_num += 1
                print("BEAT #{}!  BPM: {} Beat Volume: {} Beat Confidence: {}".format(self.beat_num, bpm, self.beatProcessor.volume, self.beatProcessor.tempo.get_confidence()))
                self.beatProcessor.volume = 0
                self.last_beat = time.time()
#                self.outputProcessor.toggle()
                next_delta = self.beatProcessor.next_beat - time.time()
                if next_delta > .66*60/bpm:
                    time.sleep(next_delta)
                else:
                    time.sleep(60/bpm)
            else:
                self.errors = 0
                time.sleep(1)
