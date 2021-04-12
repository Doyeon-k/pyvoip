

from audio_out import AudioOutput
from mic import MicDevice
from rtp_client import RTPReceiveClient, RTPSendClient
import pyaudio
import numpy as np

class Client:
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 4096

    def __init__(
            self,
            remote_host_address,
            remote_host_port,
            rtp_port):


        self.mic = MicDevice(sr=self.SAMPLE_RATE,
                             chunk_size=self.CHUNK_SIZE)

        self.sender = RTPSendClient(remote_host_address=remote_host_address,
                                    remote_host_port=remote_host_port)

        self.receiver = RTPReceiveClient(rtp_port=rtp_port)
        self.aout = AudioOutput()
        self.frame_count = 0
        print('init client')

    def _callback(self, in_data, frame_count, time_info, status):
        print(in_data)
        print(len(in_data), frame_count, time_info, status)

        timestamp = int(frame_count / self.SAMPLE_RATE * 1000)

        self.sender.send_audio(
            data=in_data,
            ts=timestamp,
            frame_count=self.frame_count)

        self.frame_count += 1
        return (None, pyaudio.paContinue)

    def _receive_callback(self, audio):
        print('audio received!')
        self.aout.write(audio)

    def start_calling(self):
        self.sender.start()
        self.receiver.start(self._receive_callback)
        # mic
        self.mic.start(self._callback)
        # audio output
        self.aout.open()
        self.aout.start()

        print('start calling ...')

    def stop_calling(self):
        # TODO
        print('stop calling')
