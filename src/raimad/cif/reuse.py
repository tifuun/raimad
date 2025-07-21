"""reuse.py: home to the Reuse CIF exporter."""

from typing import Iterator
import weakref
from dataclasses import dataclass

import raimad as rai

@dataclass
class ReuseStat:
    steamrolls: int = 0

@dataclass
class DelayedRoutCall:
    target: weakref.ReferenceType[rai.Compo]
    #lmap: None | rai.t.LMap = None

def is_ciffable(proxy: rai.Proxy):
    if proxy.transform.does_scale():
        return False

    if proxy.transform.does_rotate():
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

def ciffify(transform, multiplier):
    if transform.does_scale():
        raise NotImplementedError()

    if transform.does_rotate():
        raise NotImplementedError()

    if transform.does_shear():
        raise NotImplementedError()

    tstring = []

    if transform.does_translate():
        tx, ty = transform.get_translation()
        tstring.append(f"T{int(tx * multiplier)} {int(ty * multiplier)}")

    return ' '.join(tstring)

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
            DelayedRoutCall(weakref.ref(self.compo)),
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
                    line_call, lines_def = self.export_compolike(target)
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
    
    def export_compolike(self, compo):
        new_lines = []

        new_lines.append(f'DS {self.rout_num} 1 1;')
        line_call = [f"C {self.rout_num}"]
        self.cache[compo] = self.rout_num
        self.rout_num += 1

        if isinstance(compo, rai.Compo):
            #print('this is a compo.')
            new_lines.extend(
                self.export_compo(compo)
                )
        elif isinstance(compo, rai.Proxy):
            if is_ciffable(compo):
                flat_transform = compo.get_flat_transform() 
                line_call.append(ciffify(flat_transform, self.multiplier))
                new_lines.append(
                    DelayedRoutCall(
                        weakref.ref(compo.compo),
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
    
    def export_compo(self, compo):
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
                DelayedRoutCall(weakref.ref(subcompo))
                )

        return lines


    def _export_cif(self) -> str:
        self.queue.append(DelayedRoutCall(self.compo))

    def _yield_cif(self) -> Iterator[str]:
        """Yield lines of cif file."""
        first_rout = self.rout_num
        yield from self.yield_cif_bare(self.compo)
        yield f'C {first_rout};\n'
        yield 'E'

    def yield_cif_bare(self, compo: 'rai.typing.CompoLike') -> Iterator[str]:
        """Yield lines of CIF of a particular component, without calling it."""

        if isinstance(compo, rai.Compo):
            # Opening line, define the routine
            yield f'DS {self.rout_num} 1 1;\n'
            self.cache[id(compo)] = self.rout_num

            # advance to next routine number
            self.rout_num += 1

            # Export all geometries
            for layer, geom in compo.geoms.items():

                # If a layer has been LMapp'ed to None,
                # that means the user wants it discarded. Skip.
                if layer is None:
                    continue

                yield f'\tL L{layer};\n'
                for poly in geom:
                    yield '\tP '
                    for point in poly:
                        yield (
                            f'{int(point[0] * self.multiplier)} '
                            f'{int(point[1] * self.multiplier)} '
                            )
                    yield ';\n'

            # Precompute a list of [routine number, subcomponent]
            # Remember, subcomponents can also have subcomponents,
            # so the subroutine numbers won't always be consecutive.
            # There's no way to know ahead of time,
            # you just have to generate each subcompo and keep track of
            # the routine number
            subcompos = []
            for subcompo in compo.subcompos.values():
                subcompos.append((
                    self.rout_num,
                    list(self.yield_cif_bare(subcompo))
                    ))

            # Call subcomponent procedures
            for i, _ in subcompos:
                yield f'\tC {i};\n'
            yield 'DF;\n'

            # Define those procedures
            for _, this_subcompo in subcompos:
                yield from this_subcompo

        elif isinstance(compo, rai.Proxy):
            assert False

            # Opening line, define the routine
            yield f'DS {self.rout_num} 1 1;\n'
            self.cache[id(compo)] = self.rout_num

            # advance to next routine number
            self.rout_num += 1

            yield DelayedRoutCall

            yield 'DF;\n'

