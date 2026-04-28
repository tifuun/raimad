#!/usr/bin/env python3

import raimad as rai

class Demo(rai.Compo):
    _experimental_lyp = {
        f'A{i}': rai.cif.lyp.Properties(dither_pattern=pattern)
        for i, pattern
        in enumerate(rai.cif.lyp.raidithers.values())
        }

    def _make(self):
        for i in range(len(rai.cif.lyp.raidithers)):
            self.subcompos.append(
                rai.RectLW(64, 64)
                .proxy()
                .move(i % 4 * 70, i // 4 * 70)
                .map(f'A{i}')
                )

if __name__ == '__main__':
    rai.export_cif(Demo(), 'raiditherdemo.cif')
    rai.export_lyp(Demo(), 'raiditherdemo.lyp')

