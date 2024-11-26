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

As stated the structure of an OPT is largely the same as the config. The OPT shares its `"globals"` field with
the :ref:`config's "globals"<globals>`, with the exception that `"paths"` are excluded since they will be generated.
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
    :emphasize-lines: 





Specifying Models
=================

OPT files are designed to take into account specific models and datatypes associated with those models. To accomplish this, 


"models"
--------

"fill" keyword
^^^^^^^^^^^^^^

Fills with all defined in settings

.. seealso::
    :ref:`settings.json "opt"<uni_opt>`


Empty OPTs
----------

Uses fill and model names

Usage
=====

Basic

naming

comandline vs functions

Multiple Models
---------------

Opt_reader will pick up on them.

Generating Config
-----------------

kwarg and cli
