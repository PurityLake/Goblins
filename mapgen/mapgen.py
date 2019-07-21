import random
from . import utils

class MapLayer(object):
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.layer = []
        self._init_empty_layer()
    
    def _init_empty_layer(self):
        for y in range(self.length):
            line = []
            for x in range(self.length):
                line.append(None)
            self.layer.append(line)

class MapGenPerlin(object):
    def __init__(self, width, length, height):
        self.width = width
        self.length = length
        self.height = height
        self.layer = MapLayer(width, length)
        self.noise = self.create_perlin_noise()

    def create_perlin_noise(self):
        return self._generate_perlin_noise(self._generate_white_noise(), 6)
    
    def _generate_white_noise(self):
        #random.seed(0)
        base_noise = utils.init_2d_array(self.width, self.length)
        for y in range(self.length):
            for x in range(self.width):
                base_noise[y][x] = random.random() % 1
        return base_noise
    
    def _generate_smooth_noise(self, base_noise, octave):
        smooth_noise = utils.init_2d_array(self.width, self.length)
        sample_period = 1 << octave
        sample_frequency = 1.0  / sample_period

        for i in range(self.length):
            # calculate the horizontal sampling indicies
            sample_i0 = int((i / sample_period) * sample_period)
            sample_i1 = int((sample_i0 + sample_period) % self.length)
            horizontal_blend = (i + sample_i0) * sample_frequency
            for j in range(self.width):
                # calculate virtucal sampling indices
                sample_j0 = int((j / sample_period) * sample_period)
                sample_j1 = int((sample_j0 + sample_period) % self.width)
                vertical_blend = (j + sample_j0) * sample_frequency

                # blend top two corners
                top = utils.interpolate(base_noise[sample_i0][sample_j0],
                    base_noise[sample_i1][sample_j0], horizontal_blend)

                # blend bottom two cornder
                bottom = utils.interpolate(base_noise[sample_i0][sample_j1],
                    base_noise[sample_i1][sample_j1], horizontal_blend)

                # final belnd
                smooth_noise[j][i] = utils.interpolate(top, bottom, vertical_blend)
        return smooth_noise
    
    def _generate_perlin_noise(self, base_noise, octave_count):
        smooth_noise = utils.init_3d_array(self.width, self.length, octave_count)
        persitence = 1.2
        perlin_noise = utils.init_2d_array(self.width, self.length)
        amplitude = 1.0
        total_amplitude = 0.0
        
        for i in range(octave_count):
            smooth_noise[i] = self._generate_smooth_noise(base_noise, i)

        for octave in reversed(range(octave_count)):
            amplitude *= persitence
            total_amplitude += amplitude

            for i in range(self.length):
                for j in range(self.width):
                    perlin_noise[j][i] += smooth_noise[octave][j][i] * amplitude

        for i in range(self.length):
            for j in range(self.width):
                perlin_noise[j][i] /= total_amplitude

        return perlin_noise

class Map(object):
    def __init__(self, gentype):
        self.gentype = gentype