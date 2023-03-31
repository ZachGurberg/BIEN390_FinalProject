import sys
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QValueAxis
from PyQt5.QtGui import QPainter
from PostProcessing import GetData

class HistogramWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle('Histogram')
        self.setGeometry(100, 100, 800, 600)
        self.data = data
        self.create_histogram()

    def create_histogram(self):
        # Calculate histogram data using NumPy
        hist, bin_edges = np.histogram(self.data, bins=10)

        # Create QBarSet for each bin in the histogram
        barsets = []
        for i, val in enumerate(hist):
            barset = QBarSet(f'{bin_edges[i]:.2f} - {bin_edges[i+1]:.2f}')
            barset.append(val)
            barsets.append(barset)

        # Create QBarSeries and add QBarSets to it
        series = QBarSeries()
        for barset in barsets:
            series.append(barset)

        # Create QChart and add QBarSeries to it
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Histogram')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # Set axis labels
        axis_x = QValueAxis()
        axis_x.setTitleText('Volume')
        axis_x.setRange(min(self.data), max(self.data))
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        axis_y = QValueAxis()
        axis_y.setTitleText('Frequency')
        axis_y.setRange(0, max(hist))
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        # Create QChartView to display chart
        chart_view = QChartView(chart, self)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(chart_view)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Get data from external script
    data = GetData()
    for i in range(len(data)):
        data[i] = data[i][0] * data[i][1]
    
        
    print(data)

    window = HistogramWindow(data)
    window.show()
    sys.exit(app.exec_())