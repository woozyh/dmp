#!/usr/bin/python3.11.8

from collections.abc import Generator

class Reader(object):
    
    def __init__(self, file_path: str) -> None:
        self.file  = open(file_path)
        
    def read(self):
        self.line  = (line.strip() for line in self.file.readlines())
        self.file.close()
        return self.line
