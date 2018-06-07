import csv
import numpy
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


class CSVFile:

    def __init__(self, name):
        self.name = name

    def read(self):
        with open('%s.csv' % self.name) as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                yield row

    def getZdata(self):
        z = []
        for row in self.read():
            data = row[0]
            try:
                float(data)
            except ValueError:
                pass
            else:
                z.append(float(data))
        return z

    def getIntensityData(self):
        for row in self.read():
            numberOfBeads = len(row) - 1

        for bead in range(numberOfBeads):
            line = []
            for row in self.read():
                try:
                    float(row[0])
                except ValueError:
                    pass
                else:
                    toAdd = float(row[bead + 1])
                    line.append(toAdd)
            yield line


class GaussianDistribution:

    def __init__(self, xdata, ydata):
        self.xdata = xdata
        self.ydata = ydata

    def __str__(self):
        return "class 'gaussianDistribution' with: " \
               "\n\txdata = %s" \
               "\n\tydata = %s" % (self.xdata, self.ydata)

    @staticmethod
    def func(x, a, b, c):
        return a * numpy.exp(-(x - b)**2 / (2 * c**2))

    def getpopt(self):
        popt, pcov = curve_fit(GaussianDistribution.func, self.xdata, self.ydata)
        return popt

    def getFWHM(self, show=False):
        fwhm = abs(2 * (2 * numpy.log(2))**0.5 * self.getpopt()[2])
        print('FWHM = %s' % fwhm) if show else None
        return fwhm

    def plotData(self):
        return plt.plot(self.xdata, self.ydata)


    def plotCurvefit(self):
        xMin = min(self.xdata)
        xMax = max(self.xdata)
        x = numpy.linspace(xMin, xMax, 100)
        return plt.plot(x, GaussianDistribution.func(x, *self.getpopt()))


if __name__ == '__main__':

    inputFileName = input("Enter file name (format .csv). Do not put extension. --> ")
    try:
        open('%s' % inputFileName + '.csv')
    except FileNotFoundError:
        print("\nFile not found. Make sure file :"
              "\n- is in the same folder as python script"
              "\n- is correctly spelled"
              "\n- is of format .csv")
    else:
        chosenFile = CSVFile('%s' % inputFileName)

        zData = chosenFile.getZdata()
        allIntensityData = chosenFile.getIntensityData()
        showPlot = input("Would you like to show plot? (yes or no) ").replace(" ", "")
        for iData in allIntensityData:
            bead = GaussianDistribution(zData, iData)
            c = bead.getFWHM(show=True)
            if showPlot == 'yes':
                bead.plotData()
                bead.plotCurvefit()
                plt.show()
            else:
                pass
