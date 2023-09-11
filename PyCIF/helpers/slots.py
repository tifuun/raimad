class SlotsFromAnnotationsMeta(type):
    def __new__(cls, name, bases, namespace):
        if '__slots__' in namespace.keys():
            raise Exception(
                "Do not define slots manually, "
                "it will be inferred from annotations."
                )

        if '__annotations__' in namespace.keys():
            namespace['__slots__'] = tuple(namespace['__annotations__'].keys())

        else:
            namespace['__slots__'] = tuple()

        # TODO handle underscores

        return super().__new__(cls, name, bases, namespace)

