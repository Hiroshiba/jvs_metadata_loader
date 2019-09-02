# JVS metadata loader
Metadata loader for JVS (Japanese versatile speech) corpus.

## Requirements
Python 3.7 or higher

## Usage

```python
from pathlib import Path

from jvs_metadata_loader.loader import load_jvs_metadata

path = Path('/path/to/JVS/')
jvs_metadata = load_jvs_metadata(path)

speaker = jvs_metadata.speakers[0]
print(speaker.id)  # 'jvs001'
print(speaker.gender)  # 'Gender.M'
print(speaker.f0_range)  # '(70.0, 300.0)'

utterance = speaker.parallel_corpus.utterances[0]
print(utterance.id)  # VOICEACTRESS100_001
print(utterance.transcript)  # また、東寺のように、五大明王と呼ばれる、主要な明王の中央に配されることも多い。
print(utterance.monophone_labels[0])  # MonophoneLabel(begin_time=0.0, end_time=0.48, phoneme='sil')
print(utterance.wave_path)  # /path/to/JVS/jvs001/parallel100/wav24kHz16bit/VOICEACTRESS100_001.wav
print(utterance.full_context_label_path)  # /path/to/JVS/jvs001/parallel100/lab/ful/VOICEACTRESS100_001.lab
```
