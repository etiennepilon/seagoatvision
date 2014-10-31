
import numpy as np
from PIL import Image
import struct
from PIL import ImageDraw


class SonarImage():

    def __init__(self):

        #This is the width of the sonar's beam.
        self.beamAperture = 5.0
        self.threshold = 40
        #used as a divider (3 == divided by 8)
        self.bitShift = 3
        #The image that will be passed to the filter chain
        self.sonarImage = None
        #The image workspace where new acquisitions will be made
        self.imageCenter_x_y = None
        self.stepAngleSize = None
        self.numberOfBins = None
        self.angleMin = None
        self.angleMax = None


        self.newImageFlag = False

    #array : https://docs.python.org/2/library/array.html
    #def drawArcFromRange(self, range):

    def initialize_Parameters(self, sonarScanline_msg):
        dummy = None
        dummy, self.angleMin, self.angleMax, self.stepAngleSize, self.numberOfBins, dummy = \
            struct.unpack('BfffIf', sonarScanline_msg)
        self.sonarImage = Image.new('1', (2*self.numberOfBins, self.numberOfBins), 1)
      #  self.workspaceImage = Image.new('1', (2*self.numberOfBins, self.numberOfBins), 1)
        self.imageCenter_x_y = (self.numberOfBins, self.numberOfBins)
       # self.arcPainter = ImageDraw.Draw(self.workspaceImage)




    def drawArcWithRange(self, scanline_data, angle):
        data = list(bytearray[scanline_data])
        workspaceImage = Image.new('1', (2*self.numberOfBins, self.numberOfBins), 1)
        arcPainter = ImageDraw.Draw(workspaceImage)
        for i in range(len(data)):
            if data[i] > self.threshold:
                box = (self.imageCenter_x_y[0] - i, self.imageCenter_x_y[1] - i,
                       self.imageCenter_x_y[0] + i, self.imageCenter_x_y[1] + i)
                arcPainter.arc(box, angle-self.beamAperture, angle+self.beamAperture, data[i] >> self.bitShift)


        self.sonarImage = np.add(self.sonarImage, workspaceImage)

        if angle == self.angleMax or angle == self.angleMin:
            #Reset mechanism
            image = self.sonarImage
            self.sonarImage = Image.new('1', (2*self.numberOfBins, self.numberOfBins), 1)
            return image

        return
