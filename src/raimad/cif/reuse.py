"""reuse.py: home to the Reuse CIF exporter."""

from typing import Iterator
import weakref
from dataclasses import dataclass, field

import raimad as rai

@dataclass
class ReuseStat:
    # How many proxies were steamrolled?
    steamrolls: int = 0

    edges: list[tuple[int, int]] = field(default_factory=list)

    def add_call(self, src, dst):
        self.edges.append((src, dst))

    # TODO copypasta from graphviz.py
    def _call_graph_dot(self):
        yield 'digraph D {'
        for src, dst in self.edges:
            yield f'node{src} -> node{dst}'
        yield '}'

    def call_graph_dot(self):
        return '\n'.join(self._call_graph_dot())

@dataclass
class DelayedRoutCall:
    target: weakref.ReferenceType[rai.Compo]

    # Callee symbol number. 0 for toplevel.
    # This is not necessary for building the CIF
    # file, keeping track of it just for stat.
    source: int

def is_ciffable(proxy: rai.Proxy):
    if proxy.transform.does_scale():
        return False

    if proxy.transform.does_shear():
        return False

    # TODO there are other ways to specify NOP lmap
    # lmap is a mess in general
    if proxy.lmap.shorthand is not None:
        return False

    return True

def geoms2cif(geoms, multiplier):
    # FIXME this is copypasta with export_compo
    for layer, geom in geoms.items():

        # If a layer has been LMapp'ed to None,
        # that means the user wants it discarded. Skip.
        if layer is None:
            continue

        yield f'L L{layer};'
        for poly in geom:
            yield (' '.join((
                'P ',
                *(
                    f'{int(point[0] * multiplier)} '
                    f'{int(point[1] * multiplier)} '
                    for point in poly
                    ),
                ';'
                )))

def ciffify(transform, multiplier, multiplier_rot = 1000):

    if transform.does_scale():
        raise NotImplementedError()

    if transform.does_shear():
        raise NotImplementedError()

    tstring = []

    # TODO is this order correct???
    if transform.does_translate():
        tx, ty = transform.get_translation()
        tstring.append(f"T {int(tx * multiplier)} {int(ty * multiplier)} ")

    if transform.does_rotate():
        rx = transform._affine[0][0]
        ry = transform._affine[1][0]
        tstring.append(
            "R "
            f"{int(rx * multiplier_rot)} "
            f"{int(ry * multiplier_rot)} "
            )


    return ''.join(tstring)

class Reuse:
    """CIF Exporter that does reuse subroutines."""

    def __init__(
            self,
            compo: 'rai.typing.CompoLike',
            multiplier: float = 1e3
            ) -> None:

        self.stat = ReuseStat()
        self.compo = compo
        self.rout_num = 1
        self.multiplier = multiplier

        self.cache = weakref.WeakKeyDictionary()

        lines = [
            DelayedRoutCall(weakref.ref(self.compo), 0),
            ]

        while True:
            lines, did_update = self.iterate(lines)
            if not did_update:
                break

        # FIXME hack
        foo = lines[0]
        del lines[0]
        lines.append(foo)
        lines.append('E')

        self.cif_string = '\n'.join(lines)

    def iterate(self, lines):
        new_lines = []
        new_lines_back = []  # TODO sloppy
        did_update = False

        for line in lines:
            if isinstance(line, str):
                new_lines.append(line)
                continue

            elif isinstance(line, DelayedRoutCall):
                #print('delayed call: ', line)

                did_update = True
                target = line.target()
                assert target is not None
                try:
                    target_rout = self.cache[target]
                except KeyError:
                    #print('cache miss.')
                    line_call, lines_def = self.export_compolike(
                        target,
                        source=line.source
                        )
                    new_lines_back.extend(lines_def)
                    new_lines.append(line_call)
                    continue
                else:
                    #print('cache hit.')
                    new_lines.append(f'C {target_rout};')
                    continue

            else:
                assert False

        new_lines.extend(new_lines_back)

        return new_lines, did_update
    
    def export_compolike(self, compo, source):
        new_lines = []

        this_rout_num = self.rout_num
        self.rout_num += 1

        new_lines.append(f'DS {this_rout_num} 1 1;')
        line_call = [f"C {this_rout_num}"]
        self.cache[compo] = this_rout_num
        self.stat.add_call(source, this_rout_num)

        if isinstance(compo, rai.Compo):
            #print('this is a compo.')
            new_lines.extend(
                self.export_compo(compo, this_rout_num)
                )
        elif isinstance(compo, rai.Proxy):
            if is_ciffable(compo):
                flat_transform = compo.get_flat_transform() 
                line_call.append(ciffify(flat_transform, self.multiplier))
                new_lines.append(
                    DelayedRoutCall(
                        weakref.ref(compo.compo),
                        this_rout_num
                        )
                    )
            else:
                self.stat.steamrolls += 1
                new_lines.extend(
                    geoms2cif(compo.steamroll(), self.multiplier)
                    )
        else:
            assert False

        new_lines.append('DF;')

        line_call.append(';')

        return ' '.join(line_call), new_lines
    
    def export_compo(self, compo, this_rout_num):
        lines = []
        for layer, geom in compo.geoms.items():

            # If a layer has been LMapp'ed to None,
            # that means the user wants it discarded. Skip.
            if layer is None:
                continue

            lines.append(f'L L{layer};')
            for poly in geom:
                lines.append(' '.join((
                    'P ',
                    *(
                        f'{int(point[0] * self.multiplier)} '
                        f'{int(point[1] * self.multiplier)} '
                        for point in poly
                        ),
                    ';'
                    )))

        for subcompo in compo.subcompos.values():
            lines.append(
                DelayedRoutCall(
                    weakref.ref(subcompo),
                    this_rout_num
                    )
                )

        return lines


