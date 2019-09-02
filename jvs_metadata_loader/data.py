from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Tuple, List, Optional


class Gender(str, Enum):
    M = 'M'
    F = 'F'


@dataclass
class MonophoneLabel:
    begin_time: float
    end_time: float
    phoneme: str


@dataclass
class Utterance:
    id: str
    transcript: str
    wave_path: Path
    monophone_labels: Optional[List[MonophoneLabel]]
    full_context_label_path: Optional[Path]


@dataclass
class Corpus:
    path: Path
    utterances: List[Utterance]


@dataclass
class Speaker:
    path: Path
    id: str
    gender: Gender
    f0_range: Tuple[float, float]
    parallel_corpus: Corpus
    nonpara_corpus: Corpus
    whisper_corpus: Corpus
    falset_corpus: Corpus


@dataclass
class JVS:
    path: Path
    speakers: List[Speaker]
