from copy import deepcopy
from multiprocessing import Pool
from pint import UnitRegistry
import matplotlib.pyplot as plt
import numpy as np
import os,shutil,json,fitz,logging
import importlib
from meshtools.plotters import stattable
from ._plot_backend import _MPL_Figure


__all__=["vispipe"]

def _get_settings(*settings):
    _vp_settings={
        "dpi":500,
        "resolution":(3840,2160),
        "plot_api":_MPL_Figure
    }

    return tuple(_vp_settings.get(setting) for setting in settings)

#[x] Rough workflow: for keys in config["plots"]: global_settings.update(provided_settings.update(config["global"].update(config["plots"])))
#[ ] Start with multiplot be in serial then figure out how to get procs to comunicate.
#[ ] lru_cache for vals that have been read already.
#[ ] make better logger
#[ ] Look at righting a mesh reader for stwave and use valonly=True when doing the main read.
    #[x] make mesh reader 
    #[ ] mesh reader for stwave and use valonly=True
    #[ ] change vispipe to handle multiple grids
    
#Writes the individule .pngs to a .pdf page.
def _writepdf(pngpath,width,height):
    file=fitz.open()
    #width and height are in pixels.
    page=file.new_page(width=width,height=height)
    page.insert_image([0,0,width,height], filename=pngpath)
    pdfname=pngpath.split("/")[-1][:-4]
    file.save(os.path.join(os.path.dirname(os.path.dirname(pngpath)),f"pages/{pdfname}.pdf"))

#Creates the main pdf from the indiviual pdfs.
def _orderpdf(title):
    pages=os.listdir(os.path.join(os.path.dirname(title),"pages"))
    pages=sorted([float(i[:-4]) for i in pages])
    doc=fitz.open()
    for page in pages:
        file=fitz.open(os.path.join(os.path.dirname(title),f"pages/{page}.pdf"))
        doc.insert_pdf(file)
    doc.save(f"{title}")

def _getfunc(plm):
    func=getattr(importlib.import_module(".".join((readlist:=plm.split("."))[:-1])),readlist[-1])
    return func

def _merge_func_setting(high,low,key,library={}):
    if isinstance(high[key],str):
        high[key]={"name":high[key]}
        high[key].update(library.get(high[key]["name"],{}))

    #[ ] test if a base can have a str name plotter                
    if "name" not in high[key]:
        high[key]={**low[key],**high[key]}
        high[key]["kwargs"]={**low[key].get("kwargs",{}),**high[key].get("kwargs",{})}

    elif key in low and low[key]["name"]==high[key]["name"]:
        high[key]={**low[key],**high[key]}
        high[key]["kwargs"]={**low[key].get("kwargs",{}),**high[key].get("kwargs",{})}
    
    return high[key]

def _read_sig(plotter,vals,kwargs,plotargs,plotkwargs,locals,recnumber):
    plotsig=plotter.pop("sig")
    exclusive=plotsig.pop("exclusive",False)
    par=()
    pkw={}
    for key in plotkwargs:
        plotsig.pop(key,None)

    addargs="vp:plotargs" not in plotsig and "plotargs" in plotter 
    for key,item in plotsig.copy().items():
        
        if "*" in key:
            if "**" in key: break
            del plotsig[key]
            if item is not None:
                par+=vals[int(item)] if "vp:" not in str(item) else tuple(kwargs.pop(item[3:],locals.get(item[3:])))
            break
        del plotsig[key]

        if str(item).isdigit():
            item=vals[int(item)]
            if key=="rec" and recnumber is not None: item=item[recnumber]
            par+=(item,)
            continue
        elif isinstance(item,list):
            par+=tuple(vals[int(i)] if "vp:" not in str(i) else kwargs.pop(i[3:],locals.get(item[3:])) for i in item)
            continue
        elif isinstance(item,str) and "vp:" in item:
            item=kwargs.pop(item[3:],locals.get(item[3:]))
            if key=="rec" and recnumber is not None: item=item[recnumber]
            par+=(item,)
            continue
    
    plotargs=par+(plotargs if addargs else ())
    
    for key,item in plotsig.items():
        if "**" in key:
            if item is not None and item!="vp:plotkwargs":
                pkw.update(vals[int(item)] if "vp:" not in str(item) else tuple(kwargs.pop(item[3:],locals.get(item[3:]))))
            elif item=="vp:plotkwargs":
                plotkwargs={**pkw, **plotkwargs}
                break
            else:
                break
        if str(item).isdigit(): 
            pkw[key]=vals[int(item)]
            continue
        elif isinstance(item,list):
            pkw[key]=tuple(vals[int(i)] if "vp:" not in str(i) else kwargs.pop(i[3:],locals.get(item[3:])) for i in item)
            continue
        elif isinstance(item,str) and "vp:" in item:
            pkw[key]=kwargs.pop(item[3:],locals.get(item[3:]))
            continue
    else:
        plotkwargs={**pkw, **plotkwargs}
    if not exclusive:
        plotkwargs.update(kwargs)
    
    return plotargs,plotkwargs
            

#pipeline handes all operations associated with individual plots. 
def _pipeline(kwargs):
    try:
        dpi,(width,height),plot_api=_get_settings("dpi","resolution","plot_api")
        plt.set_loglevel("warning")
        logging.basicConfig(format='%(levelname)s: %(message)s',level=kwargs.pop("loglevel"))
        if "type" in kwargs: del kwargs["type"]
        reader=kwargs.pop("reader",None)
        path=kwargs.pop("path",None)
        pagenumber=kwargs.pop("pagenumber",None)
        recnumber=kwargs.pop("recnumber",None)
        
        plotter=kwargs.pop("plotter",None)
        savedir=kwargs.pop("savedir",None)
        pdf=kwargs.pop("pdf",None)
        useback=not kwargs.pop("no_back",False)

        loggingsuffix=f"\n\tfile={path}\n\tfig={pagenumber}\n"
        logging.info(f"Preparing plot for fig {pagenumber}")

        #Checks for a reader and the assigns vals to be plotted.
        #[ ] Redo 
        if reader:   
            logging.debug("Reading in vals.")     
            readfunc=_getfunc(reader["name"])
            readargs=reader.pop("args",())
            readkwargs=reader.pop("kwargs",{})
            vals=readfunc(path,*readargs,**readkwargs)
            #if not kwargs.get("mesh"):
            #    kwargs["mesh"]=(vals[1],)
            #    if kwargs.get("table"): kwargs["datadims"]=vals[2]
            #    vals=vals[0]
            #    reqnum=str(pagenumber).split(".")[-1]
            #    vals=vals[int(reqnum)]
            logging.debug(f"Fig {pagenumber} vals read.")
        else:
            vals=kwargs.pop("vals")
            kwargs.pop("meshtype",None)


        #Checks if the unit needs to be changed.
        try:
            if kwargs.get("defunit") and kwargs["unit"]!=kwargs.get("defunit") and kwargs.get("mesh"):
                logging.debug(f"Converting unit from {kwargs.get('defunit')} to {kwargs['unit']} for fig {pagenumber}.")
                ureg=UnitRegistry()
                tempvals=vals[vals!=kwargs.get("empty_value")]
                vals[vals!=kwargs.pop("empty_value",np.nan)]=ureg.Quantity(tempvals,kwargs.pop("defunit")).to(kwargs.get("unit")).magnitude
            else:
                if "defunit" in kwargs: del kwargs["defunit"]
                if "empty_value" in kwargs: del kwargs["empty_value"]

            if not useback:
                kwargs["cbarunit"]=kwargs.pop("unit",None)
            elif "cbar" in kwargs:
                if not isinstance(kwargs["cbar"],dict):
                    kwargs["cbar"]={"label":kwargs.pop("unit")}
                elif "label" not in kwargs["cbar"]: 
                    kwargs["cbar"]["label"]=kwargs.pop("unit")
            else:
                del kwargs["unit"]

        except:
            if not useback:
                kwargs["cbarunit"]=kwargs.get("defunit")
            elif "cbar" in kwargs:
                if not isinstance(kwargs["cbar"],dict):
                    kwargs["cbar"]={"label":kwargs.get("defunit")}
                elif "label" not in kwargs["cbar"]: 
                    kwargs["cbar"]["label"]=kwargs.get("defunit")
            if "unit" in kwargs: del kwargs["unit"]
            if "empty_value" in kwargs: del kwargs["empty_value"]
            logging.warning(f"\t\nUsing default unit ({kwargs.pop('defunit')}) for:{loggingsuffix}")
    

        if "title" in kwargs:
            titlepre=kwargs.pop("titlepre",False)
            title=kwargs.pop("title")
            if titlepre:
                title=f"{titlepre} for {title}".replace("\\n","\n")
        elif kwargs.get("titlepre"):
            title=kwargs.pop("titlepre")

        if "table" in kwargs:
            plot: _MPL_Figure=plot_api(pagenumber,subplots=(1,2),title=title,figsize=(width/dpi,height/dpi),layout=kwargs.pop("layout","tight"),subplots_kw=kwargs.pop("subplots_kw",{}))
            fig,(table_ax,ax)=plot.return_fig()
            table=kwargs.pop("table")
            tableargs=table.pop("args",())
            tablekwargs=table.pop("kwargs",{})
            tablefunc=_getfunc(table["name"])
            tableargs,tablekwargs=_read_sig(table,vals,kwargs.copy(),tableargs,tablekwargs,locals(),recnumber)
            tablefunc(*tableargs,**tablekwargs)
        else:
            plot: _MPL_Figure=plot_api(pagenumber,title=title,figsize=(width/dpi,height/dpi),layout=kwargs.pop("layout","compressed"),subplots_kw=kwargs.pop("subplots_kw",{}))
            fig,(ax,)=plot.return_fig()

        
        #Preps args and kwargs for the plot
        #[x] Make option for custom or backend
        plotsettings={key:kwargs.pop(key) for key in kwargs.copy() if key in ("subtitle","xlabel","ylabel","xticks","yticks","aspect","grid","bbox","set","cbar")}
        
        if useback:
            if "subtitle" in plotsettings:
                plot.set_subtitle(plotsettings["subtitle"],ax=ax) if not isinstance(plotsettings["subtitle"],dict) else plot.set_subtitle(ax=ax,**plotsettings["subtitle"])
            
            if "xlabel" in plotsettings:
                plot.set_xlabel(plotsettings["xlabel"],ax=ax) if not isinstance(plotsettings["xlabel"],dict) else plot.set_xlabel(ax=ax,**plotsettings["xlabel"])
            
            if "ylabel" in plotsettings:
                plot.set_ylabel(plotsettings["ylabel"],ax=ax) if not isinstance(plotsettings["ylabel"],dict) else plot.set_ylabel(ax=ax,**plotsettings["ylabel"])

            if "xticks" in plotsettings:
                plot.set_xticks(plotsettings["xticks"],ax=ax) if not isinstance(plotsettings["xticks"],dict) else plot.set_xticks(ax=ax,**plotsettings["xticks"])

            if "yticks" in plotsettings:
                plot.set_yticks(plotsettings["yticks"],ax=ax) if not isinstance(plotsettings["yticks"],dict) else plot.set_yticks(ax=ax,**plotsettings["yticks"])

            if "aspect" in plotsettings:
                plot.set_aspect(plotsettings["aspect"],ax=ax) if not isinstance(plotsettings["aspect"],dict) else plot.set_aspect(ax=ax,**plotsettings["aspect"])

            if "grid" in plotsettings:
                plot.set_grid(plotsettings["grid"],ax=ax) if not isinstance(plotsettings["grid"],dict) else plot.set_grid(ax=ax,**plotsettings["grid"])

            if "bbox" in plotsettings:
                plot.set_bbox(plotsettings["bbox"],ax=ax) if not isinstance(plotsettings["bbox"],dict) else plot.set_bbox(ax=ax,**plotsettings["bbox"])

            if "set" in plotsettings:
                plot.set(ax=ax,**plotsettings["set"])

        plotfunc=getattr(plot,plotter["name"],None)
        if plotfunc is None:
            plotfunc=_getfunc(plotter["name"])
        plotargs=plotter.pop("args",())
        plotkwargs=plotter.pop("kwargs",{})

        #sets up plot kw/args
        #[x] tuple vals might be legacy. Check
        #[x] Redo for non mesh based funcs
            #[x] Consider a mesh bool in the settings.
        if "sig" not in plotter:
            plotargs=((vals,) if not isinstance(vals,tuple) else vals)+kwargs.pop("mesh",())+plotargs
            plotkwargs.update(kwargs)
        else:
            """ plotsig=plotter.pop("sig")
            exclusive=plotsig.pop("exclusive",False)
            par=()
            pkw={}
            for key in plotkwargs:
                plotsig.pop(key,None)

            addargs="vp:plotargs" not in plotsig and "plotargs" in plotter 
            for key,item in plotsig.copy().items():
                
                if "*" in key:
                    if "**" in key: break
                    del plotsig[key]
                    if item is not None:
                        par+=vals[int(item)] if "vp:" not in str(item) else tuple(kwargs.pop(item[3:],locals().get(item[3:])))
                    break
                del plotsig[key]

                if str(item).isdigit():
                    item=vals[int(item)]
                    if key=="rec" and recnumber is not None: item=item[recnumber]
                    par+=(item,)
                    continue
                elif isinstance(item,list):
                    par+=tuple(vals[int(i)] if "vp:" not in str(i) else kwargs.pop(i[3:],locals().get(item[3:])) for i in item)
                    continue
                elif isinstance(item,str) and "vp:" in item:
                    item=kwargs.pop(item[3:],locals().get(item[3:]))
                    if key=="rec" and recnumber is not None: item=item[recnumber]
                    par+=(item,)
                    continue
            
            plotargs=par+(plotargs if addargs else ())
            
            for key,item in plotsig.items():
                if "**" in key:
                    if item is not None and item!="vp:plotkwargs":
                        pkw.update(vals[int(item)] if "vp:" not in str(item) else tuple(kwargs.pop(item[3:],locals().get(item[3:]))))
                    elif item=="vp:plotkwargs":
                        plotkwargs={**pkw, **plotkwargs}
                        break
                    else:
                        break
                if str(item).isdigit(): 
                    pkw[key]=vals[int(item)]
                    continue
                elif isinstance(item,list):
                    pkw[key]=tuple(vals[int(i)] if "vp:" not in str(i) else kwargs.pop(i[3:],locals().get(item[3:])) for i in item)
                    continue
                elif isinstance(item,str) and "vp:" in item:
                    pkw[key]=kwargs.pop(item[3:],locals().get(item[3:]))
                    continue
            else:
                plotkwargs={**pkw, **plotkwargs}
            if not exclusive:
                plotkwargs.update(kwargs) """

            plotargs,plotkwargs=_read_sig(plotter,vals,kwargs,plotargs,plotkwargs,locals(),recnumber)

        logging.debug(f"Fig {pagenumber} plotkwargs: {plotkwargs}")
        logging.debug(f"Plotting fig {pagenumber}.")

        #[x] Custom plot option
        cm=plotfunc(*plotargs,**plotkwargs)
        if useback and "cbar" in plotsettings:
            print(pagenumber,plotsettings["cbar"])
            plot.cbar(cm,ax=ax,**plotsettings.pop("cbar",) if isinstance(plotsettings["cbar"],dict) else {})
        
        pngpath=os.path.join(savedir,f"pngs/{os.path.basename(path).split('.')[0]+'-' if not pdf else ''}{pagenumber}.png")
        logging.debug(f"Fig {pagenumber} plotted.")

        plot.savefig(pngpath,dpi=dpi)
        logging.info(f"Fig saved for page {pagenumber}")

        if pdf: _writepdf(pngpath,width,height)
        logging.info(f"Page {pagenumber} succesfully writen.")
    except Exception as e:
        logging.error(f"An error occured for fig {pagenumber}.")
        logging.exception(f"{e}")
        

def vispipe(config,image=True,pdf=False,compress=False,loglevel=30):
    """Function to run batch visuilize hydrolic model outputs.

    Parameters
    ----------
    `config` : str | dict
        Path to config json file or dictionary.
        
    Keyword Arguments
    ------------------
    `image` : bool=True
        Deterimins whether pngs dir will be deleted. If False, it is left inplace.
    `compress` : bool=False
        Compresses pngs dir to a .tar.gz if true. 
    `loglevel` : int=30
        Log level for logging module.
        
    """
    if pdf: image=not image

    logging.debug("Reading universal settings.")
    with open(os.path.join(os.path.dirname(__file__),"settings.json")) as file:
        settings_jason=json.load(file)
        format_jason=settings_jason.get("format",{})
        readers_jason=settings_jason.get("readers",{})
        plotters_jason=settings_jason.get("plotters",{})
        universal_jason: dict[str,dict]=settings_jason["universals"]

    if not isinstance(config,dict):
        logging.debug("Reading config.")
        #[ ] add functionality to pass dict.
        with open(config) as file:
            config=json.load(file)
    global_jason=config["globals"]
    plots_jason: dict=config["plots"]
    
    savedir=global_jason.get("save_path",os.path.abspath(os.curdir))
    if ".pdf"==savedir[-4:]:
        savedir,savepdf=os.path.split(savedir)
    elif pdf:
        savepdf=f"{os.path.basename(savedir)}.pdf"


    logging.debug("Setting format.")
    formattype=global_jason.get("format",format_jason["default"]).lower()
    fmtset=set(format_jason["set"])
    for key,settings in universal_jason.items():
        #Selecting proper format settings
        if fmtset & settings.keys():
            fmtsettings=settings.pop(formattype,{})
            for delkeys in fmtset-set([formattype]):
                settings.pop(delkeys,None)
            settings.update(fmtsettings)
        #Pulling settings from the base 
        #[ ] Try turning this into a for loop
        if base:=settings.pop("base",False):
            basesettings=deepcopy(universal_jason[base])
            if "reader" in settings:
                settings["reader"]=_merge_func_setting(settings,basesettings,"reader",readers_jason)
            else:
                settings["reader"]=basesettings["reader"]
            
            if "plotter" in settings:
                settings["plotter"]=_merge_func_setting(settings,basesettings,"plotter",plotters_jason)
            else:
                settings["plotter"]=basesettings["plotter"]

            if "stattable" in settings:
                settings["stattable"]=_merge_func_setting(settings,basesettings,"stattable")
            else:
                settings["stattable"]=basesettings["stattable"]

            
            #[ ] test this for a fort.14 not named grd 
            #[ ] Set up netcdf to use contained grid during plotting
            #Adding a grd for a netcdf file
            #if "grd" not in global_jason and key in global_jason and base=="minmax63":
            #    global_jason["grd"]=key
            basesettings.update(settings)
            universal_jason[key]=basesettings

    logging.debug(f"Format set to {formattype}.")
    globsets=[(key,item) for key,item in global_jason.items()]
    
    for key,item in globsets:
        if key=="grd" or isinstance(item,dict) and (meshtype:=item.get("meshtype")):
            logging.debug(f"Reading mesh {key}.")
            if key=="grd":
                meshtype=None
                if not isinstance(item,dict): 
                    if formattype!="netcdf4":
                        item={"path":item}
                    else:
                        item={"path":global_jason[item] if not isinstance(global_jason[item],dict) else global_jason[item]["path"]}
                    global_jason[key]=item
            reader=item.pop("reader",universal_jason.get("grd",universal_jason.get(meshtype)).pop("reader"))
            readerargs=item.pop("reader_args",universal_jason.get("grd",universal_jason.get(meshtype)).pop("reader_args",()))
            readerkwargs=item.pop("reader_kwargs",universal_jason.get("grd",universal_jason.get(meshtype)).pop("reader_kwargs",{}))

            readfunc=_getfunc(reader)
            global_jason[key]["vals"]=readfunc(global_jason[key]["path"],*readerargs,**readerkwargs)
    

    logging.debug("Making pngs and pages dirs.")
    pngpath=os.path.join(savedir,"pngs")
    if not os.path.exists(pngpath): os.mkdir(pngpath)
    if pdf:
        pagespath=os.path.join(savedir,"pages")
        if not os.path.exists(pagespath): os.mkdir(pagespath)
    
    inputs=[]
    for i,(key,plot) in enumerate(plots_jason.items()):
        logging.debug(f"Making setting plot settings for {key}.")
        logging.debug(f"Setting references.")
        if plot is None: plot={}
        if "type" in plot:
            globalkey=plot["type"]
        else:
            globalkey=key.split(":")[0]
        #plotdict={}
        
        if globalkey in universal_jason:
            universalkey=globalkey
        elif "type" in global_jason[globalkey]:
            universalkey=global_jason[globalkey]["type"]
        elif "meshtype" in global_jason[globalkey]:
            universalkey=global_jason[globalkey]["meshtype"]
        else:
            universalkey=None
        
        logging.debug(f"Reference keys are:\n\tplot: {key}\n\tglobal: {globalkey}\n\tuniversalkey: {universalkey}")

        logging.debug("Updating universal settings.")
        #if universalkey: plotdict.update(universal_jason.get(universalkey,{}))
        
        logging.debug("Updating global settings.")
        globplot=global_jason.get(globalkey,{})
        if isinstance(globplot,str):
            globplot={"path":globplot}
        globkwargs=global_jason.get("global_kwargs",{})

        plotdict={**universal_jason.get(universalkey,{}),**globkwargs,**globplot}

        #if isinstance(globplot,dict):
        #    plotdict.update(globplot)
        #else:
        #    plotdict.update({"path":globplot})
        #plotdict.update(globkwargs)
        
        logging.debug("Updating plot settings.")
        if "reader" in plot:
            plot["reader"]=_merge_func_setting(plot,plotdict,"reader",readers_jason)

        if "plotter" in plot:
            plot["plotter"]=_merge_func_setting(plot,plotdict,"plotter",plotters_jason)

        if "stattable" in plot:
            plot["stattable"]=_merge_func_setting(plot,plotdict,"stattable")

        plotdict={**plotdict,**plot}

        if plotdict.get("table"):
            plotdict["table"]=plotdict.pop("stattable",False)
        elif "stattable" in plotdict:
            del plotdict["stattable"]

        #[x]
        if plotdict["plotter"].get("mesh"):
            logging.debug(f"Adding mesh data from {plotdict['mesh']}.")
            plotdict["mesh"]=global_jason[plotdict["mesh"]]["vals"]
        elif "mesh" in plotdict:
            del plotdict["mesh"]

        logging.debug("Adding save path and units.")
        plotdict["savedir"]=savedir
        
        if plotdict.get("unit")!=universal_jason.get(universalkey)["unit"]:
            plotdict["defunit"]=universal_jason.get(universalkey)["unit"]

        plotdict["pdf"]=pdf

        logging.debug("Checking minreqs.")
        minreqs=set(plotdict.pop("minimum"))
        dif=minreqs-set(plotdict.keys())
        if not dif or "vals" in plotdict and not len(dif)-1:
            logging.debug(f"All minreqs found for {key}.") 
            plotdict["loglevel"]=loglevel
            if (numreqs:=plotdict.pop("numreqs",False)) and (fields:=plotdict.pop("record_dependent",False)):
                logging.debug("Making record specific plots")
                for dec in range(numreqs):
                    locplotdict={key:item if key not in fields else item[dec] for key,item in plotdict.items()}
                    locplotdict["pagenumber"]=i+dec*10**-1
                    locplotdict["recnumber"]=dec

                    if plotdict.get("defunit"):
                        locplotdict["defunit"]=plotdict["defunit"][dec]
                    locplotdict.pop("record_dependent",None)
                    inputs.append(locplotdict)   
                    logging.debug(f"Fig {locplotdict['pagenumber']} kwargs {locplotdict}")
                
            
            else:
                plotdict["pagenumber"]=float(i)
                plotdict.pop("record_dependent",None)
                inputs.append(plotdict)
                logging.debug(f"Fig {plotdict['pagenumber']} kwargs {plotdict}")
        else:
            logging.error(f"Keys {minreqs - set(plotdict.keys())} are missing for plot {key}. Skipping.")
        
    #Pool() is a function used in multiprocessing. It creates a pool of functions all running at the same time. This is used in place of a for loop to speed things up drastically. 
    #The time to complete the entire proccess is roughly how long it takes to complete the largest set, instead waiting for all to finish one after the other.
    with Pool() as pool:
        result=pool.map_async(_pipeline,inputs)
        result.wait()
    #This orders the individual pages and saves them as one file before cleaning up the work space.
    #This try block allows for the error to be printed if all of the Pool jobs fail and still delete /pngs and /pages.
    try:
        if pdf: _orderpdf(os.path.join(savedir,savepdf))
    except Exception as e:
        logging.exception(f"{e}")
        if not image: shutil.rmtree(pngpath)
        if pdf: shutil.rmtree(pagespath)
        return

    #Cleans up workspace based on command line flags.
    if compress:
        import tarfile
        if os.path.isfile(f"{pngpath}.tar.gz"): 
            import pathlib
            pathlib.Path.unlink(f"{pngpath}.tar.gz")
        with tarfile.open(f"{pngpath}.tar.gz", "x:gz" ) as tar:
            tar.add(pngpath,arcname="pngs")
    if not image: shutil.rmtree(pngpath)
    if pdf: shutil.rmtree(pagespath)
    
    