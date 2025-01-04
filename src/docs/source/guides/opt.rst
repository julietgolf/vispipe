OPT Files
#########

OPT files are a modification of the standard :doc:`config files<config>`. They are designed to be more light weight and reusable in 
non-Python based workflows. They share much of their syntax with config files. Instead of having a ``"plots"`` section, OPT
files have multiple groups of plots with common settings, such as a common ``"bbox"``. 

.. seealso:: 
    :func:`vispipe.opt_reader`

.. note::
    This page applies to both ``dict`` types and JSON types. All types will be referred to by there Python types for simplicity except for ``null``.


Structure
=========

As stated the structure of an OPT is largely the same as the config. The OPT shares its ``"globals"`` field with
the :ref:`config's "globals"<config_globals>`, with the exception that ``"paths"`` are excluded since they will be generated.
The main difference comes in how plots are defined. OPTs use what are referred to as plot groups. These groups are 
designed to reduce redundancy as much as possible.


Groups
------

Groups are plots that share some common setting or settings. These settings are defined once and the passed to all members of that group. 
Each group is a ``dict`` that contains the common settings and the plot dicts for the plots in that group. When the group only has one 
common setting, the name of that group is the key that refers to that setting within the group. When there are multiple common settings,
the name of the group is named ``"group"`` and contains a ``dict`` also named ``"group"`` with the common settings. 

If a group contains no common settings it is named ``"default"``. This group behaves like the ``"plots"`` section from a config file. This
is helpful for placing a plots in between groups. 

"deflist" and fill
------------------

``"deflist"`` is an optional ``"globals"`` keyword that defines what datatypes will be used in the OPT. This can be used in conjunction with
the fill option. 

.. caution::
    ``"deflist"`` is not optional if ``"opt"`` is not defined in settings.json. How ``vispipe.opt_reader()`` handles ``"deflist"`` and ``"models"`` will be reworked to fix this.


.. code-block:: JSON 
    :caption: An example opt showing the three types of groups.
    :emphasize-lines: 9, 22, 36
    
    {
        "globals": {
            "global_kwargs":{ "cmap": "jet"},
            "deflist": [ "maxele","grd","minpr","maxwvel" ],
            "maxele": {"cmap": "magma"}
            
        },

        "default":{
            "grd": "default",
            "maxele":{
                "cmap": "viridis",
                "crange": "mm",
                "title": "EC95"
            },
            "maxele:0":{
                "bbox": [-78,43.8,-76,44.4]
            },
            "minpr": "default"
        },

        "bbox":{
            "bbox": [-78,43.8,-75.5,44.7],
            "grd": "default",
            "maxele":{
                "cmap": "viridis",
                "crange": "mm",
                "title": "EC95"
            },
            "maxele:0":{
                "bbox": [-78,43.8,-76,44.4]
            },
            "minpr": "default"
        },

        "group":{
            "group":{
                "bbox": [-78,43.8,-76,44.4],
                "title":"Test Title"
            },
            "grd": "default",
            "maxele":{
                "cmap": "viridis",
                "crange": "mm",
                "title": "EC95"
            },
            "minpr": "default",
            "maxwvel": {
                "crange": ["s",-1.5,1.5]
            }
        }
    }




Specifying Models
=================

OPT files are designed to take into account specific models and datatypes associated with those models. To accomplish this, models are defined in ``settings.json`` and the opt file itself has its
model specified. To make this specification, either use the ``"models"`` keyword with a list of the contained models in the OPT itself or name the OPT file ``*_*_{model}_opt.json``. 

.. important::
    Currently, model specification is very ridged. ``"models"`` must be a or naming must follow the proper format. These requirements will be tweaked in the future. 

"fill" keyword
--------------

The ``"fill"`` keyword is used to further simplify the OPT files. It uses the datatypes defined in ``settings.json`` to fill a group if some datatypes are not defined. This can be 
controlled by using the ``"fill"`` keyword with a ``bool`` at the global or group level, by using the ``-n`` option on the command line, or by settling the ``fill`` kwarg in 
``vispipe.opt_reader``. This allows for very simple OPT files. If all that is needed is the default of all defined types in ``settings.json`` ``"opt"``, the opt would look like this:

.. code-block:: JSON
    :caption: The model name would be defined in the file name in this case.
    
    {
        "default": null
    }

.. seealso::
    :ref:`settings.json "opt"<uni_opt>`




Usage
=====

OPTs are not used directly by ``vispipe.vispipe``. They are first converted into a standard config dictionary by ``vispipe.opt_reader`` and the used by ``vispipe.vispipe``. ``vispipe.opt_reader``
only takes a path or a list of paths. From the command line this is no different from a normal config, with the addition of some other flags. Additionally, the ``-d`` flag can be used 
to write a config from the OPT file.

.. seealso::
    :ref:`Vispipe CLI<opt_cli>` for more information on terminal flags.

comandline vs functions




Generating Config
-----------------

kwarg and cli

