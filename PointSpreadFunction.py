import csv
import numpy
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


class CSVFile:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def read(self):
        with open('%s.csv' % self.name) as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                yield row

    def getData(self):
        for row in self.read():
            numberOfBeads = len(row)

        for bead in range(numberOfBeads):
            xdata = []
            ydata = []

            if self.type == 'raw':
                for row in self.read():
                    point = row[bead].split(',')
                    try:
                        float(point[0])
                    except ValueError:
                        pass
                    else:
                        xdata.append(float(point[0]))
                        ydata.append(float(point[1]))
            elif self.type == 'organised':
                numberOfBeads -= 1
                for row in self.read():
                    try:
                        float(row[0])
                    except ValueError:
                        pass
                    else:
                        xdata.append(float(row[0]))
                        ydata.append(float(row[bead]))
            else:
                print("Type is not recognized")
                break

            yield xdata, ydata


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
        return plt.plot(self.xdata, self.ydata, '.', markersize=16)

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
        inputFileType = input("Is your data raw or organised? (raw / organised) --> ").replace(" ", "")
        chosenFile = CSVFile('%s' % inputFileName, '%s' % inputFileType)

        data = chosenFile.getData()
        showPlot = input("Would you like to show plot? (yes / no) --> ").replace(" ", "")
        for dataSet in data:
            zData = dataSet[0]
            iData = dataSet[1]
            bead = GaussianDistribution(zData, iData)
            c = bead.getFWHM(show=True)
            if showPlot == 'yes':
                bead.plotData()
                bead.plotCurvefit()
                plt.title('FWHM = %s' % c)
                plt.show()
            else:
                pass

