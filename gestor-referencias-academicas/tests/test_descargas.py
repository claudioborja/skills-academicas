import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from pdf_a_contexto import download_pdf


class Response(io.BytesIO):
    headers={'Content-Type':'application/pdf'}


class DownloadTests(unittest.TestCase):
    def test_size_limit_leaves_no_partial_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch('urllib.request.urlopen',return_value=Response(b'%PDF-1.4\n' + b'x'*50)):
                with self.assertRaises(RuntimeError):
                    download_pdf('https://a.example/a.pdf',Path(tmp),max_bytes=20)
            self.assertEqual(list(Path(tmp).iterdir()),[])

    def test_same_filename_different_urls_and_retries_preserve_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)
            with patch('urllib.request.urlopen',return_value=Response(b'%PDF-1.4\nprimero')):
                first=download_pdf('https://a.example/documento.pdf',directory)
            with patch('urllib.request.urlopen',return_value=Response(b'%PDF-1.4\nsegundo')):
                second=download_pdf('https://b.example/documento.pdf',directory)
            self.assertNotEqual(first,second)
            self.assertEqual(first.read_bytes(),b'%PDF-1.4\nprimero')
            with patch('urllib.request.urlopen',return_value=Response(b'%PDF-1.4\ncambio')):
                third=download_pdf('https://a.example/documento.pdf',directory)
            self.assertNotEqual(first,third)
            self.assertEqual(first.read_bytes(),b'%PDF-1.4\nprimero')

    def test_mislabeled_html_is_rejected_without_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch('urllib.request.urlopen',return_value=Response(b'<html>Error</html>')):
                with self.assertRaises(RuntimeError):
                    download_pdf('https://a.example/a.pdf',Path(tmp))
            self.assertEqual(list(Path(tmp).iterdir()),[])
