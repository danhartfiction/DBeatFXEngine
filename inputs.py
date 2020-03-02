import pyaudio
import aubio
import sys
import numpy as np

class inputDevice(object):
    def __init__(self, config, beatProcessor):
        self.config = config
        self.beatProcessor = beatProcessor

class micInput(inputDevice):
    def __init__(self, config, beatProcessor):
        super().__init__(config, beatProcessor)
        self.audio = pyaudio.PyAudio()
        self.volume = 0
        self.openInput()

    def openInput(self):
        try:
            self.inputStream = self.audio.open(
                input_device_index=self.config.inputDevice,
                format=pyaudio.paFloat32,
                channels=self.config.inputChannels,
                rate=self.config.sampleRate,
                input=True,
                frames_per_buffer = self.config.bufferSize,
                stream_callback = self.audio_sample_callback)
            self.inputStream.start_stream()
            print("Audio source opened.") 
        except Exception as e:
            print("An error occured: {}".format(e))
            print("Here are your available audio Input Devices:")
            # Enumerate all of the input devices and find the one matching the
            info = self.audio.get_host_api_info_by_index(0)
            for i in range(0, info.get('deviceCount')):
                if (self.audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    print("  [{}] {}".format(i, self.audio.get_device_info_by_host_api_device_index(0, i).get('name')))
            sys.exit(1)

    def audio_sample_callback(self, in_data, frame_count, time_info, status):
        sample = self.beatProcessor.processBeat(in_data) 
        self.volume += aubio.db_spl(sample)
        return (sample, pyaudio.paContinue)

