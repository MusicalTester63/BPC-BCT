import pickle
import json

class pkt:
    def __init__(self, name, sender, receiver, type, segmentsLeft, segmentList):
        self.__name = name
        self.__sender = sender
        self.__receiver = receiver
        self.__type = type
        self.__segmentsLeft = segmentsLeft
        self.__segmentList = segmentList

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_sender(self):
        return self.__sender

    def set_sender(self, sender):
        self.__sender = sender

    def get_receiver(self):
        return self.__receiver

    def set_receiver(self, receiver):
        self.__receiver = receiver

    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

    def get_segmentsLeft(self):
        return self.__segmentsLeft

    def set_segmentsLeft(self, segmentsLeft):
        self.__segmentsLeft = segmentsLeft

    def get_segmentList(self):
        return self.__segmentList

    def set_segmentList(self, segmentList):
        self.__segmentList = segmentList