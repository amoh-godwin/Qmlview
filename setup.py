from setuptools import setup, find_packages
setup(
    name="Qmlview",
    version="1.0",
    packages=find_packages(),
    install_requires=['PyQt5 >= 5.10'],
    entry_points={
            'console_scripts': ['qmlview = Qmlview.qmlview:main_run'],
    },
    
    author="Amoh - Gyebi Godwin Ampofo Michael",
    author_email="amohgyebigodwin@gmail.com",
    description="An alternative to qmlscene",
    keywords="qmlscene, ninja-preview, qml, pyqt, pyqt5, pyside, pyside2",
    url="https://github.com/amoh-godwin/Qmlview",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/amoh-godwin/Qmlview/issues",
        "Documentation": "https://github.com/amoh-godwin/Qmlview/wiki",
        "Source Code": "https://github.com/amoh-godwin/Qmlview",
    },
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    long_description = """\
    Qmlview is a command line utility. But sort of to replace the non-existent
    qmlscene, which was used to preview qml source code before it is loaded
    by any C++, Java, or python code.
    """
)
