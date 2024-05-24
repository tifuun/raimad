class NoReuse:
    def __init__(self, compo, multiplier=1e3):
        self.compo = compo
        self.rout_num = 1
        self.multiplier = multiplier

        self.cif_string = self._export_cif()

    def _export_cif(self):
        return ''.join(self._yield_cif())

    def _yield_cif(self):
        """
        Yield lines of cif file
        """
        first_rout = self.rout_num
        yield from self.yield_cif_bare(self.compo)
        yield f'C {first_rout};\n'
        yield 'E'

    def yield_cif_bare(self, compo):
        """
        Yield lines of CIF of a particular component,
        without calling it
        """

        # Opening line, define the routine
        yield f'DS {self.rout_num} 1 1;\n'

        # advance to next routine number
        self.rout_num += 1

        # Export all geometries
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

        # Precompute a list of [routine number, subcomponent]
        # Remember, subcomponents can also have subcomponents,
        # so the subroutine numbers won't always be consecutive.
        # There's no way to know ahead of time,
        # you just have to generate each subcompo and keep track of
        # the routine number
        subcompos = []
        for subcompo in compo.subcompos.values():
            subcompos.append([
                self.rout_num,
                list(self.yield_cif_bare(subcompo))
                ])

        # Call subcomponent procedures
        for i, subcompo in subcompos:
            yield f'\tC {i};\n'
        yield 'DF;\n'

        # Define those procedures
        for i, subcompo in subcompos:
            yield from subcompo

