import json
import os
from itertools import chain
from pathlib import Path
from typing import Sequence, Dict, List

import fire
from tqdm import tqdm

from jvs_metadata_loader.data import Speaker, Utterance
from jvs_metadata_loader.loader import load_jvs_metadata


def flatten(
        jvs_path: str,
        output_path: str,
        target_file_list: Sequence[str] = ('wave', 'monophone_label', 'full_context_label'),
        target_corpus_list: Sequence[str] = ('parallel', 'nonpara', 'whisper', 'falset'),
        only_label_existing: bool = False,
):
    jvs = load_jvs_metadata(Path(jvs_path))
    output_path = Path(output_path)

    output_path.mkdir()

    with_wave = 'wave' in target_file_list
    output_wave_path = output_path / 'wave'
    if with_wave:
        output_wave_path.mkdir()

    with_monophone_label = 'monophone_label' in target_file_list
    output_monophone_label_path = output_path / 'monophone_label'
    if with_monophone_label:
        output_monophone_label_path.mkdir()

    with_full_context_label = 'full_context_label' in target_file_list
    output_full_context_label_path = output_path / 'full_context_label'
    if with_full_context_label:
        output_full_context_label_path.mkdir()

    output_utterances_each_speaker_path = output_path / 'utterances_each_speaker.json'

    utterances_each_speaker: Dict[Speaker, List[Utterance]] = {}

    for speaker in tqdm(jvs.speakers, desc='num of done speakers'):
        utterances = list(chain(
            speaker.parallel_corpus.utterances if 'parallel' in target_corpus_list else [],
            speaker.nonpara_corpus.utterances if 'nonpara' in target_corpus_list else [],
            speaker.whisper_corpus.utterances if 'whisper' in target_corpus_list else [],
            speaker.falset_corpus.utterances if 'falset' in target_corpus_list else [],
        ))

        if only_label_existing:
            utterances = [
                utterance
                for utterance in utterances
                if utterance.monophone_label_path is not None
            ]

        for utterance in utterances:
            if with_wave:
                src_path = utterance.wave_path
                dst_path = output_wave_path / f'{speaker.id}_{utterance.id}{src_path.suffix}'
                os.link(str(src_path), str(dst_path))

            if with_monophone_label:
                src_path = utterance.monophone_label_path
                dst_path = output_monophone_label_path / f'{speaker.id}_{utterance.id}{src_path.suffix}'
                os.link(str(src_path), str(dst_path))

            if with_full_context_label:
                src_path = utterance.full_context_label_path
                dst_path = output_full_context_label_path / f'{speaker.id}_{utterance.id}{src_path.suffix}'
                os.link(str(src_path), str(dst_path))

        utterances_each_speaker[speaker] = utterances

    json.dump(
        {
            speaker.id: [f'{speaker.id}_{utterance.id}' for utterance in utterances]
            for speaker, utterances in utterances_each_speaker.items()
        },
        output_utterances_each_speaker_path.open(mode='w'),
    )


if __name__ == '__main__':
    fire.Fire(flatten)
