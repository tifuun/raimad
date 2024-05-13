import pycif as pc

class RectWH(pc.Compo):
    """
    RectWH

    A rectangle defined by width and height.
    """
    browser_tags = ["builtin", "polygon"]

    class Options:
        width = pc.Option('Width of rectangle', browser_default=15)
        height = pc.Option('Height of rectangle', browser_default=10)

    def _make(self, width: int, height: int):
        self.width = width
        self.height = height

        self.geoms.update({
            'root': [
                [
                    [- width / 2, - height / 2],
                    [+ width / 2, - height / 2],
                    [+ width / 2, + height / 2],
                    [- width / 2, + height / 2],
                    ]
                ]
            })

    #def _export_cif(self, transform=None):
    #    transform = transform or pc.Transform()
    #    import numpy as np
    #    move_x, move_y = pc.transform.get_translation(transform._affine)
    #    scale_x, scale_y, shear = pc.transform.get_scale_shear(transform._affine)
    #    rotation = pc.transform.get_rotation(transform._affine)

    #    does_translate = np.linalg.norm((move_x, move_y)) > 0.001  # TODO epsilon
    #    does_rotate = rotation > 0.01
    #    does_shear = shear > 0.01
    #    does_scale = 1 - np.linalg.norm((scale_x, scale_y)) > 0.001

    #    if does_shear or does_scale:
    #        return NotImplemented

    #    (x1, y1), _, (x2, y2), _ = self.geoms['root'][0]
    #    cifstring = [
    #        "\tL Lwtf;\n\tB "
    #        f"{int((abs(x2 - x1)) * 1e3)} "
    #        f"{int((abs(y2 - y1)) * 1e3)} "
    #        f"{int(((x1 + x2) / 2 + move_x) * 1e3)} "
    #        f"{int(((y1 + y2) / 2 + move_y) * 1e3)} "
    #        ]

    #    if does_rotate:
    #        # TODO call cif exporter
    #        cifstring.append(
    #            f"{int(np.cos(rotation) * 1e3)} {int(np.sin(rotation) * 1e3)} "
    #        )

    #    cifstring.append(";\n")

    #    return ''.join(cifstring)

    #def _export_cif(self, cif_exporter):
    #    cifstring = [
    #        "\tL Lroot;\n\tB "
    #        f"{int(self.width * cif_exporter.multiplier)} "
    #        f"{int(self.height * cif_exporter.multiplier)} "
    #        "0 "
    #        "0 "
    #        ]

    #    cifstring.append(";\n")

    #    return ''.join(cifstring)

    #def _export_cif_transformed(self, cif_exporter, proxy):
    #    transform = proxy.transform

    #    if transform.does_scale():
    #        return NotImplemented

    #    if transform.does_shear():
    #        return NotImplemented

    #    move_x, move_y = transform.get_translation()
    #    cifstring = [
    #        f"\tL L{proxy.lmap['root']};\n\tB "
    #        f"{int(self.width * cif_exporter.multiplier)} "
    #        f"{int(self.height * cif_exporter.multiplier)} "
    #        f"{int(move_x * cif_exporter.multiplier)} "
    #        f"{int(move_y * cif_exporter.multiplier)} "
    #        ]

    #    if transform.does_rotate():
    #        # TODO call cif exporter
    #        rot = transform.get_rotation()
    #        rotvec_x = int(pc.cos(rot) * cif_exporter.multiplier)
    #        rotvec_y = int(pc.sin(rot) * cif_exporter.multiplier)

    #        cifstring.append(
    #            f"{rotvec_x} {rotvec_y} "
    #        )

    #    cifstring.append(";\n")

    #    return ''.join(cifstring)

    def _export_cif(self, exporter, lmap, transform):
        if transform.does_scale():
            return NotImplemented

        if transform.does_shear():
            return NotImplemented

        move_x, move_y = transform.get_translation()
        cifstring = [
            f"\tL L{lmap['root']};\n\tB "
            f"{int(self.width * exporter.multiplier)} "
            f"{int(self.height * exporter.multiplier)} "
            f"{int(move_x * exporter.multiplier)} "
            f"{int(move_y * exporter.multiplier)} "
            ]

        if transform.does_rotate():
            # TODO call cif exporter
            rot = transform.get_rotation()
            rotvec_x = int(pc.cos(rot) * exporter.multiplier)
            rotvec_y = int(pc.sin(rot) * exporter.multiplier)

            cifstring.append(
                f"{rotvec_x} {rotvec_y} "
            )

        cifstring.append(";\n")

        return ''.join(cifstring)

