Adding Custom Functions
***********************

Vispipe allows the user to add custom readers, plotters, and stattables. These functions are contained in function 
dictionaries. They are placed in a datatype in either the config file or the ``settings.json`` with the keys "readers",
"plotters", or "stattables". 

Function Dictionaries
^^^^^^^^^^^^^^^^^^^^^

These dictionaries have 3 common keywords: ``"name"``, ``"args"``, ``"kwargs"``. The ``"name"`` is a ``str`` 
of either one of the names of the built in plotters or "module.submodule.func". ``"args"`` is a ``list`` are static 
args that are normally added at the end of any dynamically defined args. ``"kwargs"`` is a ``dict`` of predefined 
kwargs. Plotter dictionaries have two extra keywords. ``"mesh"`` tells ``"vispipe"`` whether to pass the mesh to the 
plotting process and ``"sig"``, which is shared with stattables dictionaries, maps the output of the reader to the 
input of the plotter or stattable. 

.. code-block:: JSON
    :caption: Function dictionary for a generic plotter.

    "plotter": {
        "name": "module.plotter",
        "args":[ "arg0", "arg1", "argn" ],
        "kwargs":{ "key0":"val0", "key1":"val1", "keyn":"valn" },
        "mesh": true
        }


``"sig"``
^^^^^^^^^

``"sig"`` is a dictionary that describes the input of the plotter or stattable. The ``"sig"`` dictionaries are parsed by 
``vispipe._vispipe._read_sig()`` which maps the output of the reader, config, and local variables to their proper position
in the input args and kwargs. Other than the keys in the table below, keys in this dictionary are for readability only. 


.. list-table:: ``"sig"`` Named Keys
    :widths: auto
    :header-rows: 1

    * - Key
      - Description
    * - ``"*"``
      - This key tells ``_read_sig()`` to stop parsing inputs as positional arguments. If the item is ``null``, ``_read_sig()`` 
        moves onto keyword variables. Otherwise, it treats it like it is a ``int`` or ``"vp:*"`` input.
    * - ``"**"``
      - Functions the same as ``"*"`` but for keyword arguments.
    * - ``"exclusive"``
      - If included and ``True``, no other arguments from the config will be added.


Internally, the reader outputs to a variable named ``vals``. If the reader has multiple outputs, the ``vals`` becomes a 
``tuple``. ``"sig"`` can reference ``vals``, values defined in the config and ``settings.json``, and local variables in 
``_pipeline()`` to order the function input. The table below describes how different values in ``"sig"`` work.

.. list-table:: ``"sig"`` Values
    :widths: auto
    :header-rows: 1

    * - Value
      - Description
    * - ``int``
      - Take the member of ``vals`` at the index of the given value. 
    * - ``"vp:*"``
      - Values with the prefix ``"vp:"`` will first search the config for a key that matches the suffix of the value 
        in ``"sig"``. If one is not found, ``locals()`` is then searched. Some important named variables are ``"vp:vals"``,
        ``"vp:mesh"``, ``"vp:plotargs"``, and ``"vp:plotkwargs"``.
    * - ``list``
      - When a ``list`` of above types is passed, the result is a ``list`` of the searches done by iterating over the given list. 

.. code-block:: JSON
    :caption: Example plotter dictionary with ``"sig"``.

    "plotter": {
        "name": "module.plotter",
        "args":[ "arg0", "arg1", "argn" ],
        "kwargs":{ "key0":"val0", "key1":"val1", "keyn":"valn" },
        "mesh": true,
        "sig": {"data": 0, "mesh": "vp:mesh", "*": null, "boundaries": 2, "**": "vp:plotkwargs"}
        }

.. warning:: 
    ``"args"`` can cause conflicts with ``"sig"`` when ``*args`` is not present in the function's signature. This 
    generally occurs in 2 ways. If a function limits the number of positional arguments with ``*`` in its signature,
    a ``TypeError`` can be triggered by passing too many positional arguments. When ``*`` is absent, the members of 
    ``"args"`` can role into keyword arguments. This has the potential to cause a ``SyntaxError`` if a keyword is 
    defined somewhere else.

Inheritance
^^^^^^^^^^^

Inheritance on function dictionaries works much the same way as datatype inheritance in config files. If a datatype 
higher in the stack has a function defined that shares a name with one defined lower, the ``"kwargs"`` will inherit 
any ``"kwargs"`` lower in the stack that are undefined. All other fields are directly inherited.
