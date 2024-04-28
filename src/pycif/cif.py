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
    #rout_num: int

def find_link_in_stack(top_proxy):

    link = None
    depth = 0

    for proxy in top_proxy.descend_p():
        if link is None:
            depth = depth + 1
            if proxy._cif_link:
                link = proxy.compo

        else:
            if proxy._cif_link:
                # TODO
                raise Exception

    return link, depth

def find_linked_in_stack(top_proxy):

    link = None
    depth = 0

    for proxy in top_proxy.descend_p():
        if link is None:
            depth = depth + 1
            if proxy._cif_linked:
                link = proxy.compo

        else:
            if proxy._cif_linked:
                # TODO
                raise Exception

    return link, depth


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

        # map proxy objects to routine numbers
        self.rout_map = {}

        # list of (caller, callee) that shows which
        # cif routine calls which routines
        self.rout_list = set()

    def export_cif(self):
        self._first_pass()
        assert len(self.rout_map) == self.rout_num - 1

        for i, fragment in enumerate(fragments):
            if isinstance(fragment, DelayedRoutCall):
                rout_num = self.rout_map[fragment.compo]
                fragments[i] = ''.join((
                    f"\tC {rout_num} ",
                    *self.compile_transform(fragment.transform),
                    ";\n"
                    ))
                #self.rout_list.add((fragment.rout_num, rout_num))

        #print('\n'.join(map(str, self.rout_list)))
        self._call_root()
        return ''.join(fragments)

    def _frag(self, fragment):
        self.cif_fragments.append(fragment)

    def _delayed(self, compo, transform):
        self.cif_fragments.append(DelayedRoutCall(compo, transform))

    def _call_root(self):
        self._frag( 'C 1;\n' )
        self._frag( 'E' )

    def _make_compo(self, compo):
        this_rout_num = self.rout_num
        self.rout_num += 1
        self.rout_map[compo] = this_rout_num

        if isinstance(compo, pc.Proxy):

            if compo._cif_link is not None:

                self._delayed(compo.compo, compo.transform)

            else:
                yield f'DS {this_rout_num} 1 1;\n'
                yield DelayedRoutCall(compo.compo, compo.transform)
                yield 'DF;\n'

                yield from self.yield_cif_bare(compo.compo)

        else:
            # Export all geometries
            yield f'DS {this_rout_num} 1 1;\n'
            yield from self.yield_geometries(compo)

            # Precompute a list of [routine number, subcomponent]
            # Remember, subcomponents can also have subcomponents,
            # so the subroutine numbers won't always be consecutive.
            # There's no way to know ahead of time,
            # you just have to generate each subcompo and keep track of
            # the routine number
            subcompos = list(self.yield_subcompos(compo))

            # Call subcomponent procedures
            for i, subcompo in subcompos:
                self.rout_list.add((this_rout_num, i))
                yield f'\tC {i};\n'

            # close the cell definition
            yield 'DF;\n'

            # Define those procedures
            for i, subcompo in subcompos:
                yield from subcompo

        #if isinstance(compo, pc.Proxy) and compo._cif_link is not None:
        #    yield DelayedRoutCall(compo._cif_link)
        #    yield 'DF;\n'

        #link, depth = find_link_in_stack(compo)

        #if link is not None:
        #    yield DelayedRoutCall(
        #        link,
        #        compo.get_flat_transform(depth),  # TODO huh?
        #        this_rout_num
        #        )
        #    yield 'DF;\n'
        #    # rout call list will be updated on second stage

        #elif (
        #        self.cif_native
        #        and
        #        (cif_string := compo._export_cif()) is not NotImplemented
        #        ):

        #    yield cif_string
        #    yield 'DF;\n'
        #    assert not compo.subcompos

        #else:
        #    # Export all geometries
        #    yield from self.yield_geometries(compo)

        #    # Precompute a list of [routine number, subcomponent]
        #    # Remember, subcomponents can also have subcomponents,
        #    # so the subroutine numbers won't always be consecutive.
        #    # There's no way to know ahead of time,
        #    # you just have to generate each subcompo and keep track of
        #    # the routine number
        #    subcompos = list(self.yield_subcompos(compo))

        #    # Call subcomponent procedures
        #    for i, subcompo in subcompos:
        #        self.rout_list.add((this_rout_num, i))
        #        yield f'\tC {i};\n'

        #    # close the cell definition
        #    yield 'DF;\n'

        #    # Define those procedures
        #    for i, subcompo in subcompos:
        #        yield from subcompo

    def yield_geometries(self, compo):
        """
        yield the direct geometries of a compo as CIF polygons,
        with the appropriate layer switches.
        """
        for layer, geom in compo.geoms.items():
            yield f'\tL L{layer};\n'
            for poly in geom:
                yield '\tP '
                for point in poly:
                    yield (
                        f'{int(point[0] * self.multiplier)} '
                        f'{int(point[1] * self.multiplier)} '
                        )
                yield ';\n'

    def yield_subcompos(self, compo):
        """
        return subcompos of a compo as cif.
        This forms a mutual recursion with
        yield_cif_bare.
        """
        for subcompo in compo.subcompos.values():
            yield [
                self.rout_num,
                list(self.yield_cif_bare(subcompo))
                ]

    def compile_transform(self, transform):
        if transform.does_scale():
            # TODO also possible to mirror in cif
            return None

        if transform.does_shear():
            return None

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



