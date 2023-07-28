
class StreamProperty(str):
    _SUBJECTS_ = []
    _DESCRIPTION_ = ""

    def __new__(cls, name: str, subjects: list, desc: str = ""):
        instance = super().__new__(cls, name)
        instance._SUBJECTS_ = subjects
        instance._DESCRIPTION_ = desc
        return instance

    def subject(self):
        return self._SUBJECTS_

    def desc(self):
        return self._DESCRIPTION_
