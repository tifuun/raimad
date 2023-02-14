"""
Class for base component
"""

from typing import Any, Type, Self, List
from dataclasses import dataclass, field
import inspect
from abc import ABC, abstractmethod
import logging

from PyCIF.draw.Polygon import Polygon
from PyCIF.draw.PolygonGroup import PolygonGroup
from PyCIF.draw.Markable import Markable
from PyCIF.draw import OptCategory
from PyCIF.draw import LayerCategory
from PyCIF.misc.Dotdict import Dotdict

# Possibilities:
# None can be used when parent and child have identical layers
# OR when both have only one layer
# str can be used to specify the layername of the parent
# when child has only one layer
# otherwise needs full dict
SubcomponentLayermapShorthand = None | str | dict
SubpolygonLayermapShorthand = None | str

Shadow = None


class Component(ABC, Markable):
    """
    Class for base component
    """
    optspecs = Dotdict()
    layerspecs = Dotdict()
    modulebrowser_howtoget = None
    # Something like 'from pc_Mymodule.Mycompo import Mycompo',
    # otherwise this is autogenerated using inspect.

    def __init__(self, opts=None, transform=None):
        """
        args and kwargs are interpreted the same way as Dotdict,
        so can be used to set parameters during creation.
        """
        super().__init__(transform=transform)
        self.subcomponents = []
        self.subpolygons = []

        self.set_opts(Dotdict())
        if opts is not None:
            self.set_opts(opts)

    def update_opts(self, opts: dict):
        """
        Apply new options to component, keeping
        old ones in place.
        """
        if not set(opts.keys()).issubset(self.optspecs.keys()):
            raise Exception(
                "opts must be a subset of optspecs"
                )
        self.opts.update(opts)

    def set_opts(self, opts: dict):
        """
        Apply new options,
        overwriting old options.
        """
        if not set(opts.keys()).issubset(self.optspecs.keys()):
            raise Exception(
                "opts must be a subset of optspecs"
                )
        self.opts = Dotdict({
            name: optspec.default
            for name, optspec
            in self.optspecs.items()
            })
        self.opts.update(opts)

    def add_subcomponent(
            self,
            component,
            layermap_shorthand: SubcomponentLayermapShorthand = None,
            ):
        """
        Add new component as a subcomponent.
        """
        layermap = parse_subcomponent_layermap_shorthand(
            self.layerspecs.keys(),
            component.layerspecs.keys(),
            layermap_shorthand,
            )

        subcomponent = Subcomponent(
            component,
            layermap,
            )

        # TODO update bbox here?

        self.subcomponents.append(subcomponent)

    def add_subpolygon(
            self,
            polygon,
            layermap: SubpolygonLayermapShorthand = None,
            ):
        """
        Layermap map subcomponent layers to component layers
        """
        layermap_full = parse_subpolygon_layermap_shorthand(
            self.layerspecs.keys(),
            layermap
            )

        subpolygon = Subpolygon(
            polygon,
            layermap_full,
            )

        #self._bbox.add_xyarray(polygon.get_xyarray())

        self.subpolygons.append(subpolygon)

    def add_subpolygons(
            self,
            polys: List[Polygon | PolygonGroup] | Polygon | PolygonGroup,
            layermap: SubpolygonLayermapShorthand = None,
            ):
        """
        Add multiple subpolygons or subpolygon groups.
        """
        if isinstance(polys, Polygon):
            self.add_subpolygon(polys, layermap)

        elif isinstance(polys, PolygonGroup):
            for polygon in polys.get_polygons():
                self.add_subpolygon(polygon, layermap)

        elif isinstance(polys, list | tuple | set):
            # TODO isiterable
            for poly in polys:
                self.add_subpolygons(poly, layermap)

        else:
            raise Exception("Please only pass polygons or polygongroups")

    def get_polygons(self, include_layers=None):
        """
        This should descend into subcomponents and subpolygons recursively,
        applying layermaps and transformations as it goes,
        to get a list of raw polygons in the end.

        returns dict mapping layers to polygons
        layers are same as self.layers

        include_layers is to specify which layers
        are needed, None means all.
        """
        if include_layers is None:
            include_layers = self.layerspecs.keys()
        else:
            assert set(include_layers).issubset(self.layerspecs.keys())

        #layers = {layer: [] for layer in include_layers}
        #for subcomponent in self.subcomponents:
        #    for child_layer, polygons in subcomponent.get_polygons(include_layers).items():
        #        parent_layer = subcomponent.layermap[child_layer]
        #        if parent_layer is None:
        #            continue
        #        layers[parent_layer].extend(polygons)

        layers = {layer: [] for layer in include_layers}
        for subcomponent in self.subcomponents:
            for layer, polygons in subcomponent.get_polygons(include_layers).items():
                for polygon in polygons:
                    polygon.apply_transform(self.transform)
                    layers[layer].append(polygon)

        for subpolygon in self.subpolygons:
            polygon = subpolygon.get_polygon(include_layers)
            if not polygon:
                continue
            polygon.apply_transform(self.transform)
            layers[subpolygon.layermap].append(polygon)

        return layers

    @abstractmethod
    def make(self, opts=None):
        """
        This method should actually generate all subpolygons
        and subcomponents.

        This is an abstract base class,
        so here this method actually does nothing.

        opts allows to pass a custom options list

        Note that make() should work with all default parameters.
        This will actually be used for making the preview image.
        """

    @classmethod
    def parent(cls):
        """
        Return parent class.
        This is a shorthand for cls.__bases__[0]
        """
        return cls.__bases__[0]

    @classmethod
    def is_interface(cls, of: Type[Self] | None = None):
        # TODO make logic more clear
        if cls is Component:
            print("""Base Component class is not an interface.""")
            return False

        if of is Component:
            print("""Base Component class cannot have interfaces""")
            return False

        if of is cls:
            return False

        if of is None:
            if cls.parent() is Component:
                return False
            return True

        else:
            if issubclass(cls, of):
                return True

    @classmethod
    def get_custom_methods(cls):
        """
        Extract custom methods from this component class.
        For example, automatic connection methods
        from CPWs.
        """
        # TODO can interfaces override or pass through
        # custom methods? How would this work?

        # Maybe we need a special decorator
        # for external methods?

        return {
            attr_name: attr
            for attr_name, attr
            in cls.__dict__.items()
            if not attr_name.startswith('_') and inspect.isfunction(attr)
            }

    @classmethod
    def lint(cls):
        """
        Check whether this component class violtates any rules
        """
        if not cls.default_opts.keys() == cls.opt_descriptions.keys():
            print("Options and option descriptions don't match!")

        if len(cls.__bases__) > 1:
            print(
                "Multiple base classes detected. "
                "Please don't use multiple inheritance, "
                "it may seem like a smart choice now, "
                "but you will just hurt yourself in the end. "
                "A wiser approach is encapsulation."
                )

        #if cls.interface_name != Component.interface_name:
        #    # This is an interface
        #    if cls.parent() == Component:
        #        print("Trying to create an interface of Component")

        # Big comment block here where I can jot down any other rules:
        #
        # Interfaces should not add new subcomponents/subpolygons
        #
        #
        #
        #
        # And also for general codestyle:
        #


@dataclass
class Optspec(object):
    """
    Specification of an option:
    includes default value, description, shadow status
    """
    default: Any
    desc: str = ''
    category: OptCategory.OptCategory = field(
        default_factory=lambda: OptCategory.Unspecified,
        )
    # Shadow must be kept last!
    shadow: bool = False

    def get_shadow(self):
        """
        Get shadow version of this optspec
        """
        return Optspec(self.default, self.desc, True)


@dataclass
class Layerspec(object):
    """
    Specification of a layer:
    index, name, fancy name, color1, color2
    """
    fancy_name: str = ''
    #color1: str = ''
    #color2: str = ''
    category: LayerCategory.LayerCategory = field(
        default_factory=lambda: LayerCategory.Unspecified,
        )

    # Index should be kept last
    index: int = -1


def make_opts(parent_class, **kwargs):
    """
    Helper function to generate options and option descriptions
    for a component class.
    You must pass in the parent class
    TODO add example
    """
    optspecs = Dotdict(parent_class.optspecs)
    for name, spec in kwargs.items():
        if spec is Shadow:
            optspecs[name] = parent_class.optspecs[name].get_shadow()
        else:
            if isinstance(spec, dict):
                optspecs[name] = Optspec(**spec)
            else:
                optspecs[name] = Optspec(*spec)

    return optspecs


def make_layers(parent_class, **kwargs):
    """
    """
    layerspecs = Dotdict(parent_class.layerspecs)
    for index, (name, spec) in enumerate(kwargs.items()):
        if isinstance(spec, dict):
            layerspecs[name] = Layerspec(**spec, index=index)
        else:
            layerspecs[name] = Layerspec(*spec, index=index)
    # TODO should we allow overwriting layers of parent?

    return layerspecs


class Subcomponent(object):
    def __init__(self, component, layermap):
        self.component = component
        self.layermap = layermap

    def get_polygons(self, include_layers):
        """
        This is the counterpart to component.get_polygons()
        that applies the correct transformations and everything.

        So basically it's a constant flip-flop between component.get_polygons()
        and subcomponent.get_polygons(), in a sort of tree,
        with the leaves being subpolygons
        """
        include_layers_child = [
            child_layer
            for child_layer, parent_layer in self.layermap.items()
            if parent_layer is not None
            ]

        child_layers = self.component.get_polygons(include_layers_child)
        parent_layers = {
            self.layermap[child_layer_name]: polys
            for child_layer_name, polys in child_layers.items()
            }
        #for polygons in child_layers.values():
        #    for poly in polygons:
        #        poly.apply_transform(self.transform)
        #        # Subpolygon.get_polygon copies
        #        # the polygon, so it's okay
        #        # to transform it in-place here.

        return parent_layers


class Subpolygon(object):
    def __init__(self, polygon, layermap):
        self.polygon = polygon
        self.layermap = layermap
        # ^ this is called a layermap, but
        # really it's just a single string
        # specifying which layer in the parent component
        # will this polygon go to.

    def get_polygon(self, include_layers):
        """
        """
        if self.layermap in include_layers:
            return self.polygon
        return None


def parse_subcomponent_layermap_shorthand(parent_layers, child_layers, layermap_shorthand: SubcomponentLayermapShorthand):
    if layermap_shorthand is None:
        if len(parent_layers) == len(child_layers):
            # Case One: parent and child the same number of layers
            layermap = dict(zip(child_layers, parent_layers))

        elif len(child_layers) == len(parent_layers) == 1:
            # Case Two: parent and child both have one layer
            # (not necessarily same name)
            layermap = {list(child_layers)[0]: list(parent_layers)[0]}
            # (the list() cast is in here just in case someone passes
            # something like a dict_keys object into this function
        else:
            raise Exception(
                "Could not parse None layermap shoarthand"
                )
    elif isinstance(layermap_shorthand, str):
        if len(child_layers) != 1:
            raise Exception(
                "You specified an str layermap shorthand, "
                "but the child component doesn't have "
                "just one layer."
                )

        if layermap_shorthand not in parent_layers:
            raise Exception(
                "You specified an str layermap shorthand, "
                "but that layer is not in the parent component."
                )

        layermap = {list(child_layers)[0]: layermap_shorthand}

    elif isinstance(layermap_shorthand, dict):
        if not set(layermap_shorthand.keys()).issubset(child_layers):
            raise Exception(
                "Layermap keys are not a subset of child component layers"
                )

        if not set(layermap_shorthand.values()).issubset(parent_layers):
            raise Exception(
                "Layermap values are not a subset of parent component layers"
                )

        layermap = layermap_shorthand

    else:
        raise Exception(
            "Layermap shorthand is incorrect type"
            )

    # Pad layermap
    for missing_layer in set(child_layers) - set(layermap):
        layermap[missing_layer] = None

    return layermap


def parse_subpolygon_layermap_shorthand(parent_layers, layermap_shorthand: SubpolygonLayermapShorthand):
    if layermap_shorthand is None:
        if len(parent_layers) == 1:
            return list(parent_layers)[0]
        else:
            raise Exception(
                "You specified a None layermap shorthand, "
                "but the parent component has more than one layer"
                )

    elif isinstance(layermap_shorthand, str):
        if layermap_shorthand in parent_layers:
            return layermap_shorthand
        else:
            raise Exception(
                "There is no such layer in parent component."
                )

    else:
        raise Exception(
            "Layermap shorthand is incorrect type"
            )



