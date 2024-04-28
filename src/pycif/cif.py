from dataclasses import dataclass

import numpy as np

import pycif as pc

class CIFExportError(Exception):
    pass

class CannotCIFLinkError(Exception):
    pass

@dataclass
class DelayedRoutCall():
    compo: pc.Proxy
    transform: pc.Transform
    rout_num: int
    name: str | None = None


class CIFExporter:
    def __init__(
            self,
            compo,
            multiplier=1e3,
            rot_multiplier=1e3,
            cif_native=True,
            cif_link=True,
            cif_link_fatal=False
            ):

        self.compo = compo
        self.rout_num = 1
        self.multiplier = multiplier
        self.rot_multiplier = rot_multiplier
        self.cif_native = cif_native

        # TODO cif_link and cif_link_native
        self.cif_fragments = []

        # map proxy/compo objects to routine numbers
        self.rout_map = {}
        # map routine numbers to oroxy/compo objects
        self.reverse_rout_map = {}

        # list of (caller, callee) that shows which
        # cif routine calls which routines
        self.rout_list = set()

        self.rout_names = {}

    def export_cif(self):
        self._make_compo(self.compo)

        new_compos = 69420
        while new_compos > 0:
            new_compos = 0

            for i, fragment in enumerate(self.cif_fragments):
                if not isinstance(fragment, DelayedRoutCall):
                    continue

                rout_num = (
                    self.rout_map.get(fragment.compo, None)
                    or
                    self._make_compo(fragment.compo)
                    )

                self.cif_fragments[i] = ''.join((
                    f'\t C {rout_num} ',
                    *self.compile_transform(fragment.transform),
                    ";\n"
                    ))

                self.rout_list.add((fragment.rout_num, rout_num))
                self.rout_names[rout_num] = fragment.name
                new_compos += 1

        self._call_root()
        return ''.join(self.cif_fragments)

    def _frag(self, fragment):
        self.cif_fragments.append(fragment)

    def _delayed(self, compo, transform, rout_num, name=None):
        self.cif_fragments.append(DelayedRoutCall(compo, transform, rout_num, name))

    def _call_root(self):
        self._frag( 'C 1;\n' )
        self._frag( 'E' )

    def _make_compo(self, compo):
        this_rout_num = self.rout_num
        self.rout_num += 1
        self.rout_map[compo] = this_rout_num
        self.reverse_rout_map[this_rout_num] = compo

        if isinstance(compo, pc.Proxy):
            self._frag( f'DS {this_rout_num};\n' )
            self._delayed(compo.compo, compo.transform, this_rout_num)
            self._frag( 'DF;\n' )

        else:
            self._frag( f'DS {this_rout_num} 1 1;\n' )
            self._make_geometries(compo)

            for name, proxy in compo.subcompos.items():
                self._delayed(proxy, None, this_rout_num, name)

            # close the cell definition
            self._frag( 'DF;\n' )

        return this_rout_num

    def _make_geometries(self, compo):
        """
        yield the direct geometries of a compo as CIF polygons,
        with the appropriate layer switches.
        """
        for layer, geom in compo.geoms.items():
            self._frag(f'\tL L{layer};\n')
            for poly in geom:
                self._frag('\tP ')
                for point in poly:
                    self._frag(
                        f'{int(point[0] * self.multiplier)} '
                        f'{int(point[1] * self.multiplier)} '
                        )
                self._frag(';\n')

    def compile_transform(self, transform):
        if transform is None:
            return ''

        if transform.does_scale():
            # TODO also possible to mirror in cif
            raise Exception()

        if transform.does_shear():
            raise Exception()

        if transform.does_translate():
            yield from self.compile_translation(*transform.get_translation())

        if transform.does_rotate():
            yield from self.compile_rotation(transform.get_rotation())

    def compile_rotation(self, rotation):
        yield 'R '
        yield str(int(np.cos(rotation) * self.rot_multiplier))
        yield ' '
        yield str(int(np.sin(rotation) * self.rot_multiplier))
        yield ' '

    def compile_translation(self, move_x, move_y):
        yield 'T '
        yield str(int(move_x * self.multiplier))
        yield ' '
        yield str(int(move_y * self.multiplier))
        yield ' '

    @pc.join_generator('', pc.gv.DOTString)
    def as_dot(self):
        yield 'digraph D {\n'

        for rout_num in range(1, self.rout_num):
            compo = self.reverse_rout_map[rout_num]

            label = []
            label.append(f'Cell {rout_num}')

            if isinstance(compo, pc.Proxy):
                shape = 'ellipse'
                if (name := self.rout_names.get(rout_num)):
                    label.append(rf'\"{name}\"')

                if compo.transform.does_translate:
                    transl = compo.transform.get_translation()
                    label.append(f'Move {transl[0]:.3g}, {transl[1]:.3g}')

                if compo.transform.does_rotate:
                    rot = pc.rad2deg(compo.transform.get_rotation())
                    label.append(f'Rotate {rot:.3g}')
            else:
                shape = 'box'
                label.append(type(compo).__name__)

            label = r'\n'.join(label)

            yield f'\t{rout_num} [shape={shape} label="{label}"];\n'

        for from_, to in self.rout_list:
            yield f'\t{from_} -> {to};\n'

        yield '}\n'


def export_cif(
        compo,
        multiplier=1e3,
        rot_multiplier=1e3,
        cif_native=True,
        cif_link=True,
        cif_link_fatal=False,
        ):
    return CIFExporter(
        compo,
        multiplier,
        rot_multiplier,
        cif_native,
        cif_link,
        cif_link_fatal
        ).export_cif()



