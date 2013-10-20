import threading
import tkinter
try:
    import wave
    import pyaudio

except:
    print("Pyaudio missing. It is a simple install--please install.")





class Audio(object):
    def __init__(self,app):
        self.app = app
        if self.app.musicEnabled:
            self.bgMusic = './res/audio/overworld.wav'

            self.bgStream = AudioFile(self.bgMusic)
            self.app.getRoot().after(20,self.checkForMusic)

    def checkForMusic(self):
        if self.app.musicEnabled:
            if not self.bgStream.isPlaying:
                self.bgStream.play()





class AudioFile(object):
    """Audio File

    Plays a WAVE file using PyAudio v0.2.7.

    Credits: This class is a wrapped version of the basic pyaudio demo script included with the library.

    """

    CHUNK = 1024

    def __init__(self, file):
        try:
            self.isPlaying = False
            self.wf = wave.open(file, 'rb')
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format = self.p.get_format_from_width(self.wf.getsampwidth()),
                                      channels = self.wf.getnchannels(),
                                      rate = self.wf.getframerate(),
                                      output = True)
        except:
            print("Error initializing AudioFile.")

        if not self.isPlaying:
            self.isPlaying = True
            threading.Timer(0.1, self.play).start()



    def play(self):

        try:
            data = self.wf.readframes(self.CHUNK)
            while data != '':
                self.stream.write(data)
                data = self.wf.readframes(self.CHUNK)
        except:
            print("Error playing AudioFile.")


    def close(self):
        #pass

        try:
            self.stream.close()
            self.p.terminate()
        except:
            print("Error closing AudioFile.")
