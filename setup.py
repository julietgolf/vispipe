from setuptools import setup 

REQUIREMENTS = ["numpy","pint","PyMuPDF","netCDF4","matplotlib"]

CLASSIFIERS = [ 
    'Development Status :: Beta', 
    'Intended Audience :: Developers', 
    'Programming Language :: Python', 
    'Programming Language :: Python :: 3.9+', 
    ] 

setup(name='vispipe', 
      version='1.0.0', 
      description='Visulisation Pipline', 
      author='Joshua Dante Gramm', 
      author_email='joshua.d.gramm@usace.army.mil', 
      package_dir={"vispipe":"src/vispipe"},
      packages=["vispipe"], 
      classifiers=CLASSIFIERS, 
      install_requires=REQUIREMENTS,
      entry_points={"console_scripts":["vispipe=vispipe.vispipe_cli:main"]},
      include_package_data=True
      )


#plot_backend
#   opt_reader
#   options
#   gridedit
