import PyCIF as pc

class TransformedPoint(pc.Point):
    _transform: pc.Transform

    def __init__(self, point: pc.Point, transform: pc.Transform):
        self.x = point.x
        self.y = point.y
        self.transform = transform
        self.wtf = 'wtf'

    def __get__(self, instance: pc.Markable.Marks, cls):
        if not instance:
            raise Exception("wtf")

        return instance._transform.transform_point(self)

# TODO unused
