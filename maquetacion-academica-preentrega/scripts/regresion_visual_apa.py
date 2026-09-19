"""Regresión geométrica del PDF renderizado de cuatro casos APA controlados.

No audita manuscritos arbitrarios ni sustituye inspección humana de los PNG.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs


def compact(text):
    return ' '.join(text.split())


def check_pdf(path, *, title, running_head=None, abstract_marker, body_marker, note_marker=None):
    errors = []

    def fail(code, page, detail):
        errors.append(dict(code=code, page=page, detail=detail))

    with pymupdf.open(path) as pdf:
        texts = [compact(page.get_text()) for page in pdf]
        if len(pdf) != 3:
            fail('page_count', None, f'Se esperaban 3 páginas; se obtuvieron {len(pdf)}.')
        for number, page in enumerate(pdf, 1):
            if abs(page.rect.width - 612) > 1 or abs(page.rect.height - 792) > 1:
                fail('page_size', number, 'El caso requiere papel carta vertical.')
            words = page.get_text('words')
            numbers = [w for w in words if w[4] == str(number) and 20 <= w[1] <= 60]
            if len(numbers) != 1 or abs(numbers[0][2] - (page.rect.width - 72)) > 6:
                fail('page_number', number, 'Número ausente, repetido, incorrecto o fuera del margen derecho.')
            if running_head:
                hits = page.search_for(running_head, clip=pymupdf.Rect(0, 15, page.rect.width, 65))
                if len(hits) != 1 or abs(hits[0].x0 - 72) > 6:
                    fail('running_head', number, 'Encabezado abreviado ausente o desplazado.')
            if number == 1:
                for drawing in page.get_drawings():
                    rect = drawing['rect']
                    if rect.width >= 80 and rect.height <= 5 and rect.y0 >= 72:
                        fail('cover_border', number, 'Línea horizontal decorativa en la portada.')
                        break
        for marker, expected_page, code in ((abstract_marker, 2, 'abstract_page'),
                                             (body_marker, 3, 'body_page')):
            pages = [n for n, text in enumerate(texts, 1) if compact(marker) in text]
            if pages != [expected_page]:
                fail(code, expected_page, f'El texto de control aparece en páginas {pages}.')
        for number in (1, 3):
            if len(texts) < number or compact(title) not in texts[number - 1]:
                fail('title', number, 'Título incompleto o ausente.')
        if note_marker and (not texts or compact(note_marker) not in texts[0]):
            fail('author_note', 1, 'Nota de autor incompleta o fuera de la portada.')
        return dict(pages=len(pdf), errors=errors)


def cases():
    student = dict(profile='student', title='Aprendizaje universitario', authors='Ana Pérez',
                   affiliation='Departamento de Educación, Universidad de Prueba',
                   course='EDU 101 Aprendizaje', instructor='Luis López', due_date='19 de septiembre de 2026')
    professional = {k: student[k] for k in ('title', 'authors', 'affiliation')}
    professional.update(profile='professional', running_head='APRENDIZAJE UNIVERSITARIO',
                        author_note=['La autora declara que no existen conflictos de interés.',
                                     'La correspondencia debe dirigirse a Ana Pérez, Universidad de Prueba. Correo electrónico: ana@example.org.'])
    long_title = ('Estrategias de aprendizaje y acompañamiento docente en estudiantes universitarios '
                  'de primer año en entornos virtuales y presenciales de instituciones latinoamericanas')
    long_note = [
        'Ana Pérez pertenece al Departamento de Educación de la Universidad de Prueba. Los datos de este documento son ficticios y permiten evaluar la presentación de una portada profesional.',
        'La afiliación de la autora no ha cambiado durante la preparación del manuscrito. Se conserva la información institucional compartida en la línea de afiliación de la portada.',
        'La autora declara que no existen conflictos de interés. Este documento no recibió financiación externa. Se agradece la revisión de la legibilidad de sus elementos y de la continuidad de la numeración.',
        professional['author_note'][-1],
    ]
    return {'estudiantil': student, 'estudiantil_titulo_largo': dict(student, title=long_title),
            'profesional': professional,
            'profesional_nota_larga': dict(professional, title=long_title, author_note=long_note)}


def run_suite(output, renderer_python, renderer_script, timeout=120):
    output, renderer_python, renderer_script = map(Path, (output, renderer_python, renderer_script))
    # Una carpeta nueva por ejecución evita confundir renders antiguos con resultados actuales.
    validate_outputs([renderer_python, renderer_script], [output])
    for path in (renderer_python, renderer_script):
        if not path.is_file():
            raise ValueError(f'No existe la dependencia explícita: {path}')
    if timeout <= 0:
        raise ValueError('timeout debe ser positivo')
    output.mkdir(parents=True, exist_ok=False)
    converter = Path(__file__).with_name('markdown_a_docx.py')
    report = dict(scope='Regresión de cuatro casos controlados; no certificación APA ni revisión humana.',
                  platform=platform.platform(), python=sys.version,
                  renderer_python=str(renderer_python.resolve()), renderer_script=str(renderer_script.resolve()),
                  renderer_sha256=hashlib.sha256(renderer_script.read_bytes()).hexdigest(),
                  cases=[], status='error')
    abstract = 'Este resumen permite comprobar la separación de páginas del documento.'
    body = 'El cuerpo permite comprobar el inicio del texto y la continuidad de la numeración.'
    for name, metadata in cases().items():
        folder = output / name
        folder.mkdir()
        source, data, docx = folder / 'entrada.md', folder / 'datos.json', folder / 'prueba.docx'
        atomic_write(source, f'# Resumen\n\n{abstract}\n\n# {metadata["title"]}\n\n{body}\n')
        atomic_write(data, json.dumps(metadata, ensure_ascii=False, indent=2))
        result = dict(name=name, errors=[], pages=0)
        try:
            commands = [
                [str(renderer_python.resolve()), str(converter), str(source.resolve()), '--out', str(docx.resolve()),
                 '--apa7-strict', '--apa-metadata', str(data.resolve())],
                [str(renderer_python.resolve()), str(renderer_script.resolve()), str(docx.resolve()),
                 '--output_dir', str((folder / 'render').resolve()), '--emit_pdf'],
            ]
            for command in commands:
                subprocess.run(command, check=True, capture_output=True, text=True,
                               encoding='utf-8', errors='replace', timeout=timeout)
            pdf = folder / 'render/prueba.pdf'
            result.update(check_pdf(pdf, title=metadata['title'], running_head=metadata.get('running_head'),
                                    abstract_marker=abstract, body_marker=body,
                                    note_marker=' '.join(metadata.get('author_note', [])) or None))
            expected = {f'page-{n}.png' for n in range(1, result['pages'] + 1)}
            actual = {p.name for p in (folder / 'render').glob('page-*.png')}
            if actual != expected:
                result['errors'].append(dict(code='page_images', page=None, detail='Faltan PNG o hay páginas sobrantes.'))
            for image in (folder / 'render').glob('page-*.png'):
                pixmap = pymupdf.Pixmap(str(image))
                if pixmap.width < 600 or pixmap.height < 700 or abs(pixmap.width / pixmap.height - 612 / 792) > .02:
                    result['errors'].append(dict(code='page_images', page=None, detail=f'Dimensiones inesperadas: {image.name}'))
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            detail = str(error)
            if isinstance(error, subprocess.CalledProcessError):
                detail += '\n' + (error.stderr or '')[-2000:]
            result['errors'].append(dict(code='execution', page=None, detail=detail))
        report['cases'].append(result)
    report['status'] = ('error' if any(e['code'] == 'execution' for c in report['cases'] for e in c['errors'])
                        else 'failed' if any(c['errors'] for c in report['cases']) else 'passed')
    atomic_write(output / 'informe.json', json.dumps(report, ensure_ascii=False, indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path, help='Directorio nuevo para casos, PNG, PDF e informe.json')
    parser.add_argument('--renderer-python', required=True, type=Path, help='Python del entorno de renderizado, con python-docx y pdf2image')
    parser.add_argument('--renderer-script', required=True, type=Path, help='Ruta explícita al render_docx.py de confianza')
    parser.add_argument('--timeout', type=int, default=120, help='Límite de segundos por proceso')
    args = parser.parse_args()
    try:
        report = run_suite(args.out, args.renderer_python, args.renderer_script, args.timeout)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps({'status': report['status'], 'report': str(args.out / 'informe.json')}, ensure_ascii=False))
    return {'passed': 0, 'failed': 1, 'error': 2}[report['status']]


if __name__ == '__main__':
    raise SystemExit(main())
