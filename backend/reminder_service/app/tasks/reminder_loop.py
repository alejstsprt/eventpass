import warnings


class _BDBaseDict:

    def pri(self):
        print("el")


class BaseDict(dict, _BDBaseDict):
    __basedict = None

    def __new__(cls):
        if cls.__basedict is None:
            cls.__basedict = super().__new__(cls)
            cls.__basedict.update({"1": 250})
        return cls.__basedict

    def __add__(self, obj):
        self.pri()
        warnings.warn(
            "По возможности используйте способ '+=' для добавления, иначе получите рассинхрон."
        )
        self.update(obj)
        return self

    def __iadd__(self, obj: dict):
        self.update(obj)
        return self

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        return super().__delitem__(key)

    def __delattr__(self, name):
        warnings.warn(
            "Удаление базы данных данным способом невозможно в целях безопасности"
        )
        return None

    def __repr__(self):
        result = {}
        for key, value in self.items():
            if isinstance(value, str):
                result.setdefault(key, "qqqqqqqqqqqqqq")
            else:
                result.setdefault(key, value)

        return f"{result}"
