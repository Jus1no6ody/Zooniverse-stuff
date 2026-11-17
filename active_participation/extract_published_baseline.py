"""Extract the reported 30-day June 2021 reference point from PLOS Table 1."""
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCE = 'https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0293289&type=manuscript'
LABELS = {'Zooniverse': 'zooniverse', 'EyeWire': 'eyewire', 'EteRNA': 'eterna', 'FoldIt': 'foldit'}


def extract(raw):
    root = ET.fromstring(raw)
    table = next(t for t in root.iter('table-wrap') if t.get('id') == 'pone.0293289.t001')
    rows = []
    for row in table.iter('tr'):
        cells = [''.join(cell.itertext()).strip() for cell in row if cell.tag in ('td', 'th')]
        if len(cells) == 6 and cells[1] in LABELS:
            rows.append({'platform': LABELS[cells[1]],
                         'reported_active_accounts': int(cells[4].replace('’', '').replace("'", '').replace(',', ''))})
    if {r['platform'] for r in rows} != set(LABELS.values()) or len(rows) != 4:
        raise ValueError('Could not uniquely locate all four platform rows')
    return {
        'paper_doi': 'https://doi.org/10.1371/journal.pone.0293289',
        'table': 'Table 1', 'source_xml_url': SOURCE,
        'source_xml_sha256': hashlib.sha256(raw).hexdigest(), 'source_license': 'CC BY',
        'reported_period': '30-day window ending in June 2021',
        'exact_start_utc': None, 'exact_end_exclusive_utc': None,
        'activity_definition': 'At least one task in the reported window, as defined by the original study',
        'warning': 'Published snapshot, not a calendar-month or annual time series; exact bounds and cross-platform task definitions require clarification.',
        'observations': rows,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--xml', required=True, type=Path, help='Manuscript XML downloaded from source_xml_url')
    parser.add_argument('--output', type=Path, default=Path(__file__).parent / 'published_2021_reference.json')
    args = parser.parse_args()
    args.output.write_text(json.dumps(extract(args.xml.read_bytes()), indent=2))
