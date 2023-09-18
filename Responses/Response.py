class JSONResponse:
    def __init__(self, code=200, message=None, data=None):
        if data is None:
            data = {}
        self._code = code
        self._message = message
        self._data = data

    def build(self):
        return self.to_dict(), self.code

    def build_data_by_records(self, records):
        self.append_data("records", [record.to_dict() for record in records])
        if hasattr(records, 'page'):
            self.append_data("page", records.page)
            self.append_data("total", records.total)
        else:
            self.append_data("page", 1)
            self.append_data("total", len(records))

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def append_data(self, key, value):
        self._data[key] = value

    def to_dict(self):
        return {
            "code": self._code,
            "message": self._message,
            "data": self._data
        }
