.. VisPipe documentation master file,
   contain the root `toctree` directive.
   #[ ] Make a doc that describes setting inheritance more in depth.

VisPipe
=======
.. _pypi: https://pypi.org/project/vispipe/
.. _github: https://github.com/julietgolf/vispipe
.. _CSTORM: https://www.erdc.usace.army.mil/Media/Fact-Sheets/Fact-Sheet-Article-View/Article/476697/

Project Links: `GitHub Repo <github_>`_ | `PYPI <pypi_>`_

The Visualization Pipeline (VisPipe) is a package designed to handle scripted batch visualization.  
Originally designed for use with `Coastal Storm Modeling System (CSTORM) <CSTORM_>`_ for use on high 
performance computers, it was spun off to be a standalone package for use on local systems 
and HPCs. 

:doc:`JSON files</guides/config>` are used to predefine data sources and and plot settings. The settings used in the JSON
corelate directly to the inputs used by the functions used to read and plot data. This allows for a 
high degree of customization and allows for a large amount of plug and play. These files allow for 
VisPipe to be used used in workflows not built in Python. As an example, CSTORM is built largely in
Bash and Fortran. If the data exists in a Python workflow the a raw dictionary can be passed 
directly to :func:`vispipe.vispipe` instead of reading a JSON config file. 

VisPipe is packaged with a :doc:`Matplotlib backend</reference/plot_backend/MPL_Figure>` that has 
ready to use plotters. Custom plotting function can be :doc:`added</guides/funcdict>` to enable more
complex plots. Additionally, the entire backend is designed to be swappable, giving the user the
ability to use a different plotting function.


.. toctree::
   :maxdepth: 2
   :caption: Documentation Table of Contents

   guides/index
   reference/index


