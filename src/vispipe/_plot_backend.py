import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.tri import Triangulation
import numpy as np
from ._gridedit import meshgridcut,tri_bbox_prep
import numpy as np


#[ ] Clean up inputs
__all__=["_MPL_Figure"]
class _MPL_Figure():
    def __init__(self,
    id,
    fig=None,
    ax=None,
    subplots=None,
    title=None,
    layout="compressed",
    figsize=None,
    subplots_kw={}) -> None:
        self._id=id
        if ax is None and not fig:
            fig,ax=plt.subplots(*(subplots if subplots else (1,1)),figsize=figsize,**subplots_kw)

        self._fig=fig
        if isinstance(ax,np.ndarray):
            self._ax=ax.flatten() 
        elif isinstance(ax,mpl.axes.Axes):
            self._ax=np.array([ax])
        elif hasattr(ax,"__init__"):
            self._ax=np.asarray(ax)
        else:
            raise AttributeError("self._ax could not be set.")
        
        self._current_ax=self._ax[0]
        
        self._subplots=subplots
        self._title=title
        self._layout=layout
        self._figsize=figsize
        self._bbox=None
        if title: self._fig.suptitle(title)
        fig.set_layout_engine(layout)

    

    @property
    def figure(self): return self._fig

    @property
    def subfigs(self): return self._ax
    
    def __getitem__(self,index):
        return self._ax[index]
    def __iter__(self):
        self._pos=-1
        self._stop=len(self._ax)-1
        return self
    def __next__(self):
        if self._pos == self._stop:
            raise StopIteration
        self._pos+=1
        return self._ax[self._pos]

    def gca(self):
        return self._current_ax
    
    def sca(self,ax):
        self._current_ax=ax
        plt.sca(ax)

    def return_fig(self):
        return self._fig,self._ax
    
    def get_title(self):
        return self._fig._suptitle.get_text()

    def set_title(self,t,**kwargs):
        return self._fig.suptitle(t,**kwargs)
    
    def get_subtitle(self,ax=None):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
        
        return ax.get_title()

    def set_subtitle(self,label,fontdict=None,loc=None,pad=None,*,y=None,ax=None,**kwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)

        return ax.set_title(label,fontdict,loc,pad,y=y,**kwargs)
    
    def get_xlabel(self,ax=None):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
            
        return ax.xaxis.get_label()

    def set_xlabel(self,xlabel,fontdict=None,labelpad=None,*,loc=None,ax=None,**kwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
        
        ax.set_xlabel(xlabel,fontdict,labelpad,loc=loc,**kwargs)
    
    def get_ylabel(self,ax=None,**kwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
            
        return ax.yaxis.get_label()

    def set_ylabel(self,ylabel,fontdict=None,labelpad=None,*,loc=None,ax=None,**kwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
        
        ax.set_ylabel(ylabel,fontdict,labelpad,loc=loc,**kwargs)

    def set_xticks(self,xticks,labels=None,*,minor=False,ax=None,**kwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
        
        ax.set_xticks(xticks,labels,minor=minor,**kwargs)

    
    def set_yticks(self,yticks,labels=None,*,minor=False,ax=None,**kwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
        
        ax.set_yticks(yticks,labels,minor=minor,**kwargs)


    def set_aspect(self,aspect,adjustable=None,anchor=None,share=False,ax=None):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)

        ax.set_aspect(aspect,adjustable,anchor,share)

        
    def set_grid(self,visible=None,which='major',axis='both',ax=None,**kwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
        
        ax.grid(visible,which,axis,**kwargs)

    def get_bbox(self,ax=None):
        if self._bbox:
            return self._bbox
        else:
            if ax is None: ax=self.gca()
            xlim=ax.get_xlim()
            ylim=ax.get_ylim()
            return (xlim[0],ylim[0],xlim[1],ylim[1])
        
    def set_bbox(self,bbox,ax=None,**kwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
        
        ax.set(xlim=(bbox[0],bbox[2]),ylim=(bbox[1],bbox[3]))

    def set(self,ax=None,**plot_kw):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
        ax.set(**plot_kw)

    def link_subplots(self,ax1,*ax2,sharex=True,sharey=True,**kwargs):
        if ax2 is None:
            parent_ax:plt.Axes=self.gca()
            child_axs=(ax1,)
        else:
            parent_ax=ax1
            child_axs=ax2

        for ax in child_axs:
            if sharex: ax1._shared_axes["x"].join(parent_ax,ax)
            if sharey: ax1._shared_axes["y"].join(parent_ax,ax)
            #if sharex: parent_ax.sharex(ax,**{key:(val if key not in sharex_kw else sharex_kw[key]) for key,val in kwargs.items()})
            #if sharey: parent_ax.sharey(ax,**{key:(val if key not in sharey_kw else sharey_kw[key]) for key,val in kwargs.items()})
            #parent_ax=ax
            
    #[ ]Utilize bbox's to trim all data types.
    def line(self,points,ax=None,**linekwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)

        if len(points)>2:
            points=points.T
        return ax.plot(*points,**linekwargs)
    
    def scatter(self,points,ax=None,**scatterkwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)

        if len(points)>2:
            points=points.T
        return ax.scatter(*points,**scatterkwargs)

    #[ ] def line3d():

    def triplot(self,*meshdata,ax=None,bbox=None,**trikwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
        if bbox is None: bbox=self._bbox
        
        if not isinstance(meshdata[0],Triangulation):
            mesh=Triangulation(meshdata[0][:,0],meshdata[0][:,1],meshdata[1])
        else:
            mesh=meshdata[0]
            
        if np.any(bbox):
            mesh=tri_bbox_prep(mesh,bbox)

        return ax.triplot(mesh,**trikwargs)
    
    #[ ] Decht this
    def contour(self,vals,mesh,ax=None,bbox=None,fill=True,limits=None,levels=101,**conkwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
        if bbox is None: bbox=self._bbox
            
        if np.any(bbox):
            mesh,vals=meshgridcut(mesh,bbox,vals=vals)

        if "levels" not in conkwargs:
            low=np.min(vals)
            high=np.max(vals)
            levels=np.linspace(low,high,101,endpoint=True)
        else:
            levels=conkwargs.pop("levels")
        conkwargs.pop("fillval",None)
        #Creates the filled contour to be plotted.
        if fill: 
            cm=ax.contourf(mesh[0],mesh[1],vals,levels=levels,**conkwargs)
            #conlabel=False
        else: cm=ax.contour(mesh[0],mesh[1],vals,levels=levels,**conkwargs)

        return cm
    
    #[ ] Decht this
    def tricontour(self,vals,*meshdata,limits=None,levels=101,ax=None,bbox=None,fillval=None,fill=True,**triconkwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
        if bbox is None: bbox=self._bbox

        if not isinstance(meshdata[0],Triangulation):
            mesh=Triangulation(meshdata[0][:,0],meshdata[0][:,1],meshdata[1])
        else:
            mesh=meshdata[0]
        
        if np.any(bbox):
            mesh,valsstats=tri_bbox_prep(mesh,bbox,vals=vals)
            valsstats=valsstats[valsstats!=fillval]
        else:
            valsstats=vals[vals!=fillval]
        if not limits:
            low=np.min(valsstats)
            high=np.max(valsstats)
            mesh.set_mask(np.all(np.isin(mesh.triangles,np.asarray(vals==fillval).nonzero()),axis=1))
        else:
            low=limits[0]
            high=limits[1]
        levels=np.linspace(low,high,levels,endpoint=True)
        #Creates the filled contour to be plotted.
        if fill: cm=ax.tricontourf(mesh,vals,levels=levels,**triconkwargs)
        else: cm=ax.tricontour(mesh,vals,levels=levels,**triconkwargs)

        return cm

    def hist(self,vals,bins,cmap=None,ax=None,bbox=None,valsrange=None,fillval=-99999,**histkwargs):
        if ax is None:
            ax=self.gca()
        else:
            self.sca(ax)
        if bbox is None: bbox=self._bbox
        if valsrange:
            vals=vals[vals>=valsrange[0]]
            vals=vals[vals<=valsrange[1]]
        n,bins,patches=ax.hist(vals[vals!=fillval],bins,**histkwargs)

        if cmap:
            frac=n.size
            cmap=plt.get_cmap(cmap)

            for f,patch in enumerate(patches):
                patch.set_facecolor(cmap(f/frac))

        return (n,bins,patches)
    
    def cbar(self,mapable,cax=None,ax=None,label=None,label_kwargs={},**colorbarkwargs):
        if ax is None:
            ax=self.gca()
        elif isinstance(ax,np.ndarray):
            self.sca(ax[0])
        else:
            self.sca(ax)
        cbar=plt.colorbar(mapable,cax=cax,ax=ax,**colorbarkwargs)
        if label: cbar.ax.set_ylabel(label,**{**{"rotation":90,"labelpad":18},**label_kwargs})
        
    def show(self,*args,**kwargs):

        if self._legend_kw:
            for axn in self._ax:
                if not axn.get_legend_handles_labels() == ([], []):
                    axn.legend(**self._legend_kw if isinstance(self._legend_kw,dict) else {})
            
        plt.show(*args,**kwargs)

    #[x] Make save
    def savefig(self,path,dpi=None):
        self._fig.set_dpi(dpi)
        return self._fig.savefig(path,dpi=dpi)

