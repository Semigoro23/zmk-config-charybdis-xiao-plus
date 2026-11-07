"""Compare DTS GPIO assignments to the exported Rev G PCB connection table."""
import csv
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
shield = root / 'config/boards/shields/charybdis'
rows = list(csv.DictReader((root / 'docs/wiring.csv').open(encoding='utf-8-sig')))

def gpio(side, net):
    found = [r['nrf_gpio'] for r in rows if r['side'] == side and r['carrier_net'] == net]
    assert len(found) == 1, (side, net, found)
    m = re.fullmatch(r'P([01])\.(\d+)', found[0])
    assert m, (side, net)
    return tuple(map(int, m.groups()))

def property_gpios(text, prop):
    match = re.search(r'\b' + re.escape(prop) + r'\s*=([^;]+);', text)
    assert match, prop
    return [tuple(map(int, pair)) for pair in re.findall(r'&gpio([01])\s+(\d+)', match[1])]

common = (shield / 'charybdis.dtsi').read_text()
for side, name in [('L', 'left'), ('R', 'right')]:
    overlay = (shield / f'charybdis_{name}.overlay').read_text()
    suffix = side.lower()
    actual_rows = property_gpios(common, 'row-gpios')
    actual_cols = property_gpios(overlay, 'col-gpios')
    assert actual_rows == [gpio(side, f'row{i}_{suffix}') for i in range(1, 6)]
    assert actual_cols == [gpio(side, f'col{i}_{suffix}') for i in range(1, 7)]
    assert len(set(actual_rows + actual_cols)) == 11
    assert (0, 13) not in actual_rows + actual_cols
    if side == 'R':
        assert property_gpios(overlay, 'cs-gpios') == [gpio(side, 'rgb_l')]
        assert property_gpios(overlay, 'irq-gpios') == [gpio(side, 'miso_r')]
        for signal, net in [('SCK', 'sc_r'), ('MOSI', 'mosi_r'), ('MISO', 'mosi_r')]:
            actual = [tuple(map(int, pair)) for pair in re.findall(
                r'NRF_PSEL\(SPIM_' + signal + r',\s*(\d+),\s*(\d+)\)', overlay)]
            assert len(actual) == 2 and all(p == gpio(side, net) for p in actual)
    else:
        encoder = common.split('left_encoder:', 1)[1].split('};', 1)[0]
        assert property_gpios(encoder, 'a-gpios') == [gpio(side, 'miso_l')]
        assert property_gpios(encoder, 'b-gpios') == [gpio(side, 'sc_l')]
        used = set(actual_rows + actual_cols + [gpio(side, 'miso_l'), gpio(side, 'sc_l')])
        for pin in ['D13', 'D17', 'D18']:
            assert gpio(side, 'SPARE_' + pin + '_L') not in used

assert 'diode-direction = "row2col"' in common
assert 'CONFIG_ZMK_EXT_POWER=y' not in '\n'.join(p.read_text() for p in (root / 'config').rglob('*.conf'))
assert 'gpio_pin_configure(port, 13, GPIO_INPUT)' in (root / 'src/charge.c').read_text()
assert 'BOARD_SEEEDUINO_XIAO_BLE' in (root / 'Kconfig').read_text()
print('PASS: Rev G rows, columns, encoder, PMW3610, unused spare GPIO and charge selector')
