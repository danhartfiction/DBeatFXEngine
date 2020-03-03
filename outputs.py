import sacn
import numpy as np

class outputEngine(object):
    def __init__(self, config):
        self.config = config
        self.outputs = []


class ledStrip(object):

    def __init__(self, name, ip, num_pixels, universe):
        self.name = name
        self.ip = ip
        self.num_pixels = num_pixels
        self.universe = universe
        self.pixels = np.zeros(shape=(num_pixels, 3))
        self.cpink = np.zeros(shape=(num_pixels, 3))
        self.cblue = np.zeros(shape=(num_pixels, 3))
        for i in range(num_pixels):
            self.cpink[i] = [255, 0, 255]
            self.cblue[i] = [0, 255, 255]


class ledStrips(outputEngine):
    def __init__(self, config):
        super().__init__(config) 
        self.outputs.append(ledStrip('flag', '10.10.10.71', 50, 2))
        self.outputs.append(ledStrip('shelves', '10.10.10.72', 46, 3))
        self.outputs.append(ledStrip('backwall', '10.10.10.73', 50, 4))

        self.sacn = sacn.sACNsender()
        self.sacn.start()
        self.pink = True
        self.sacn.manual_flush = True
        for ls in self.outputs:
            print("Activating led strip named {}".format(ls.name))
            self.sacn.activate_output(ls.universe)
            self.sacn[ls.universe].destination = ls.ip

    def update(self):
        for ls in self.outputs:
            data = ls.pixels.flatten()
            self.sacn[ls.universe].dmx_data = data.astype(int).clip(0,255)
        self.flush()

    def flush(self):
        self.sacn.flush()
