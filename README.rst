==============
dottorrent-gui
==============

An advanced GUI torrent file creator with batch functionality, powered by PyQt and
`dottorrent <https://github.com/kz26/dottorrent>`_

.. image:: img/screenshot1.png

--------
Features
--------

* Fast (capable of several hundred MB/s)
* Cross-platform
* Full Unicode support
* Automatic and manual piece size selection, up to 64MB
* Batch torrent creation mode
* Filename exclusion patterns
* HTTP/web seeds support `(BEP 19) <http://www.bittorrent.org/beps/bep_0019.html>`_
* Private flag support `(BEP 27) <http://www.bittorrent.org/beps/bep_0027.html>`_
* User-definable source string
* Optional MD5 file hash inclusion
* Import/export of profiles (trackers, web seeds, source string, filename exclusion patterns)

------------
Installation
------------

Windows
-------

Binary releases of stable versions for 64-bit Windows can be found at
`https://github.com/kz26/dottorrent-gui/releases <https://github.com/kz26/dottorrent-gui/releases>`_.
Extract to a folder and run ``dottorrent_gui.exe``.

Linux
-----

**Requirements**

* Python 3.3+
* PyQt5 5.7+

Latest stable release: ``pip install dottorrent-gui``

Development: ``git clone`` this repository, then ``pip install .``

To run: ``dottorrent-gui``

-------
License
-------

© 2016 Kevin Zhang. Made available under the terms of the
`GNU General Public License v3 <http://choosealicense.com/licenses/gpl-3.0/>`_.