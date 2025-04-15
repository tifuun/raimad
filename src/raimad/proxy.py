"""proxy.py: home to Proxy class and supporting classes."""

from typing import Iterator

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

from copy import copy

import raimad as rai

class LMap:
    """
    LMap: Layer map.

    LMaps tell RAIMAD how the layers of a subcompo map
    to its parent compo.
    An LMap is canonically represented by an LMapShorthand,
    which may be either None, a string, or a dict.

    A None layermap is "transparent":
    the subcompo layers are mapped directly to the parent.
    If the subcompo has layers "foo" and "bar",
    then the parent will have layers "foo" and "bar".

    A string layermap collapses all of the subcompo
    layers to one layer in the parent.
    If the subcompo has layers "foo" and "bar",
    and a layermap of "baz",
    then the parent will have a layer "baz" containing
    the geometries from both "foo" and "bar".

    A dict layermap allows arbitrary layer mapping.
    The keys of the dict correspond to subcompo layers,
    and the values correspond to parent layers

    TODO explain edgecases.
    """

    def __init__(self, shorthand: 'rai.typing.LMapShorthand') -> None:
        self.shorthand = shorthand

    def __getitem__(self, name: str) -> str:
        """Given a child layer, return the parent layer."""
        if self.shorthand is None:
            return name

        if isinstance(self.shorthand, str):
            return self.shorthand

        if isinstance(self.shorthand, dict):
            return self.shorthand[name]

        assert False
    # TODO hacky

    def copy(self) -> Self:
        """Copy this lmap."""
        return type(self)(self.shorthand)

    def compose(self, other: Self) -> Self:
        """
        Merge this lmap with another lmap.

        Parameters
        ----------
        other: Self
            The other lmap

        Returns
        -------
        Self
            Self is returned to allow method chaining.
        """
        if other.shorthand is None:
            # None lmap, pass everything through
            pass

        elif isinstance(other.shorthand, str):
            # single-string lmap, flatten everything to one layer
            self.shorthand = other.shorthand

        elif isinstance(other.shorthand, dict):
            # TODO better way to do this?
            if isinstance(self.shorthand, dict):
                for self_k, self_val in tuple(self.shorthand.items()):
                    try:
                        self.shorthand[self_k] = other[self_val]
                    except KeyError:
                        pass

            elif self.shorthand is None:
                self.shorthand = copy(other.shorthand)

            elif isinstance(self.shorthand, str):
                self.shorthand = other[self.shorthand]

        else:
            assert False

        return self

class ProxiedMarksContainer(
        rai.FilteredDictList[
            'rai.typing.Point',
            'rai.typing.PointLike',
            'rai.typing.BoundPoint',
            ]):
    """
    ProxiedMarksContainer: A MarksContainer seen through a Proxy.

    Unlike a MarksContainer, which returns regular Points,
    this ProxiedMarksContainer returns BoundPoints that
    are bound to a proxy.
    This allows using marks as a reference point for
    transforms,
    for example
    `someproxy.marks.left_corner.rotate(pi)`
    to rotate around the left corner.
    """

    def __init__(
            self,
            proxy: 'rai.typing.Proxy',
            dict_: dict[int | str, 'rai.typing.Point'] | None = None,
            *,
            copy: bool | None = None
            ):
        super().__init__(dict_, copy=copy)
        self._proxy = proxy

    def _filter_set(self, val: 'rai.typing.PointLike') -> 'rai.typing.Point':
        """
        Set filter for markscontainer.

        Make sure that no matter what creature gets passed in
        (regular tuple or boundpoint or whatever),
        what gets stored is a simple regular tuple.
        """
        return (val[0], val[1])

    def _filter_get(self, val: 'rai.typing.Point') -> 'rai.typing.BoundPoint':

        assert not isinstance(val, rai.BoundPoint)
        assert isinstance(val, tuple)
        assert type(val) is tuple
        assert len(val) == 2

        point = self._proxy.transform_point(val)
        boundpoint = rai.BoundPoint(
            point[0],
            point[1],
            self._proxy
            )
        return boundpoint

class Proxy:
    """
    Proxy: transforming and layermapping wrapper around a Compo.

    TODO description here.
    """

    compo: 'rai.typing.CompoLike'

    def __init__(self,
                 compo: 'rai.typing.CompoLike',
                 lmap: 'rai.typing.LMapShorthand' = None,
                 transform: 'rai.typing.Transform | None' = None,
                 _cif_link: bool = False,
                 _autogenned: bool = False,
                 _deepcopied: bool = False,
                 ):
        """
        Create new Proxy.

        Do not instantiate Proxies directly
        unless you have a good reason to.
        Use `Compo.proxy()` instead.

        Parameters
        ----------
        compo
            The compo or proxy that the new proxy will point to
        lmap
            Layer map shorthand for the new proxy
        transform:
            Transformation for the new proxy (None for identity transform)
        """
        self._cif_linked = False
        self._cif_link = _cif_link
        self.autogenned = _autogenned
        self.deepcopied = _deepcopied
        self.compo = compo
        self.lmap = LMap(lmap)
        self.transform = transform or rai.Transform()

    def steamroll(self) -> 'rai.typing.Geoms':
        """
        Get all geometries of this proxy.

        Returns
        -------
        rai.typing.Geoms
            Returns all geometries
            (i.e. all raw geometries as well as subcompos)
            of the CompoLike pointed to by this proxy,
            as seen through this proxy.

        TODO example
        """
        return {
            mapped_layer: [
                self.transform.transform_poly(geom)
                for geom in geoms
                ]
            for layer, geoms
            in self.compo.steamroll().items()
            if (mapped_layer := self.lmap[layer]) is not None
            }

    def get_flat_transform(self, maxdepth: int = -1) -> 'rai.typing.Transform':
        """
        Get flattened transform from tower of proxies.

        Parameters
        ----------
        maxdepth
            Stop at this many proxies. -1 means no limit.

        Returns
        -------
        rai.typing.Transform
            A new transform that is eqiuivalent to applying
            all transform in this proxy tower.
        """
        if maxdepth == 0 or isinstance(self.compo, rai.Compo):
            return self.transform.copy()

        # return (
        #     self.compo.get_flat_transform(maxdepth - 1)
        #     .compose(self.transform)
        #     )

        # TODO huh? copy?
        return self.transform.copy().compose(
            self.compo.get_flat_transform(maxdepth - 1)
            )

    def get_flat_lmap(self, maxdepth: int = -1) -> LMap:
        """
        Get flattened layermap from tower of proxies.

        Parameters
        ----------
        maxdepth
            Stop at this many proxies. -1 means no limit.

        Returns
        -------
        LMap
            A new layermap that is eqiuivalent to applying
            all layermaps in this proxy tower successibely.
        """
        if maxdepth == 0 or isinstance(self.compo, rai.Compo):
            return self.lmap.copy()

        return self.lmap.copy().compose(
            self.compo.get_flat_lmap(maxdepth - 1)
            )

    @property
    def geoms(self) -> 'rai.typing.Geoms':
        """
        Get the raw geometries as seen through this proxy.

        Returns
        -------
        rai.typing.Geoms
            Returns the raw geometries
            (i.e. NOT geometries defined in subcompos)
            defined in the CompoLike pointed to by this Proxy,
            as seen through this proxy.
        """
        return {
            self.lmap[layer]: [
                self.transform.transform_poly(geom)
                for geom in geoms
                ]
            for layer, geoms
            in self.compo.geoms.items()
            }

    @property
    def subcompos(self) -> rai.SubcompoContainer:
        """
        Get subcompos of the CompoLike pointed to by this proxy.

        Returns
        -------
        SubcompoContainer
            A special `SubcompoContainer` is returned
            that is aware that you're looking at it through a proxy,
            so all of the subcompos
            will be wrapped in copies of this proxy.
        """
        new = rai.SubcompoContainer(
            self.final().subcompos._dict,
            copy=False
            )
        #new._proxy = self.deep_copy(_autogenned = True)
        new._proxy = self
        return new
        #return self.compo.subcompos._get_proxy_view(self)

    def final(self) -> 'rai.typing.Compo':
        """
        Return the compo at the bottom of a tower of proxies.

        Returns
        -------
        rai.typing.Compo
            The compo at the bottom of a tower of proxies
        """
        return self.compo.final()

    def final_p(self) -> 'rai.typing.Proxy':
        """
        Return the proxy at the bottom of a tower of proxies.

        Returns
        -------
        rai.typing.Compo
            The proxy at the bottom of a tower of proxies --
            i.e. the second-to-last element in the tower of proxies.
        """
        if isinstance(self.compo, rai.Compo):
            return self
        return self.compo.final_p()

    def depth(self) -> int:
        """
        Measure depth of a tower of proxies.

        Returns
        -------
        int
            0 if called on a compo,
            1 if called on a proxy of a compo,
            2 if called on a proxy of a proxy of a compo,
            and so on.
        """
        return self.compo.depth() + 1

    def descend(self) -> 'Iterator[rai.typing.CompoLike]':
        """
        Descend a tower of proxies to the compo at the bottom.

        Diagram
        -------

        +-------+
        |  self | ----> yield
        +---+---+
            |
            v
        +---+---+
        | proxy | ----> yield
        +---+---+
            |
            v
        +---+---+
        | proxy | ----> yield
        +---+---+
            |
            v
        +---+---+
        | compo | ----> yield
        +-------+

        Yields
        ------
        rai.typing.CompoLike
            Yields all of the proxies in the tower,
            and the compo at the very bottom.
        """
        yield self
        yield from self.compo.descend()

    def descend_p(self) -> 'Iterator[rai.typing.Proxy]':
        """
        Descend a tower of proxies to the lowest proxy.

        Diagram
        -------

        +-------+
        |  self | ----> yield
        +---+---+
            |
            v
        +---+---+
        | proxy | ----> yield
        +---+---+
            |
            v
        +---+---+
        | proxy | ----> yield
        +---+---+
            |
            v
        +---+---+
        | compo | -/--> dont yield
        +-------+

        Yields
        ------
        rai.typing.Proxy
            Yields all of the proxies in the tower,
            but no the compo at the bottom.
        """
        yield self
        yield from self.compo.descend_p()

    def proxy(self) -> 'rai.typing.Proxy':
        """
        Return a new proxy pointing to this proxy.

        Returns
        -------
        rai.typing.Proxy
            The new proxy
        """
        return rai.Proxy(self)

    def walk_hier(self) -> 'Iterator[rai.typing.Proxy]':
        """
        Traverse the subcomponent hierarchy of the CompoLike of this proxy.

        This method will recursively walk through the entire
        subcompo hierarchy of the CompoLike pointed to by
        this proxy.
        Each node is wrapped in a copy of this proxy.
        TODO explain better

        Yields
        ------
        rai.typing.Proxy
            For every subcomponent in the hierarchy,
            a copy of this proxy tower (i.e. self.deep_copy_reassign)
            is returned that points to the subcomponent.

        SeeAlso
        -------
        raimad.Proxy.walk_hier
        """
        # TODO test this?
        for subcompo in self.compo.walk_hier():
            yield self.deep_copy_reassign(subcompo, _autogenned=True)

    def shallow_copy(
            self,
            _autogenned: bool = False,
            _deepcopied: bool = False
            ) -> 'rai.typing.Proxy':
        """
        Make a shallow copy of this proxy.

        This function returns a new proxy that is a copy of this proxy.
        If this proxy points to a different proxy, the target
        proxy is NOT coppied.

        In other words,
        if the current proxy is a proxy tower,
        only the topmost proxy is copied.

        Diagram
        -------

        +-------+        .----. 
        |  self | ----> | copy | <-- this is returned
        +---+---+        '--+-' 
            |               |
            |  .-----------' 
            | |
            v v
        +---+---+
        | proxy |
        +---+---+
            |
            v
        +---+---+
        | proxy |
        +---+---+
            |
            v
        +---+---+
        | compo |
        +-------+

        Returns
        -------
        rai.typing.Proxy
            Copy of this proxy

        SeeAlso
        -------
        self.shallow_copy_reassign,
        self.deep_copy,
        self.deep_copy_reassign
        """
        return type(self)(
            self.compo,
            self.lmap.shorthand,
            self.transform.copy(),
            _autogenned=_autogenned,
            _deepcopied=_deepcopied
            )

    def shallow_copy_reassign(
            self,
            new_compo: 'rai.typing.CompoLike',
            _autogenned: bool = False,
            _deepcopied: bool = False,
            ) -> 'rai.typing.Proxy':
        """
        Make a shallow copy of this proxy and reassign to a new CompoLike.

        This function returns a new proxy that is a copy of this proxy,
        but reassigned to `new_compo`.

        if the current proxy is a proxy tower,
        the proxies below this one are esentially ignored.
        The returned proxy is always pointing directly to `new_compo`,
        and the layermap and transform is exactly the same
        as this proxy.

        Diagram
        -------

        +-------+        .----. 
        |  self | ----> | copy | <-- this is returned
        +---+---+        '--+-' 
            |               |               
            v               |               
        +---+---+           |               
        | proxy |           |             
        +---+---+           |              
            |               |                
            v               |            
        +---+---+           |             
        | proxy |           |             
        +---+---+           |              
            |               |               
            v               v               
        +---+---+      +----+------+
        | compo |      | new_compo |
        +-------+      +-----------+

        Returns
        -------
        rai.typing.Proxy
            Copy of this proxy reassigned to `new_compo`

        SeeAlso
        -------
        self.shallow_copy,
        self.deep_copy,
        self.deep_copy_reassign
        """
        return type(self)(
            new_compo,
            self.lmap.shorthand,
            self.transform.copy(),
            _autogenned=_autogenned,
            _deepcopied=_deepcopied
            )

    def deep_copy(
            self,
            _autogenned: bool = False,
            ) -> 'rai.typing.Proxy':
        """
        Make a deep copy of this proxy.

        If this proxy is pointing directly to a compo,
        then this method is identical to `self.shallow_copy`.
        If, however, this proxy is a proxy tower,
        then all of the proxies in the tower are copied.

        Returns
        -------
        rai.typing.Proxy
            Deep copy of this proxy


        Diagram
        -------

        +-------+        .----. 
        |  self | ----> | copy | <-- this is returned
        +---+---+        '--+-' 
            |               |                        
            v               v                        
        +---+---+        .--+--.                     
        | proxy | ----> | copy  |                  
        +---+---+        '--+--'                    
            |               |                         
            v               v                     
        +---+---+        .--+--.                   
        | proxy | ----> | copy  |                  
        +---+---+        '--+--'                    
            |               |                        
            |  .-----------'                         
            | |                                       
            v v                                      
        +---+-+-+                   
        | compo |                   
        +-------+                   

        SeeAlso
        -------
        self.shallow_copy,
        self.shallow_copy_reassign,
        self.deep_copy_reassign
        """

        if isinstance(self.compo, rai.Compo):
            return self.shallow_copy(
                _autogenned=_autogenned,
                _deepcopied=True,
                )

        elif isinstance(self.compo, rai.Proxy):
            return self.shallow_copy_reassign(
                self.compo.deep_copy(
                    _autogenned = _autogenned,
                    ),
                _autogenned=_autogenned,
                _deepcopied=True
                )

        else:
            assert False

    def deep_copy_reassign(
            self,
            new_compo: 'rai.typing.CompoLike',
            _autogenned: bool = False,
            _deepcopied: bool = False,
            ) -> 'rai.typing.Proxy':
        """
        Make a deep copy of this proxy and reassign to `new_compo`.

        If this proxy is pointing directly to a compo,
        then this method is identical to `self.shallow_copy_reassign`.
        If, however, this proxy is a proxy tower,
        then all of the proxies in the tower are copied,
        and the bottom-most proxy is reassigned to `new_compo`.

        Diagram
        -------

        +-------+        .----. 
        |  self | ----> | copy | <-- this is returned
        +---+---+        '--+-' 
            |               |                        
            v               v                        
        +---+---+        .--+--.                     
        | proxy | ----> | copy  |                  
        +---+---+        '--+--'                    
            |               |                         
            v               v                     
        +---+---+        .--+--.                   
        | proxy | ----> | copy  |                  
        +---+---+        '--+--'                    
            |               |                        
            +               |                        
            |               |                        
            v               v                        
        +---+---+      +----+------+
        | compo |      | new_compo |
        +-------+      +-----------+

        Returns
        -------
        rai.typing.Proxy
            Deep copy of this proxy reassigned to `new_compo`.

        SeeAlso
        -------
        self.shallow_copy,
        self.shallow_copy_reassign,
        self.deep_copy
        """

        if isinstance(self.compo, rai.Compo):
            return self.shallow_copy_reassign(
                new_compo,
                _autogenned=_autogenned,
                _deepcopied=_deepcopied,
                )

        elif isinstance(self.compo, rai.Proxy):
            return self.shallow_copy_reassign(
                self.compo.deep_copy_reassign(
                    new_compo,
                    _autogenned=_autogenned,
                    _deepcopied=True,
                    ),
                _autogenned=_autogenned,
                _deepcopied=_deepcopied,
                )

        else:
            assert False

    def transform_point(
            self,
            point: 'rai.typing.PointLike'
            ) -> 'rai.typing.PointLike':
        """
        Apply this proxies transform to a point, return the transformed point.

        A Point (tuple of two floats) is always returned,
        even if a BoundPoint is passed in.

        Parameters
        ----------
        point : rai.typing.PointLike
            The point to transform.

        Returns
        -------
        rai.typing.Point
            The transformed point.
        """
        return self.transform.transform_point(
            self.compo.transform_point(point)
            )

    def _str(self, depth: int = 0) -> str:
        """
        Return string representation of proxy.

        Returns
        -------
        str
            TODO example string
        """
        # FIXME refactor this spaghetti
        return ''.join((
            '<' * (depth == 0),
            '\t' * depth,
            'Automatic' if self.autogenned else 'Manual',
            ' deepcopied' * self.deepcopied,
            f" Proxy at {rai.wingdingify(id(self))} ",
            f"with {str(self.transform)} ",
            "of\n",
            f"{self.compo._str(depth=1)}",
            '>' * (depth == 0)
            ))

    def __str__(self) -> str:
        """
        Return string representation of proxy.

        Returns
        -------
        str
            TODO example string
        """
        return self._str()

        #stack = ''.join([
        #    'ma'[proxy.autogenned]
        #    for proxy in self.descend_p()
        #    ])
        #return (
        #    "<"
        #    f"Proxy of {self.final()} at {rai.wingdingify(id(self))} "
        #    f"stack `{stack}x`"
        #    ">"
        #    )

    def __repr__(self) -> str:
        """
        Return string representation of proxy.

        Returns
        -------
        str
            TODO example string
        """
        return self.__str__()

    # Transform functions #
    # TODO for all transforms
    # TODO same implementation as in Compo
    # TODO stack another transform or modify self?
    def scale(self, x: float, y: float | None = None) -> Self:
        """
        Scale this proxy.

        Parameters
        ----------
        x : float
            Factor to scale by along the x axis
        y : float
            Factor to scale by along the y axis.
            If unspecified or None,
            use the x scale factor.

        Returns
        -------
        Self
            self is returned to allow chaining methods.
        """
        self.transform.scale(x, y)
        return self

    def movex(self, factor: float) -> Self:
        """
        Move this proxy horizontally.

        Parameters
        ----------
        x : float
            Move this many units along x axis.

        Returns
        -------
        Self
            self is returned to allow chaining methods.
        """
        self.transform.movex(factor)
        return self

    def movey(self, factor: float) -> Self:
        """
        Move this proxy vertically.

        Parameters
        ----------
        y : float
            Move this many units along y axis.

        Returns
        -------
        Self
            self is returned to allow chaining methods.
        """
        self.transform.movey(factor)
        return self

    def move(self, x: float, y: float) -> Self:
        """
        Move this proxy.

        Parameters
        ----------
        x : float
            Move this many units along x axis.
        y : float
            Move this many units along y axis.

        Returns
        -------
        Self
            self is returned to allow chaining methods.
        """
        self.transform.move(x, y)
        return self

    def hflip(self, x: float = 0) -> Self:
        """
        Flip (mirror) along horizontal axis.

        Parameters
        ----------
        x : float
            Flip around this horizontal line (x coordinate)

        Returns
        -------
        Self
            self is returned to allow chaining methods.
        """
        self.transform.hflip(x)
        return self

    def vflip(self, y: float = 0) -> Self:
        """
        Flip (mirror) along vertical axis.

        Parameters
        ----------
        y : float
            Flip around this vertical line (y coordinate)

        Returns
        -------
        Self
            self is returned to allow chaining methods.
        """
        self.transform.vflip(y)
        return self

    def flip(self, x: float = 0, y: float = 0) -> Self:
        """
        Flip (mirror) along both horizontal and vertical axis.

        Parameters
        ----------
        x : float
            Flip around this point (x coordinate). Default: origin
        y : float
            Flip around this point (y coordinate). Default: origin

        Returns
        -------
        Self
            self is returned to allow chaining methods.
        """
        self.transform.flip(x, y)
        return self

    def rotate(self, angle: float, x: float = 0, y: float = 0) -> Self:
        """
        Rotate this proxy, possibly around a point.

        Parameters
        ----------
        angle : float
            Rotate by this many radians in the positive orientation
        x : float
            Rotate around this point (x coord). Default: origin
        y : float
            Rotate around this point (y coord). Default: origin

        Returns
        -------
        Self
            self is returned to allow method chaining.
        """
        self.transform.rotate(angle, x, y)
        return self

    def map(self, lmap_shorthand: 'rai.typing.LMapShorthand') -> Self:
        """
        Apply a layermap shorthand to a proxy.

        Parameters
        ----------
        lmap_shorthand
            The layermap shorthand to apply

        Returns
        -------
        Self
            self is returned to allow method chaining.

        Examples
        --------
        TODO examples

        SeeAlso
        -------
        TODO link to doc page
        """

        self.lmap = LMap(lmap_shorthand)
        return self

    @property
    def marks(self) -> ProxiedMarksContainer:
        """
        Get the marks of the CompoLike pointed to by this proxy.

        Returns
        -------
        ProxiedMarksContainer
            A special `ProxiesMarksContainer` is returned
            which can be used to query the underlying CompoLike's
            marks as seen through this proxy.
        """
        return ProxiedMarksContainer(
            self,
            self.compo.marks._dict,
            copy=False
            )

    # bbox functions #
    # TODO same as compo -- some sort of reuse?
    @property
    def bbox(self) -> 'rai.BoundBBox':
        """
        Get a BoundBBox pointing to this proxy.

        Returns
        -------
        rai.BoundBBox
            A BoundBBox pointing to this proxy

        Examples
        --------
        TODO examples

        SeeAlso
        -------
        TODO doc page link
        """
        bbox = rai.BoundBBox(proxy=self)
        for geoms in self.steamroll().values():
            for geom in geoms:
                bbox.add_poly(geom)
        return bbox

    # snapping functions #
    def snap_left(self, target: Self) -> Self:
        """
        Move this proxy so its bbox is to the left of the target proxy.

        Diagram
        -------
         ________
        |        |
        |        |________
        |        |        |
        |  self  | target |
        |        |________|
        |        |
        |________|

        Parameters
        ----------
        The target proxy

        Returns
        -------
        Self
            This proxy is returned to allow method chaining.
        """
        self.bbox.mid_right.to(target.bbox.mid_left)
        return self

    def snap_right(self, target: Self) -> Self:
        """
        Move this proxy so its bbox is to the right of the target proxy.

        Diagram
        -------
                  ________
                 |        |
         ________|        |
        |        |        |
        | target |  self  |
        |________|        |
                 |        |
                 |________|

        Parameters
        ----------
        The target proxy

        Returns
        -------
        Self
            This proxy is returned to allow method chaining.
        """
        self.bbox.mid_left.to(target.bbox.mid_right)
        return self

    def snap_above(self, target: Self) -> Self:
        """
        Move this proxy so its bbox is directly above the target proxy.

        Diagram
        -------
         ________________ 
        |                |
        |      self      |
        |________________|
            |        |
            | target |
            |________|

        Parameters
        ----------
        The target proxy

        Returns
        -------
        Self
            This proxy is returned to allow method chaining.
        """
        self.bbox.bot_mid.to(target.bbox.top_mid)
        return self

    # TODO target should be CompoLike not Proxy, Right??
    def snap_below(self, target: Self) -> Self:
        """
        Move this proxy so its bbox is directly below the target proxy.

        Diagram
        -------
             ________ 
            |        |
            | target |
         ___|________|___ 
        |                |
        |      self      |
        |________________|

        Parameters
        ----------
        The target proxy

        Returns
        -------
        Self
            This proxy is returned to allow method chaining.
        """
        self.bbox.top_mid.to(target.bbox.bot_mid)
        return self

    def _repr_svg_(self) -> str:
        """
        Make svg representation of component.

        This is not an official magic method specified by Python,
        but rather a convention used by Jupyter Notebook
        and related tools.
        We also use it in RAIMARK.

        Returns
        -------
        str
            String containing SVG representation of component.

        SeeAlso
        -------
        rai.export_svg
        rai.Compo._export_svg_
        """
        return rai.export_svg(self)

