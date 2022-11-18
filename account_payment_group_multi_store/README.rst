.. |company| replace:: ADHOC SA

.. |company_logo| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-logo.png
   :alt: ADHOC SA
   :target: https://www.adhoc.com.ar

.. |icon| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-icon.png

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==============================
Multi Stores on Payment Groups
==============================

Add stores on payment group to:
* Compute debt only of that store
* Filter journal on payments for that store
* If payment groups are created from somewhere else the store_id will be computed from payment if all the payments are from same store (no restrictions for now)

May be on the future we can also add integration to receiptbooks

TODO: por el momento no está mejorado que al querer agregar apuntes contables se filtre tmb por ese dominio porque requiere re-escribir el dominio de to_pay_move_line_ids, tal vez en v16+ podamos cambiar y que ese dominio venga definido por un campo calculado o algo mas heredable


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: http://runbot.adhoc.com.ar/

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/ingadhoc/{project_repo}/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* |company| |icon|

Contributors
------------

Maintainer
----------

|company_logo|

This module is maintained by the |company|.

To contribute to this module, please visit https://www.adhoc.com.ar.
