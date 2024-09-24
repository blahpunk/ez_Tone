from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QDial, QComboBox, QLabel, QWidget
from waveform import WaveOscillator
from audio_handler import play_tone, stop_playback, toggle_loop, set_current_note, set_frequency, set_amplitude
from frequencies import note_frequencies
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ez_Tone')
        self.setGeometry(300, 300, 600, 300)
        self.setStyleSheet("background-color: cyan;")

        self.oscillator = WaveOscillator(self)
        self.oscillator.setStyleSheet("background-color: turquoise;")

        self.playButton = QPushButton('Play', self)
        self.loopButton = QPushButton('Loop', self)
        self.loopButton.setCheckable(True)
        self.stopButton = QPushButton('Stop', self)

        self.toneSelect = QComboBox(self)
        self.toneSelect.addItems(list(note_frequencies.keys()))
        self.toneSelect.setCurrentText('A')

        self.amplitudeDial = QDial(self)
        self.amplitudeDial.setMinimum(0)
        self.amplitudeDial.setMaximum(100)
        self.amplitudeDial.setValue(50)

        self.frequencyDial = QDial(self)
        self.frequencyDial.setMinimum(20)
        self.frequencyDial.setMaximum(20000)
        self.frequencyDial.setValue(int(note_frequencies['A']))

        layout = QVBoxLayout()
        layout.addWidget(self.oscillator)
        layout.addWidget(self.playButton)
        layout.addWidget(self.loopButton)
        layout.addWidget(self.stopButton)
        layout.addWidget(self.toneSelect)
        layout.addWidget(QLabel('Frequency (Hz)'))
        layout.addWidget(self.frequencyDial)
        layout.addWidget(QLabel('Amplitude (0-1)'))
        layout.addWidget(self.amplitudeDial)

        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.playButton.clicked.connect(self.handlePlay)
        self.loopButton.clicked.connect(lambda: toggle_loop(self.loopButton.isChecked()))
        self.stopButton.clicked.connect(self.handleStop)
        self.toneSelect.currentIndexChanged.connect(self.updateNote)
        self.frequencyDial.valueChanged.connect(self.updateFrequency)
        self.amplitudeDial.valueChanged.connect(self.updateAmplitude)

    def handlePlay(self):
        play_tone()

    def handleStop(self):
        stop_playback()

    def updateNote(self):
        note = self.toneSelect.currentText()
        set_current_note(note)
        self.frequencyDial.setValue(int(note_frequencies[note]))  # Ensure the dial is updated

    def updateFrequency(self):
        freq = self.frequencyDial.value()
        set_frequency(freq)

    def updateAmplitude(self):
        amp = self.amplitudeDial.value() / 100.0
        set_amplitude(amp)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
