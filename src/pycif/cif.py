def export_cif(compo, multiplier=1e3):
    return ''.join(yield_cif(compo, multiplier))

def yield_cif(compo, multiplier=1e3, rout=1):
    yield from yield_cif_bare(compo, multiplier, rout)
    yield f'C {rout};\n'
    yield 'E'

def yield_cif_bare(compo, multiplier=1e3, rout=1):
    yield f'DS {rout} 1 1;\n'
    rout += 1
    for layer, geom in compo.geoms.items():
        yield f'\tL L{layer};\n'
        for poly in geom:
            yield '\tP '
            for point in poly:
                yield (
                    f'{int(point[0] * multiplier)} '
                    f'{int(point[1] * multiplier)} '
                    )
            yield ';\n'

    for i, subcompo in enumerate(compo.subcompos):
        yield f'\tC {rout + i};\n'
    yield 'DF;\n'

    for i, subcompo in enumerate(compo.subcompos):
        yield from yield_cif_bare(subcompo, multiplier, rout + i)


