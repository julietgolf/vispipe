Vispipe Terminal Command
########################


Vispipe comes with a built in terminal command that allows for vispipe to be called from outside a Python script.
The command has fa number of flags that control the kwargs of ``vispipe()``. Additionally, ``vispipe -o`` and 
associated flags allows for .opt files to be read dirrectly.


``vispipe()`` kwarg flags
*************************

.. list-table::
    :widths: auto
    :header-rows: 1

    * - Flag
      - Long Flag
      - Description
      - Action
      - Default
    * - p 
      - pdf 
      - Generates a pdf. Sets images to False.
      - store_true 
      - False
    * - i
      - image
      - Toggles if \*/pngs is kept. Keeps \*/pngs at the end of the run if -p is called.
      - store_false
      - True
    * - c
      - compress
      - Compress \*/pngs to a .tar.gz. Sets images to False.
      - store_true
      - False
    * - v
      - verbose
      - store_const, 10
      - Show debugging messages.
      - 30

``opt_reader()`` kwarg flags
****************************

.. list-table::
    :widths: auto
    :header-rows: 1

    * - Flag
      - Long Flag
      - Description
      - Action
      - Default
    * - o
      - opts
      - Read in an opt file instead of a json.
      - store_true
      - False
    * - f
      - filepre
      - Common file prefix for all data files.
      - 
      - ""
    * - t
      - titlepre
      - Common title prefix for all plots.
      -
      - ""
    * - n
      - nofill
      - Does not add missing datatypes to groups from deflist or settings.json.
      - store_false
      - True
    * -
      - specname
      - Key value pairs of non standard file name for a type. Input looks like 'key0 val0 key1 val1 ... keyn valn'.
      - 
      - None
    * - d
      - dump
      - Dumps opt into a opt.json. Does not run ``vispipe()``.
      - store_true
      - False

Swap Settings
*************

.. list-table:: 
    :widths: auto
    :header-rows: 1

    * - Long Flag
      - Description
      - Action
      - Default
    * - swap_settings
      - store_true
      - Add a custom \"settings.json\". Old files are renamed in vispipe dir.
      - False
