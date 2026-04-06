import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation, TriContourSet
from matplotlib.layout_engine import LayoutEngine
from matplotlib.text import Text
from matplotlib.cm import ScalarMappable
from matplotlib.lines import Line2D
from matplotlib.collections import PathCollection
from matplotlib.contour import QuadContourSet
from matplotlib.container import BarContainer
from matplotlib.patches import Polygon
from matplotlib.colorbar import Colorbar
import numpy as np
from numpy.typing import ArrayLike
from abc import ABCMeta
from typing import overload
import os

__all__ = ["MPL_Figure"]

class _vispipe_backend_api(metaclass=ABCMeta): ...

class MPL_Figure(_vispipe_backend_api):
    def __init__(
        self,
        id: int | str | None = None,
        fig: plt.Figure | None = None,
        ax: plt.Axes | None = None,
        subplots: tuple[int, int] | None = None,
        title: str | None = None,
        layout: str | LayoutEngine | None = "compressed",
        figsize: tuple[float, float] | None = None,
        subplots_kw: dict = {},
        legend: bool | dict = False,
    ) -> None: ...
    @property
    def figure(self) -> plt.Figure: ...
    @property
    def subfigs(self) -> np.ndarray: ...
    def __getitem__(self, index): ...
    def __iter__(self): ...
    def __next__(self): ...
    def gca(self) -> plt.Axes: ...
    def sca(self, ax: plt.Axes): ...
    def return_fig(self) -> tuple[plt.Figure, np.ndarray]: ...
    def get_title(self) -> str: ...
    def set_title(self, t: str, **kwargs) -> Text: ...
    def get_subtitle(self, ax: plt.Axes | None = None) -> str: ...
    def set_subtitle(
        self,
        label: str,
        loc: str | None = None,
        pad: float | None = None,
        *,
        y: float | None = None,
        ax: plt.Axes | None = None,
        **kwargs,
    ) -> Text: ...
    def get_xlabel(self, ax: plt.Axes | None = None) -> str: ...
    def set_xlabel(
        self,
        xlabel: str | None = None,
        labelpad: float | None = None,
        *,
        loc: str | None = None,
        ax: plt.Axes | None = None,
        **kwargs,
    ) -> Text: ...
    def get_ylabel(self, ax: plt.Axes | None = None, **kwargs) -> str: ...
    def set_ylabel(
        self,
        ylabel: str | None = None,
        labelpad: float | None = None,
        *,
        loc: str | None = None,
        ax: plt.Axes | None = None,
        **kwargs,
    ) -> Text: ...
    def set_xticks(
        self,
        xticks: ArrayLike,
        labels: list[str] | None = None,
        *,
        minor: bool = False,
        ax: plt.Axes | None = None,
        **kwargs,
    ): ...
    def set_yticks(
        self,
        yticks: ArrayLike,
        labels: list[str] | None = None,
        *,
        minor: bool = False,
        ax: plt.Axes | None = None,
        **kwargs,
    ): ...
    def set_aspect(
        self,
        aspect: str | float,
        adjustable: str | None = None,
        anchor: str | tuple[float, float] | None = None,
        share: bool = False,
        ax: plt.Axes | None = None,
    ): ...
    def set_grid(
        self,
        visible: bool | None = None,
        which: str = "major",
        axis: str = "both",
        ax: plt.Axes | None = None,
        **kwargs,
    ): ...
    def get_bbox(
        self, ax: plt.Axes | None = None
    ) -> tuple[float, float, float, float]: ...
    def set_bbox(
        self,
        bbox: tuple[float, float, float, float],
        ax: plt.Axes | None = None,
        **kwargs,
    ): ...
    def set(self, ax: plt.Axes | None = None, **plot_kw): ...
    def link_subplots(
        self,
        ax1: plt.Axes,
        *ax2: plt.Axes,
        sharex: bool = True,
        sharey: bool = True,
        **kwargs,
    ): ...
    def line(
        self,
        points: np.ndarray,
        *args,
        T: bool = True,
        ax: plt.Axes | None = None,
        **linekwargs,
    ) -> list[Line2D]: ...
    def scatter(
        self,
        points: np.ndarray,
        *args,
        T: bool = True,
        ax: plt.Axes | None = None,
        **scatterkwargs,
    ) -> PathCollection: ...
    @overload
    def triplot(
        self,
        nodes: np.ndarray,
        elemcomps: np.ndarray,
        ax: plt.Axes | None = None,
        bbox: tuple[float, float, float, float] | None = None,
        **trikwargs,
    ) -> tuple[Line2D, Line2D]: ...
    @overload
    def triplot(
        self,
        mesh: Triangulation,
        ax: plt.Axes | None = None,
        bbox: tuple[float, float, float, float] | None = None,
        **trikwargs,
    ) -> tuple[Line2D, Line2D]: ...
    def contour(
        self,
        vals: np.ndarray,
        mesh: np.ndarray,
        ax: plt.Axes | None = None,
        bbox: tuple[float, float, float, float] | None = None,
        fill: bool = True,
        limits: tuple[float, float] | None = None,
        levels: int = 101,
        **conkwargs,
    ) -> QuadContourSet: ...
    @overload
    def tricontour(
        self,
        vals: np.ndarray,
        nodes: np.ndarray,
        elemcomps: np.ndarray,
        limits: tuple[float, float] | None = None,
        levels: int = 101,
        ax: plt.Axes | None = None,
        bbox: tuple[float, float, float, float] | None = None,
        fillval: float | None = None,
        fill: bool = True,
        **triconkwargs,
    ) -> TriContourSet: ...
    @overload
    def tricontour(
        self,
        vals: np.ndarray,
        mesh: Triangulation,
        limits: tuple[float, float] | None = None,
        levels: int = 101,
        ax: plt.Axes | None = None,
        bbox: tuple[float, float, float, float] | None = None,
        fillval: float | None = None,
        fill: bool = True,
        **triconkwargs,
    ) -> TriContourSet: ...
    def hist(
        self,
        vals,
        bins,
        cmap: str | None = None,
        ax: plt.Axes | None = None,
        valsrange: tuple[float, float] | None = None,
        fillval: float = -99999,
        **histkwargs,
    ) -> tuple[
        np.ndarray | list[np.ndarray], np.ndarray, BarContainer | list[Polygon]
    ]: ...
    def cbar(
        self,
        mapable: ScalarMappable,
        cax: plt.Axes | None = None,
        ax: plt.Axes | None = None,
        label: str | None = None,
        label_kwargs: dict = {},
        **colorbarkwargs,
    ) -> Colorbar: ...
    def savefig(self, path: str | os.PathLike, dpi: int | None = None): ...
