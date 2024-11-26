Writing Config Files
********************

Vispipe config files are used to produce plots. In this file, the paths to the data, the datatypes that will be 
plotted, and the settings used to plot them are defined. Configs can be either a ``dict`` passed directly to 
``vispipe()`` or a JSON file whose path is passed to ``vispipe()``. They consist of a two sections: 
``"globals"`` and ``"plots"`` 


#. :data:`globals`
#. :ref:`"plots"`

.. note::
    This page applies to both ``dict`` types and JSON types. All types will be referred to by there Python types for simplicity except for ``null``. 


Structure
=========

The config is ``dict`` with two sub-dictionaries, ``"globals"`` and ``"plots"``.

.. code-block:: JSON 
    :caption: The basic layout of the config.

    {
        "globals":{
            "datatype": {"setting": "setting"}
        },
        "plots":{
            "plot": {"setting": "setting"}
        }
    }

.. _globals:

"globals"
---------

``"globals"`` contains datatype dictionaries whose settings will be applied to plots of that type, a ``"global_kwargs"`` dictionary whose
settings apply to all types, and the save path. It's primary function is to serve as a map from ``"plots"`` to ``"universal"`` [1]_.  The 
mapping is handled either sharing a key in ``"universal"`` or by using the ``"type"`` option in the datatype. ``"type"`` should reference 
a ''"universal"`` member. This allows for the multiple members of ``"globals"`` to share a datatype without sharing a key. Secondarily,
paths to the data are generally placed here using the ``"path"`` keyword. 

If a setting is shared across all datatypes in globals it can be placed in ``"global_kwargs"``. This is a sub dictionary of ``"globals"``.
The settings in this dictionary are considered to have a higher priority than ``"universal"`` but lower than a specific datatype in 
``"globals"``. Settings in ``"global_kwargs"`` can be overwritten by specifying them in a datatype in ``"globals"`` or a plot in ``"plots"``

``"save_path"`` is an optional keyword that specifies either the folder for the output PNGs or the location of the PDF. If it not specified,
the current directory will be used as the save path. In the event that a PDF will be generated, the filename will be derived from the name of 
the current directory. 

.. code-block:: JSON 
    :caption: A ``"globals"`` section showing the different ways of specifying settings. See that paths can be relative or absolute.
    :emphasize-lines: 6, 8, 12

    {
        "globals":{
            "global_kwargs": {
                "cmap": "jet"
            },
            "minpr": "C:\\Users\\Username\\Desktop\\example\\EC95\\TRAINING_TP_0100_SYN_Tides_0_SLC_0_RFC_0_WAV_1_GCP_EC95_minpr.63",
            "maxele": {
                "path": "TRAINING_TP_0100_SYN_Tides_0_SLC_0_RFC_0_WAV_1_GCP_EC95_maxele.63",
                "cmap": "viridis"
                },
            "LID800.Tp": {
                "path": "TRAINING_TP_0100_SYN_Tides_0_SLC_0_RFC_0_WAV_1_GCP_EC95_LID800.Tp.out_max",
                "type": "Tp.out_max"
            },

        },
        "plots":{
            "plot": {"setting": "setting"}
        }
    }


"plots"
-------

The ``"plots"`` dictionary is the final level of settings before plotting. As opposed to ``"globals"`` and ``"universal"`` which define 
the general settings of a datatype, ``"plots"`` are specific to a plot and not shared. Things like ``"title"`` and ``"bbox"`` are defined
here as they are usually unique to that plot. These dictionaries have the highest priority of all levels. Any and all settings can be reset
at this level. If ``null`` is passed instead a settings dictionary, the plot will assume all settings defined in ``"globals"`` and ``"universal"``.

The names of the individual plot dictionaries should match the name of a member of ``"globals"``. If multiple plots reference the same member,
add a ``":"`` and some unique identifier after the colon. The contents identifier have no impact other than to prevent repeated keys in ``"plots"``.


If only PNGs are being produced, the order of the members of plots does not matter. However, if a PDF is being produced the, order determines 
the order of the plots in the PDF.

.. code-block:: JSON 
    :caption: A simple ``"plots"`` section. Notice even the plotter can be reset.
    :emphasize-lines: 19
    
    {
        "globals":{
            "global_kwargs": {
                "cmap": "jet"
            },
            "minpr": "C:\\Users\\Username\\Desktop\\example\\EC95\\TRAINING_TP_0100_SYN_Tides_0_SLC_0_RFC_0_WAV_1_GCP_EC95_minpr.63",
            "maxele": {
                "path": "TRAINING_TP_0100_SYN_Tides_0_SLC_0_RFC_0_WAV_1_GCP_EC95_maxele.63",
                "cmap": "viridis"
                },
            "LID800.wave": {
                "path": "TRAINING_TP_0100_SYN_Tides_0_SLC_0_RFC_0_WAV_1_GCP_EC95_LID800.wave.out_max",
                "type": "wave.out_max"
        },
        "plots": {
            "maxvel": null,
            "maxvel:0":{
                    "title": "Maximum Water Velocity Distribution."
                    "plotter": "hist",
                    "nbins":1001
                },
            "minpr": {
                "unit": "mbar",
                "table":true,
                "title": "GCP_EC95 SYN TP 0100\\nTides 0 SLC 0 RFC 0 WAV 1",
                "bbox": [-75.0,39.7,-71.4,41.7]
            },
            "LID800.wave": {
                "unit": "sec",
                "title": "GCP_EC95 SYN TP 0100\\nTides 0 SLC 0 RFC 0 WAV 1"
            }
        }
    }


Passing Data
============

While paths can be placed into ``"plots"``, ``"globals"`` it is often more convenient to place them here. This is because if there are no 
other settings that need to be specified at the ``"globals"`` level for a datatype, the path can be passed as a ``str``, e.g. 
``"datatype": "some\\path\\to\\file.data"``, directly instead of as a ``dict``, ``"datatype": {"path": "some\\path\\to\\file.data"}``. [1]_ Alternatively,
the data can be passed directly into ``vispipe()`` using the ``"vals"`` keyword. This can only be done by passing a ``dict`` to ``vispipe()``.



Plotting with Multiple Records
==============================

Datatypes whose ``"universal"`` has a :ref:`"file_recs"<file_recs>` field can be changed using the ``"recs"`` keyword from
either ``"plots"`` or ``"universals"``. The value of ``"recs"`` can take the form of a ``str``, ``list[str]``, or ``dict``. ``
When in the form of a ``str`` or ``list``, recs acts a filter. Not changing any settings, but rather it determines what records
to plot and what order to plot them in. In the form of a ``dict``, ``"recs"`` will also change the settings. 

When ``"recs"`` settings are being merged, only the keys in the higher priority field, whether ``str``, ``list``, or ``dict``, 
are considered. If for instance, ``"globals"`` has ``"recs": ["height","period"]`` and ``"plots"`` has ``"recs": "period"``, 
``"height"`` from globals will be ignored. 

.. caution::
    If the union of the two sets of ``"recs"`` keys between ``"globals"`` and ``"plots"`` is ``{}``, ``"plots"`` will not be connected
    ``"universal"`` for the record specified in ``"plots"``. This is because the only settings that get passed are those specified
    at the higher level. If ``"plots"`` had ``"recs": "direction"`` and ``"globals"`` had the same in the previous example, ``"plots"``
    would have nothing to draw from ``"globals"`` since ``"globals"`` never knew to draw from ``"universal"``.   

When record settings are being updated, they have a priority of .5 higher than their parents level. So if a setting is defined in
both ``"globals"`` and a record in ``"recs"`` of ``"globals"``, ``"recs"`` will overwrite ``"globals"`` for that record. However,
if it is also in ``"plots"`` but not in the record for the ``"recs"`` in ``"plots"``, the final settings will be taken from 
``"plots"`` and not from the ``"recs"`` in ``"globals"``.


.. code-block:: JSON 
    :caption: ``"LID800.wave"`` has narrowed its recs down in ``"globals"``. In ``"plots"``, the order was swapped and different color maps where specified for each.
    :emphasize-lines: 14,33,36

    {
        "globals":{
            "global_kwargs": {
                "cmap": "jet"
            },
            "minpr": "C:\\Users\\Username\\Desktop\\example\\EC95\\TRAINING_TP_0100_SYN_Tides_0_SLC_0_RFC_0_WAV_1_GCP_EC95_minpr.63",
            "maxele": {
                "path": "TRAINING_TP_0100_SYN_Tides_0_SLC_0_RFC_0_WAV_1_GCP_EC95_maxele.63",
                "cmap": "viridis"
                },
            "LID800.wave": {
                "path": "TRAINING_TP_0100_SYN_Tides_0_SLC_0_RFC_0_WAV_1_GCP_EC95_LID800.wave.out_max",
                "type": "wave.out_max",
                "recs": ["height","period"]
        },
        "plots": {
            "maxvel": null,
            "maxvel:0":{
                    "title": "Maximum Water Velocity Distribution."
                    "plotter": "hist",
                    "nbins":1001
                },
            "minpr": {
                "unit": "mbar",
                "table":true,
                "title": "GCP_EC95 SYN TP 0100\\nTides 0 SLC 0 RFC 0 WAV 1",
                "bbox": [-75.0,39.7,-71.4,41.7]
            },
            "LID800.wave": {
                "unit": "sec",
                "title": "GCP_EC95 SYN TP 0100\\nTides 0 SLC 0 RFC 0 WAV 1"
                "recs": {
                    "period": {
                        "cmap": "plasma"
                    },
                    "height":{
                        "cmap": "magma"
                    }
                }
            }
        }
    }


.. rubric:: Footnotes
.. [1] This functionality will be provided to ``"plots"`` in the future. 

