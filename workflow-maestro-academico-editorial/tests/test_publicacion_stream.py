from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import archivos_seguros as safe


class StreamingTests(unittest.TestCase):
    def test_append_failure_preserves_original_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'registro.jsonl'
            target.write_bytes(b'Original\r\n')
            with patch('archivos_seguros.os.replace', side_effect=OSError('fallo de disco')):
                with self.assertRaises(OSError):
                    safe.atomic_append(target, 'Nuevo\n')
            self.assertEqual(target.read_bytes(), b'Original\r\n')
            self.assertEqual(list(Path(tmp).iterdir()), [target])
    def test_failed_stream_preserves_old_file_and_removes_temporary(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'salida.bin'
            target.write_bytes(b'original')
            with self.assertRaises(RuntimeError):
                with safe.atomic_output(target, overwrite=True) as stream:
                    stream.write(b'incompleto')
                    raise RuntimeError('fallo del productor')
            self.assertEqual(target.read_bytes(), b'original')
            self.assertEqual(list(Path(tmp).iterdir()), [target])

    def test_successful_stream_publishes_only_after_closing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'salida.bin'
            with safe.atomic_output(target) as stream:
                stream.write(b'completo')
                self.assertFalse(target.exists())
            self.assertEqual(target.read_bytes(), b'completo')
            self.assertEqual(list(Path(tmp).iterdir()), [target])
