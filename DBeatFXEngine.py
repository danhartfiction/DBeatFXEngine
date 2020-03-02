#!/usr/bin/env python3

import sys
import time

import config
import inputs
import effects
import beats
import outputs

if __name__ == "__main__":
    config = config.Config()
    beatProcessor = beats.aubioBeats(config)
    outputProcessor = outputs.ledStrips(config)
    inputProcessor = inputs.micInput(config, beatProcessor)
    effectProcessor = effects.dranofx(config, beatProcessor, outputProcessor)
    effectProcessor.start()
    effectProcessor.join()

    while True:
        time.sleep(config.mainLoopTick)