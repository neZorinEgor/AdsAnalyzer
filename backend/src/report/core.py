from abc import ABC, abstractmethod
from io import BytesIO

from docx import Document
from enum import StrEnum


class ReportType(StrEnum):
    BASE = "base"
    FOO = "bar"


class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, image: BytesIO) -> Document:
        raise NotImplementedError()
