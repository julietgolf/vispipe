Settings Keyword Table
**********************

This table contains the built in keywords used in config files and settings.json. The following tags are used in the table:

- U: Usage specific to settings.json.
- G: Usage specific to ``"globals"`` in a config.
- P: Usage specific to ``"plots"`` in a config.
- O: Usage specific to opt files.
- F: Usage specific to a func dict.
- V: Indicates that key is passed as a value.

.. _pint units: https://github.com/hgrecco/pint/blob/master/pint/default_en.txt

+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| Keyword             | Description                                                                                                                                               | Example |
+=====================+===========================================================================================================================================================+=========+
| ``"format"``        | - U: Section in settings.json that contains options for input formats, i.e. ``"ascii"``.                                                                  |         |
|                     | - G: Optional value that tells vispipe what format will be used for inputs.                                                                               |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"default"``       | - ``"format"`` U: The default format used by vispipe.                                                                                                     |         |
|                     | - V: If passed instead of a dict in the plot section of a config the global and universal settings are used. Using the json keyword ``null`` is prefered. |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"grd"``           | Mesh type used for the default mesh if one is not ``"mesh"`` keyword is not provided.                                                                     |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"reader"``        | Used in settings.json to specify what reader function will be used to pull data from can be formatted in 2 ways.                                          |         | 
|                     |                                                                                                                                                           |         |
|                     | #. ``reader: {"name": "[modules,...].func", "args": [], "kwargs":{}, "mesh": bool}``                                                                      |         |
|                     | #. ``"[modules,...].func"``                                                                                                                               |         |
|                     |                                                                                                                                                           |         |
|                     | ``"mesh"`` in this context is a `bool` and detirmines whether a mesh is passed or not.                                                                    |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"plotter"``       | Used in settings.json to specify what plotting function will be used. Formatted the same as above with the addition of the ``"sig"`` keyword below.       |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"sig"``           | Sub-dictionary of ``"plotter"`` dictionary. Describes the function signiture of the plotting function what reader outputs and vispipe variables to use.   |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"stattable"``     | Specifies what function to use to add a table to the figure.                                                                                              |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"tables"``        | If ``true`` meshtools.plotters.stattable is used to add a table of statistics.                                                                            |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"mesh"``          | Used to specify the mesh associated with the data.                                                                                                        |         |
|                     |                                                                                                                                                           |         |
|                     | - F: A `bool` that detirmines if a plotter requires a mesh to plot against.                                                                               |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"unit"``          | Unit of measurement associated with data. Used as the label for the colorbar. Must be a                                                                   |         |
|                     | unit in pint's `pint units`_.                                                                                                                             |         |
|                     |                                                                                                                                                           |         |
|                     | - U: The default unit of measurement.                                                                                                                     |         |
|                     | - G,P: If different than the default pint will attempt to convert the data to the provided  unit.                                                         |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"title"``         | Title of the figure.                                                                                                                                      |         | 
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"titlepre"``      | Added to the front of title as "{titlepre} for {title}". If ``"title"`` is not present                                                                    |         |
|                     | it is used for the figure title alone.                                                                                                                    |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"minimum"``       | The keys that must be present for a plot to begin. If not all are found after the plot                                                                    |         |
|                     | dictionary is built the plot will be skipped.                                                                                                             |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"empty_value"``   | The value of a cell or node that never became wet. Used to mask out data.                                                                                 |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"base"``          | - U: References a base type to pull values from. Allows for common date to be contained instead of repeated.                                              |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"numreqs"``       | Number of records in a file that can be plotted. i.e. wave.out_max has ``"numreqs"`` of                                                                   |         |
|                     | three. All values unique to a record must be in a list of equal length to ``"numreqs"``.                                                                  |         |
|                     | Vispipe breaks the output up and plots them in separate processes.                                                                                        |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"type"``          | Used to associate a group of settings with a higher level group if they do not share                                                                      |         |
|                     | keys.                                                                                                                                                     |         | 
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"meshtype"``      | Used to associate a mesh that with a key other than ``"grd"`` with its universal                                                                          |         |
|                     | settings.                                                                                                                                                 |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| Backend Calls       | ``"subtitle"``, ``"xlabel"``, ``"ylabel"``, ``"xticks"``, ``"yticks"``, ``"aspect"``, ``"grid"``, ``"bbox"``, ``"set"``, ``"cbar"``                       |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"no_back"``       | If ``true`` the backend creates a ``fig`` and ``ax`` to be used by a plotting function. The backend calls above are ignored by ``vispipe``                |         |
|                     | unless specified in the plotters ``"sig"``.                                                                                                               |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``"models"``        | - O: Used to denote a mixed model opt file. Consists of a list of model names in the ``"opt"`` section of settings.json.                                  |         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+

 
#[ ] Update with new level merger and deflist