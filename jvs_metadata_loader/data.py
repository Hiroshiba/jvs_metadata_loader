from enum import Enum
from pathlib import Path
from typing import Tuple, List, Optional, NamedTuple


class Gender(str, Enum):
    M = 'M'
    F = 'F'


class MonophoneLabel(NamedTuple):
    begin_time: float
    end_time: float
    phoneme: str


class Utterance(NamedTuple):
    id: str
    transcript: str
    wave_path: Path
    monophone_labels: Optional[List[MonophoneLabel]]
    monophone_label_path: Optional[Path]
    full_context_label_path: Optional[Path]

    def __hash__(self):
        return hash(self.id)


class Corpus(NamedTuple):
    path: Path
    utterances: List[Utterance]


class Speaker(NamedTuple):
    path: Path
    id: str
    gender: Gender
    f0_range: Tuple[float, float]
    parallel_corpus: Corpus
    nonpara_corpus: Corpus
    whisper_corpus: Corpus
    falset_corpus: Corpus

    def __hash__(self):
        return hash(self.id)


class JVS(NamedTuple):
    path: Path
    speakers: List[Speaker]
