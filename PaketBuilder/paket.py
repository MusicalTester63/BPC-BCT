class paket:
    def __init__(self, meno, odosielatel, prijemca, typ, segmentsLeft, segmentList):
        self._meno = meno
        self._odosielatel = odosielatel
        self._prijemca = prijemca
        self._typ = typ
        self._segmentsLeft = segmentsLeft
        self._segmentList = segmentList

    def get_meno(self):
        return self._meno

    def get_od(self):
        return self._odosielatel

    def get_pr(self):
        return self._prijemca

    def get_typ(self):
        return self._typ

    def get_segmentsLeft(self):
        return self._segmentsLeft

    def get_segmentList(self):
        return self._segmentList
