from pprint import pprint
from typing import Final, Any


class logger:
    reset: Final[str] = "\x1b[0m"
    blue: Final[str] = "\x1b[96m"
    yellow: Final[str] = "\x1b[93m"

    @classmethod
    def info(cls, data: Any, flag: str = ""):
        res = "{color}{level}{reset}{color_flag}[{flag}]{reset}:".format(level="[INFO]",
                                                                         color=cls.blue,
                                                                         reset=cls.reset,
                                                                         flag=flag,
                                                                         color_flag=cls.yellow)
        print(res, end="")
        pprint(data)


