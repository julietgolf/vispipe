Getting Started
###############

The goal of this guide is to install, setup, and run vispipe. 

.. note::
    This page applies to both ``dict`` types and JSON types. All types will be referred to by there Python types for simplicity except for ``null``.

Installation
************

Until VisPipe is on PYPI, it must be set up from the gitlab repo. The simplest way to do this is to clone 
the source from the repo and follow the below steps. 

.. code-block:: console

    git clone vispipe
    cd vispipe
    pip install .


This will construct the package and any install any dependencies. 

settings.json
*************

Next, settings.json must be edited. This file holds default values for each datatype. This file is located
in the Python package under ``vispipe/settings.json``. In settings.json, add the desired datatypes to the 
``"universal"`` dictionary. Each datatype will be a key value pair where the key is the datatype name and 
the value is a dictionary with default settings. These will generally include, the reader function, the 
plotter, if and what mesh is needed for that plotter, labels, and units. All of these values can be over 
written in the config.

Readers should be placed in a function dictionary. These dictionaries have 3 keywords: ``"name"``, ``"args"``, 
``"kwargs"``. The ``"name"`` is a ``str`` of either one of the names of the built in plotters or 
"module.submodule.func". ``"args"`` is a ``list`` are static args that are normally added at the end of
any dynamically defined args. ``"kwargs"`` is a ``dict`` of predefined kwargs. If ``"args"`` and
``"kwargs"`` are not needed, then just the value of ``"name"`` can be provided instead of the dictionary.

.. note::
    If the reader outputs values other than the data, a ``"sig"`` must be given to the plotter. See 
    :doc:`funcdict` for more details.

.. code-block:: JSON
    :caption: A simple datatype for a maxvel.63 in ADCIRC.

    "maxvel": {
            "reader": {
                "name":"meshtools.read_minmax63",
                "kwargs":{"extreme_only":true}
            },
            "mesh": "grd",
            "plotter": "tricontour",
            "unit": "mps",
            "xlabel": "Longitude (deg)",
            "ylabel": "Latitude (deg)",
            "fillval":-99999,
            "aspect":"equal",
            "extend":"both"
        }

.. note::
    If VisPipe is not installed in a virtual environment and the site-packages folder of the python environment 
    requires super user privileges, settings.json can be edited by editing in the source before installing. 

.. seealso::
    :doc:`settings` for more details on settings.json.

Config
******

The *config.json* are used each run to produce the plots. It is split into 2 fields, ``"globals"`` and ``"plots"``. 
The ``"globals"`` are used by all plots of that datatype and ``"global_kwargs"`` is a sub-dictionary of ``"globals"`` 
with settings that are applied to all datatypes. Each datatype in ``"globals"`` is a dictionary that at a minimum 
requires ``"path"`` with the absolute or relative path to the file the data will be pulled from. If no other settings 
are needed for that datatype, then just the path can be given in place of the dictionary.  By default, the key refers
to a member in ``"universal"``. If ``"type"`` is added with the name of the relevant ``"universal"`` to the datatypes
``"globals"`` dictionary, its key can be anything.

The ``"plots"`` field contains the settings specific to each plot. This is the final level of settings needed to 
make plots. Each member of ``"plots"`` is for all intents and purposes a plot. The key for the plot should be a 
reference to a member in ``"globals"``. If multiple plots of the same data are needed, append ``":*"`` to the end of 
the key. What follows the colon is unimportant, just that it makes the key unique. If no settings need to be defined
``null`` can be used in place of a dictionary. If producing a PDF, the order the plots appear in ``"plots"`` will be
their order in the PDF.

.. code-block:: JSON
    :caption: Example config file

    {
    "globals": {
        "global_kwargs": {"cmap": "magma"},
        "grd": "EC95_g01.grd",
        "maxele": {
            "path": "TRAINING_TP_0100_SYN_Tides_0_SLC_0_RFC_0_WAV_1_GCP_EC95_maxele.63",
            "title": "GCP_EC95 SYN TP 0100\\nTides 0 SLC 0 RFC 0 WAV 1",
            },
        "NNJ800.Tp": {
            "path": "TRAINING_TP_0100_SYN_Tides_0_SLC_0_RFC_0_WAV_1_GCP_EC95_NNJ800.Tp.out_max",
            "type": "Tp.out_max"
        },
        "save_path": "simple.pdf"
    },
    "plots": {
        "grd": {
            "title": "GCP_EC95 SYN TP 0100\\nTides 0 SLC 0 RFC 0 WAV 1",
            "cmap": "gray"
        },
        "maxele": null,
        "maxele:0": {
            "unit": "feet",
            "bbox": [-75.0,39.7,-71.4,41.7]
        },
        "NNJ800.Tp": {
            "title": "GCP_EC95 SYN TP 0100\\nTides 0 SLC 0 RFC 0 WAV 1",
        }
    }
    }

.. seealso::
    :doc:`config` for a more in-depth explanation. 

Settings Priority
*****************

3 levels of settings have been described: ``"universal"``, ``"globals"``, and ``"plots"``. These levels are listed in ascending priority. 
This means that any setting defined multiple times will take the value defined the furthest down the list. While not equivalent, this code 
is descriptive of how settings are updated:

.. code-block:: python
    
    plot_uni = universal_settings[datatype]
    plot_glb = global_settings[datatype]
    plot_plt = plot_settings[datatype]

    plot_kwargs = {}

    plot_kwargs.update(plot_uni)    
    plot_kwargs.update(plot_glb)
    plot_kwargs.update(plot_plt)

    multiprocessing.Pool(plot_kwargs)


Each time plot_kwargs is updated, any keywords in the updater and not in plot_kwargs are added. Any keywords in both the updater and plot_kwargs 
have their value changed in plot_kwargs. With a few exceptions, any setting can be defined at any level. 

A useful visualization is swiss cheese. A piece of bread represents a functions keyword arguments and swiss cheese represents a settings level. 
When slice is laid on the bread, The bread will be covered, but some of the swiss' holes will show the bread below. When another slice is placed,
some of the first slice and bread will be visible. Finally, the third slice will cover some and show some of the second slice, third slice, and 
the bread. As long as there are no holes in the bread, it should fall apart when picked up.

Execution
*********

To execute, either :doc:`vispipe.vispipe</reference/vispipe/vispipe.vispipe>` or the built in terminal command :doc:`vispipe</reference/cli>`. Both 
take the path to the config as their first argument, but the function can take a config ``dict`` inplace of the path. Vispipe can out put the plots
as PNGs, a .tar.gz of the PNGs, or as a PDF using the options below.

.. list-table:: Output Options
    :widths: auto
    :header-rows: 1

    * - Format 
      - ``vispipe()`` kwarg
      - ``vispipe`` Flag

    * - .png
      - ``image = True``
      - -i, --image
    * - .pdf
      - ``pdf = True``
      - -p, --pdf
    * - .tar.gz
      - ``compress = True``
      - -c, --compress

.. note::
    ``image`` is ``True`` by default. If ``pdf`` and ``compress`` are ``True`` ``image`` will only be ``not``ed once. If ``image`` is set to ``False`` when either 
    is set to ``True``, ``images`` will be switched back to ``True``.

.. seealso::
    :doc:`Vispipe CLI</reference/cli>` for more information on terminal flags.

