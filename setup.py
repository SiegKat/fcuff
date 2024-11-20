import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'fcuff',
  version = '0.0.1',
  description = 'Análise e processamento de dados de experimentos com célula combústivel e eletrolizadores',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/SiegKat/fcuff',
  author = 'Thiago Costa',
  author_email = 'tabrantedaco2023@fau.edu',
  license = 'MIT',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3'
  ],
  keywords = ['electrochemistry', 'fuel cell', 'electrolyzer'],
  packages=setuptools.find_packages(),
  python_requires='>=3.13',
  install_requires=['numpy', 'pandas', 'matplotlib', 'scipy', 'PySide6', 'PyQT6'],
  project_urls={
    'Documentation': 'https://siegkat.github.io/fcuff/',
    'Source': 'https://github.com/SiegKat/fcuff'
  }
)
