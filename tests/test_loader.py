from pathlib import Path
from unittest import TestCase

from jvs_metadata_loader.data import JVS, Speaker, Gender, Corpus, Utterance, MonophoneLabel
from jvs_metadata_loader.loader import load_jvs_metadata


class LoadTest(TestCase):
    def test_load_jvs_metadata(self):
        path = Path(__file__).parent / 'data'
        target = load_jvs_metadata(path)

        expected = JVS(
            path=path,
            speakers=[
                Speaker(
                    path=path / 'test1',
                    id='test1',
                    gender=Gender.M,
                    f0_range=(10.0, 100.0),
                    parallel_corpus=Corpus(
                        path=path / 'test1' / 'parallel100',
                        utterances=[
                            Utterance(
                                id='test1_p1',
                                transcript='テスト１の１',
                                wave_path=path / 'test1' / 'parallel100' / 'wav24kHz16bit' / 'test1_p1.wav',
                                monophone_labels=[
                                    MonophoneLabel(
                                        begin_time=0.0,
                                        end_time=0.48,
                                        phoneme='sil',
                                    ),
                                    MonophoneLabel(
                                        begin_time=0.48,
                                        end_time=0.57,
                                        phoneme='t',
                                    ),
                                    MonophoneLabel(
                                        begin_time=0.57,
                                        end_time=0.69,
                                        phoneme='e',
                                    ),
                                ],
                                full_context_label_path=path / 'test1' / 'parallel100' / 'lab' / 'ful' / 'test1_p1.lab',
                            ),
                            Utterance(
                                id='test1_p2',
                                transcript='テスト１の２',
                                wave_path=path / 'test1' / 'parallel100' / 'wav24kHz16bit' / 'test1_p2.wav',
                                monophone_labels=[
                                    MonophoneLabel(
                                        begin_time=0.0,
                                        end_time=0.1,
                                        phoneme='sil',
                                    ),
                                    MonophoneLabel(
                                        begin_time=0.1,
                                        end_time=0.2,
                                        phoneme='s',
                                    ),
                                    MonophoneLabel(
                                        begin_time=0.2,
                                        end_time=0.3,
                                        phoneme='t',
                                    ),
                                ],
                                full_context_label_path=path / 'test1' / 'parallel100' / 'lab' / 'ful' / 'test1_p2.lab',
                            ),
                        ],
                    ),
                    nonpara_corpus=Corpus(
                        path=path / 'test1' / 'nonpara30',
                        utterances=[]
                    ),
                    whisper_corpus=Corpus(
                        path=path / 'test1' / 'whisper10',
                        utterances=[]
                    ),
                    falset_corpus=Corpus(
                        path=path / 'test1' / 'falset10',
                        utterances=[]
                    ),
                ),
                Speaker(
                    path=path / 'test2',
                    id='test2',
                    gender=Gender.F,
                    f0_range=(100.0, 1000.0),
                    parallel_corpus=Corpus(
                        path=path / 'test2' / 'parallel100',
                        utterances=[
                            Utterance(
                                id='test2_p1',
                                transcript='テスト２の１',
                                wave_path=path / 'test2' / 'parallel100' / 'wav24kHz16bit' / 'test2_p1.wav',
                                monophone_labels=[
                                    MonophoneLabel(
                                        begin_time=0.0,
                                        end_time=0.48,
                                        phoneme='sil',
                                    ),
                                    MonophoneLabel(
                                        begin_time=0.48,
                                        end_time=0.57,
                                        phoneme='f',
                                    ),
                                    MonophoneLabel(
                                        begin_time=0.57,
                                        end_time=0.69,
                                        phoneme='u',
                                    ),
                                ],
                                full_context_label_path=path / 'test2' / 'parallel100' / 'lab' / 'ful' / 'test2_p1.lab',
                            ),
                        ],
                    ),
                    nonpara_corpus=Corpus(
                        path=path / 'test2' / 'nonpara30',
                        utterances=[]
                    ),
                    whisper_corpus=Corpus(
                        path=path / 'test2' / 'whisper10',
                        utterances=[]
                    ),
                    falset_corpus=Corpus(
                        path=path / 'test2' / 'falset10',
                        utterances=[]
                    ),
                ),
            ],
        )

        self.assertEqual(target, expected)




