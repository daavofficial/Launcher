import os
import datetime as dt
from enum import Enum

import helpers.config as config

class Logger:
    class Level(Enum):
        NONE = -1
        DEBUG = 0
        INFO = 1
        WARN = 2
        ERROR = 3
        CRITICAL = 4

        def __lt__(self, other):
            return self.value < other.value

        def __le__(self, other):
            return self.value <= other.value

        def __gt__(self, other):
            return self.value > other.value

        def __ge__(self, other):
            return self.value >= other.value

    # __init__ was modified to use config.LOG_CONF - not portable
    def __init__(self, name: str, file: str):
        self.Name = name
        self.File = file
        self.level: self.Level = self.GetLevel(config.LOG_CONF['level'])
        
        self.WriteToConsole = config.LOG_CONF['print']
        self.WriteToFile = config.LOG_CONF['write']

    def __log(self, level: Level, message: str):
        if level < self.level:
            return

        datetime = dt.datetime.now()
        msg = datetime.strftime("%Y-%m-%d %H:%M:%S ")
        msg += f"<{self.Name}> {level.name}: {message}"

        if self.WriteToConsole:
            print(msg)

        if self.WriteToFile:
            with open(f"{config.PATH_ROOT}/logs/{self.File}", "a") as f:
                f.write(msg + "\n")

    def debug(self, message: str):
        self.__log(self.Level.DEBUG, message)

    def info(self, message: str):
        self.__log(self.Level.INFO, message)

    def warn(self, message: str):
        self.__log(self.Level.WARN, message)

    def error(self, message: str):
        self.__log(self.Level.ERROR, message)

    def critical(self, message: str):
        self.__log(self.Level.CRITICAL, message)

    def SetLevel(self, level):
        self.level = self.GetLevel(level)

    def GetLevel(self, level):
        if isinstance(level, self.Level):
            return level
        elif type(level) == str:
            level = level.lower()
            if "debug" in level:
                return self.Level.DEBUG
            elif "info" in level:
                return self.Level.INFO
            elif "warn" in level:
                return self.Level.WARN
            elif "error" in level:
                return self.Level.ERROR
            elif "critical" in level:
                return self.Level.CRITICAL
            elif "none" in level:
                return self.Level.NONE
            else:
                raise Exception("Unknown level string provided")
        else:
            raise Exception("Unknown level type provided")