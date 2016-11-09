from io import BytesIO
import tarfile
import os

from tests.base_case import ChatBotTestCase
from chatterbot.trainers import UbuntuCorpusTrainer


class UbuntuCorpusTrainerTestCase(ChatBotTestCase):

    def setUp(self):
        super(UbuntuCorpusTrainerTestCase, self).setUp()
        self.chatbot.set_trainer(UbuntuCorpusTrainer)

    def _create_test_corpus(self):
        """
        Create a small tar in a similar format to the
        Ubuntu corpus file in memory for testing.
        """
        tar = tarfile.TarFile('ubuntu_corpus.tar', 'w')

        data1 = (
            b'2004-11-04T16:49:00.000Z	tom		jane : Hello\n' +
            b'2004-11-04T16:49:00.000Z	tom		jane : Is anyone there?\n' +
            b'2004-11-04T16:49:00.000Z	jane	tom	I am good' +
            b'\n'
        )

        data2 = (
            b'2004-11-04T16:49:00.000Z	tom		jane : Hello\n' +
            b'2004-11-04T16:49:00.000Z	tom		jane : Is anyone there?\n' +
            b'2004-11-04T16:49:00.000Z	jane	tom	I am good' +
            b'\n'
        )

        tsv1 = BytesIO(data1)
        tsv2 = BytesIO(data2)

        tarinfo = tarfile.TarInfo('ubuntu_dialogs/3/1.tsv')
        tarinfo.size = len(data1)
        tar.addfile(tarinfo, fileobj=tsv1)

        tarinfo = tarfile.TarInfo('ubuntu_dialogs/3/2.tsv')
        tarinfo.size = len(data2)
        tar.addfile(tarinfo, fileobj=tsv2)

        tsv1.close()
        tsv2.close()
        tar.close()

        return os.path.realpath(tar.name)

    def test_extract(self):
        file_object_path = self._create_test_corpus()
        self.chatbot.trainer.extract(file_object_path)
