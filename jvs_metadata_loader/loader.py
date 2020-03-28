from pathlib import Path
from typing import List, Tuple

from jvs_metadata_loader.data import MonophoneLabel, Gender, JVS, Speaker, Corpus, Utterance

_filename_gender_f0range = 'gender_f0range.txt'
_filename_transcripts = 'transcripts_utf8.txt'
_dirname_wave = 'wav24kHz16bit'
_dirname_label = 'lab'
_dirname_monophone_label = 'mon'
_dirname_full_context_label = 'ful'


def load_monophone_label(path: Path):
    monophone_labels: List[MonophoneLabel] = []
    for line in path.read_text().splitlines():
        begin_time, end_time, phoneme = line.split()
        monophone_label = MonophoneLabel(begin_time=float(begin_time), end_time=float(end_time), phoneme=phoneme)
        monophone_labels.append(monophone_label)
    return monophone_labels


def load_transcript(path: Path):
    utterance_ids: List[str] = []
    transcripts: List[str] = []
    for line in path.read_text().splitlines():
        utterance_id, transcript = line.split(':')
        utterance_ids.append(utterance_id)
        transcripts.append(transcript)
    return utterance_ids, transcripts


def load_gender_f0range(path: Path):
    speaker_ids: List[str] = []
    genders: List[Gender] = []
    f0_ranges: List[Tuple[float, float]] = []
    for line in path.read_text().splitlines():
        # header
        if line == 'speaker Male_or_Female minf0[Hz] maxf0[Hz]':
            continue

        speaker_id, gender, f0_range_min, f0_range_max = line.split()
        speaker_ids.append(speaker_id)
        genders.append(Gender(gender))
        f0_ranges.append((float(f0_range_min), float(f0_range_max)))
    return speaker_ids, genders, f0_ranges


def load_corpus_metadata(path: Path):
    utterance_ids, transcripts = load_transcript(path / _filename_transcripts)

    utterances = []
    for utterance_id, transcript in zip(utterance_ids, transcripts):
        wave_path = path / _dirname_wave / f'{utterance_id}.wav'

        # check existing
        if not wave_path.exists():
            # see https://twitter.com/hiho_karuta/status/1168368666934566912
            continue

        path_label = path / _dirname_label
        if path_label.exists():
            monophone_label_path = path_label / _dirname_monophone_label / f'{utterance_id}.lab'
            if monophone_label_path.exists():
                monophone_labels = load_monophone_label(monophone_label_path)
                full_context_label_path = path_label / _dirname_full_context_label / f'{utterance_id}.lab'
            else:
                # see https://twitter.com/hiho_karuta/status/1168370171905339392
                monophone_labels = None
                monophone_label_path = None
                full_context_label_path = None
        else:
            monophone_labels = None
            monophone_label_path = None
            full_context_label_path = None

        utterance = Utterance(
            id=utterance_id,
            transcript=transcript,
            wave_path=wave_path,
            monophone_labels=monophone_labels,
            monophone_label_path=monophone_label_path,
            full_context_label_path=full_context_label_path,
        )
        utterances.append(utterance)

    return Corpus(
        path=path,
        utterances=utterances,
    )


def load_jvs_metadata(path: Path):
    speaker_ids, genders, f0_ranges = load_gender_f0range(path / _filename_gender_f0range)

    speakers = []
    for speaker_id, gender, f0_range in zip(speaker_ids, genders, f0_ranges):
        path_speaker = path / speaker_id

        parallel_corpus = load_corpus_metadata(path_speaker / 'parallel100')
        nonpara_corpus = load_corpus_metadata(path_speaker / 'nonpara30')
        whisper_corpus = load_corpus_metadata(path_speaker / 'whisper10')
        falset_corpus = load_corpus_metadata(path_speaker / 'falset10')

        speaker = Speaker(
            path=path_speaker,
            id=speaker_id,
            gender=gender,
            f0_range=f0_range,
            parallel_corpus=parallel_corpus,
            nonpara_corpus=nonpara_corpus,
            whisper_corpus=whisper_corpus,
            falset_corpus=falset_corpus,
        )
        speakers.append(speaker)

    return JVS(
        path=path,
        speakers=speakers,
    )
