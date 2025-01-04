Settings File
*************

The ``settings.json`` file is where common and frequently used settings are defined. These are treated as default
settings across all ``vispipe`` runs. It is split into 5 sections:

#. :ref:`"universal"<"universal" and Datatypes>`
#. :ref:`"format"`
#. :ref:`"readers"<"readers" and "plotters">`
#. :ref:`"plotters"<"readers" and "plotters">`
#. :ref:`"options"` 
#. :ref:`"opt"` 

Each section is a JSON ``object`` type which translate to Python ``dict`` type. All but ``"universal"`` are
optional. However, the more robust ``settings.json`` the simpler config and opt files will be to write

.. note::
    This page applies to both ``dict`` types and JSON types. All types will be referred to by there Python types for simplicity except for ``null``.

Sections
========

"universal" and Datatypes
-------------------------

The members of ``"universal"`` are the individual datatypes that ``vispipe`` can plot. The settings defined in each
datatype are the lowest priority settings, if they are defined in a config or opt they will be overwritten.

.. code-block:: JSON
    :caption: An overly robust example for a ``maxvel.63`` file from ADCIRC. 

    "maxvel": {
            "ascii": {
                "reader": {
                    "name":"meshtools.read_minmax63",
                    "kwargs":{"extreme_only":true}
                }
            },
            "netcdf4": {
                "reader": {
                    "name":"meshtools.file_io.readers.readvalnc"
                    "args":["vel_max"]
            },
            "mesh": "grd",
            "plotter": "tricontour",
            "minimum": ["reader","plotter","path"],
            "empty_value": -99999,
            "stattable":{
                "name":"meshtools.plotters.plotters.stattable",
                "kwargs":{"modeltype":"adcirc"},
                "sig":{"vals":"vp:vals","ax":"vp:table_ax","mesh":"vp:mesh","*":null,"exclusive":true}
            },
            "xlabel": "Longitude (deg)",
            "ylabel": "Latitude (deg)",
            "titlepre": "ADCIRC Maximum Water Speed",
            "unit": "mps",
            "cbar":true,
            "aspect":"equal",
            "extend":"both"
        }

The above example is intentionally verbose to be used as a demonstrate for the rest of the guide. In a real
``settings.json`` much of the above can be simplified. 

.. _file_recs:

File Records
^^^^^^^^^^^^

Files that contain multiple datatypes with different settings requirements are accounted for with the ``"file_records"`` 
field. This field is a ``dict[dict]`` where each record of the file is described by a subdictionary named by 
the subdatatype. The subdictionaries are formatted the same as normal datatypes and is weighted .5 more in priority 
than its parent. This means it will overwrite setting that it has in common with its parent datatype, but not a setting
defined in the config file. 

If the reader function outputs all records at once, the members of ``"file_records"`` should be in the same order. Their
order also determines the order they will be placed into a PDF if generated. To change this order or to only plot a 
subset of the records, a field ``"recs"`` consisting of a ``str`` or ``list[str]``, where the ``str`` is a keyword in 
``"file_records"``, can be added to the datatype. 

.. code-block:: JSON 
    :caption: An example from STWAVE. ``"recs"`` will cause ``"direction"``, then ``"height"``, but not ``"period"`` to be plotted.

    "wave.out_max":{
        "base": "out_max",
        
        "plotter":{
            "sig":{"rec":0,"mesh":1,"*":null}
        },
        "stattable":{
            "sig":{"rec":0,"ax":"vp:table_ax","mesh":1,"*":null,"exclusive":true}
        },
        "recs": ["direction","height"]
        "file_records":{
            "height":{
                "unit": "meter",
                "titlepre": "STWAVE Significant Wave Height",
                "crange": false
            },
            "period":{
                "unit": "sec",
                "titlepre": "STWAVE Associated Mean Wave Period",
                "crange": false
            },
            "direction":{
                "unit": "deg",
                "titlepre": "STWAVE Associated Mean Wave Direction",
                "crange": ["h",0,360]
            }
        }
    }
    

``"base"`` Datatypes
^^^^^^^^^^^^^^^^^^^^

Datatypes can call on a base datatype to inherit default settings. This is done by adding the keyword ``"base"``
where the value is another member of ``"universals"``.

.. code-block:: JSON
    :caption: Much of the example from above can be moved into a base datatype and reused.
    :emphasize-lines: 28, 37

    "minmax63": {
            "ascii": {
                "reader": {
                    "name":"meshtools.read_minmax63",
                    "kwargs":{"extreme_only":true}
                }
            },
            "netcdf4": {
                "reader": "meshtools.file_io.readers.readvalnc"
            },
            "mesh": "grd",
            "plotter": "tricontour",
            "minimum": ["reader","plotter","path"],
            "empty_value": -99999,
            "stattable":{
                "name":"meshtools.plotters.plotters.stattable",
                "kwargs":{"modeltype":"adcirc"},
                "sig":{"vals":"vp:vals","ax":"vp:table_ax","mesh":"vp:mesh","*":null,"exclusive":true}
            },
            "xlabel": "Longitude (deg)",
            "ylabel": "Latitude (deg)",
            "cbar":true,
            "unit":"feet",
            "fillval":-99999,
            "aspect":"equal",
            "extend":"both"
        },
    "maxvel": {
        "base": "minmax63",
        "titlepre": "ADCIRC Maximum Water Speed",
        "unit": "mps",
        "reader": {
                "name":"meshtools.file_io.readers.readvalnc"
                "args":["vel_max"]
        }
    },
    "maxele": {
        "base": "minmax63",
        "titlepre": "ADCIRC Maximum Water Height",
        "unit": "meter",
        "reader": {
                "name":"meshtools.file_io.readers.readvalnc"
                "args":["zeta_max"]
        }
    }

``"grd"`` and Mesh Datatype
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If a plotter requires a mesh to plot data against, the datatype being plotted points to the mesh with the keyword 
``"mesh"`` where the value is the datatype name of the mesh. Alternatively, if ``"mesh"`` is missing or set to ``True``,
the ``"grd"`` datatype is treated as the default mesh.

Type Aliasing
^^^^^^^^^^^^^

By default, the key used in a config is used to search ``"universal"`` settings. This does not work when there are 
multiple sets of data of the same datatype since this would cause a naming conflict. 

"readers" and "plotters"
------------------------

In these sections, reader and plotting functions can be defined so they can be reused in datatypes. The keys for the
individual function dictionaries are what would normally be in the ``"name"`` field. 


"format"
--------

The ``"format"`` section consists of a ``"default"``, which defines the default file format, and ``"set"``, 
which defines the other accepted formats. Datatypes can have members whose keyword matches a member of 
``"set"`` and a ``dict`` as the value. When ``settings.json`` is ingested, the correct format is selected from
the datatypes and the contents of the corresponding ``"dict"`` are moved up into the datatype as normal settings.

.. code-block:: JSON
    :caption: Example using ascii and netcdf4.

    "format":{
    "default": "ascii",
    "set": ["ascii", "netcdf4"]
    }



"options"
---------

The ``"options"`` field is used to change the settings in ``vispipe._options._Options``. 

.. list-table:: ``"options"`` Values
    :widths: auto
    :header-rows: 1

    * - Name
      - Description
      - Requirement
    * - ``"ncpu"``
      - Number of CPUs used by ``multiprocessing.Pool``.
      - ``int`` or ``str(int)``
    * - ``"dpi``
      - Dots per inch. Density of the final image.
      - ``int`` or ``str(int)``
    * - ``"resolution"``
      - Resolution of the final image.
      - ``list[x,y]`` where ``x`` and ``y`` are ``int`` or ``str(int)``
    * - ``backend``
      - The plot backend used by vispipe.
      - ``str`` formatted "[modules,...].backend"


.. _uni_opt:

"opt"
-----

The models that :func:`vispipe.opt_reader` should look for is defined here. ``"opt"`` is a nested dictionary with 3
levels. The top level are the names of the models, the middle is the datatypes in that model, and
the bottom are settings for ``vispipe.opt_reader()``. The only current setting at the lowest level
is ``"file_base"``, which is the base name of the data file if it is not the datatype name.

.. _CSTORM: https://www.erdc.usace.army.mil/Media/Fact-Sheets/Fact-Sheet-Article-View/Article/476697/

.. code-block:: JSON
    :caption: The ``"opt"`` field for `CSTORM`_.

    "opt":{
        "adcirc":{
            "grd":{"file_base":"fort.14"},
            "minpr":{"file_base":"minpr.63"},
            "maxele":{"file_base":"maxele.63"},
            "maxwvel":{"file_base":"maxwvel.63"},
            "maxvel":{"file_base":"maxvel.63"}
        },
        "swan":{
            "swan_HS_max":{"file_base":"swan_HS_max.63"},
            "swan_TPS_max":{"file_base":"swan_TPS_max.63"},
            "swan_TM01_max":{"file_base":"swan_TM01_max.63"},
            "swan_TM02_max":{"file_base":"swan_TM02_max.63"},
            "swan_TMM10_max":{"file_base":"swan_TMM10_max.63"},
            "swan_DIR_max":{"file_base":"swan_DIR_max.63"}
        },
        "stwave":{
            "Tp.out_max":{},
            "wave.out_max":{}
        }
    }

CLI Flag
========

Running ``vispipe --swap_settings /path/to/new/settings.json`` in the command line adds a new 
settings.json to vispipe. The previous settings.json is renamed and kept in the module directory. 