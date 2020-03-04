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
    effectProcessor = effects.dranofx(config, inputProcessor, beatProcessor, outputProcessor)

    while True:
        effectProcessor.mainLoop()
        time.sleep(0.05)
