from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class RegisterSafetyTests(unittest.TestCase):
    def commands(self, root):
        image = root/'imagen.png'
        image.write_bytes(b'imagen de prueba')
        return [
            [sys.executable,str(ROOT/'gestor-tablas-figuras-pies/scripts/registrar_tabla.py'), '--id','1','--titulo','Tabla','--origen','generada','--necesidad','Prueba','--modelo','Modelo','--prompt','Prompt','--razon-generacion','Razón'],
            [sys.executable,str(ROOT/'gestor-imagenes-academicas-libros/scripts/registrar_imagen.py'), '--id','1','--numero-figura','Figura 1','--capitulo','1','--ubicacion','Prueba','--fecha-creacion','2026-04-05','--archivo',str(image),'--titulo','Imagen','--origen','generada','--necesidad','Prueba','--modelo','Modelo','--prompt','Prompt','--razon-generacion','Razón','--metodo','ia_generativa','--funcion','ilustracion','--busqueda-previa','Búsqueda'],
        ]

    def test_manifest_and_annex_must_differ_before_appending(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for cmd in self.commands(root):
                with self.subTest(cmd=cmd[1]):
                    out = root/'original.jsonl'
                    out.write_bytes(b'Conservar\r\n')
                    result = subprocess.run([*cmd,'--manifest',str(out),'--anexo',str(out)],capture_output=True)
                    self.assertNotEqual(result.returncode,0)
                    self.assertEqual(out.read_bytes(),b'Conservar\r\n')

    def test_existing_manifest_is_preserved_when_appending(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index,cmd in enumerate(self.commands(root)):
                manifest, annex = root/f'{index}.jsonl', root/f'{index}.md'
                manifest.write_bytes(b'{"id":"anterior"}\r\n')
                result = subprocess.run([*cmd,'--manifest',str(manifest),'--anexo',str(annex)],capture_output=True)
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertTrue(manifest.read_bytes().startswith(b'{"id":"anterior"}\r\n'))
                self.assertIn('Prompt',annex.read_text(encoding='utf-8'))
