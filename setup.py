from setuptools import setup, find_packages

setup(name='lime',
      version='0.1.1.32',
      description='Local Interpretable Model-Agnostic Explanations for machine learning classifiers',
      url='http://github.com/bivanalhar/lime',
      author='Bivan Alzacky Harmanto',
      author_email='bivan.alzacky@gmail.com',
      license='BSD',
      packages= find_packages(exclude=['js', 'node_modules', 'tests']),
      install_requires=[
          'numpy',
          'scipy',
          'scikit-learn>=0.18',
          'scikit-image>=0.12'
      ],
      include_package_data=True,
      zip_safe=False)

