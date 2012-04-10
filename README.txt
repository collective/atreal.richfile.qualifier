.. contents::

Overview
========

System to enrich a file content type in Plone with a marker interface
regarding its mimetype.


Description
===========

Please note that ``atreal.richfile.qualifier`` is a Plone component for
developers. Do not expect anything more in your Plone site if you don't use
Plone components that may use ``atreal.richfile.qualifier``, such as:

* atreal.richfile.filepreview_
* atreal.richfile.streaming_
* atreal.richfile.metadata_
* atreal.richfile.image_
* ...

.. _atreal.richfile.filepreview: http://pypi.python.org/pypi/atreal.richfile.filepreview
.. _atreal.richfile.streaming: http://pypi.python.org/pypi/atreal.richfile.streaming
.. _atreal.richfile.metadata: http://pypi.python.org/pypi/atreal.richfile.metadata
.. _atreal.richfile.image: http://pypi.python.org/pypi/atreal.richfile.image


``atreal.richfile.qualifier`` works on Plone 3 with ATFile and on Plone 4 with
ATFile and ATBlob. You can easily configure your own file content type: ::

    <five:implements
        class="Products.ATContentTypes.content.file.ATFile"
        interface=".interfaces.IFileQualifiable"
        />


Control Panel
=============

Few options are avalaible in the Control Panel :

* 'Update all contents': will update all contents of the portal supported by
  this plugin.
* 'Clean all datas': will clean datas created by this plugin, for each
  supported content of the portal.

Important: These operations will take a while, and may slow down the site
significantly while the content is updated.

Important: These operations search by the interface provided by the content in
portal_catalog, so if you already have contents in your site when you install
this package, you have to update 'object_provides' index first.

Important Notes
===============

The version 1.1.1 of atreal.richfile.qualifier is not Plone 3 compatible ! Please
use version 1.1.2 instead.

Authors
=======

|atreal|_

* `atReal Team`_

  - Thierry Benita [tbenita]
  - Matthias Broquet [tiazma]
  - Florent Michon [f10w]

.. |atreal| image:: http://www.atreal.fr/medias/atreal-logo-48.png
.. _atreal: http://www.atreal.fr/
.. _atReal Team: mailto:contact@atreal.fr


Contributors
============

* `atReal Team`_

  - Romain BEYLERIAN [rbeylerian]

.. _atReal Team: mailto:contact@atreal.fr


Credits
=======

* Sponsorised by City of Albi (France), http://www.mairie-albi.fr/

