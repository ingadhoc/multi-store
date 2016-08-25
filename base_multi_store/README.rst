===========
Multi Store
===========

An store is an organizational entity that could be part of a company or not (cross to all companies).

This module add a new concept "stores" in some point similar to multicompany. Similarities:

* User can have multiple stores available (store_ids)
* User can be active only in one store (store_id) which can be set up in his own preferences
* There is a group "multi store" that gives users the availability to see multi store fields

It is intended to be used for:

* security reazons, for eg. limit users to some journals
* information, for eg. sales by shop

Only a few models are directly linked (Direct Linked Models) to shops (for eg. journals and warehouses). The other models are linked by a related field (Related Linked Models) to those models (for eg. the invoice store comes from the journal store)

Security rules for models (in generally):

* Direct Linked Models:
    * Records can only see if same store or not store set, this is done this way so they can not choose none autorhized records on M2O fields

* Related Linked Models:
    * Records can be seen by everyone, no matters the store
    * Create, unlink and write is only allow if same store or not store set

#. Just install it

Configuration
=============

To configure this module, you need to:

#. Go to Configuration / Companies / Stores
#. Create and set up your stores

Usage
=====

To use this module, you need to:

#. Select on your preferences on wsich store you are working on
#. Analyze your information grouping and filtering by store field

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.adhoc.com.ar/

.. repo_id is available in https://github.com/OCA/maintainer-tools/blob/master/tools/repos_with_ids.txt
.. branch is "8.0" for example

Known issues / Roadmap
======================

* ...

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

* ADHOC SA: `Icon <http://fotos.subefotos.com/83fed853c1e15a8023b86b2b22d6145bo.png>`_.

Contributors
------------


Maintainer
----------

.. image:: http://fotos.subefotos.com/83fed853c1e15a8023b86b2b22d6145bo.png
   :alt: Odoo Community Association
   :target: https://www.adhoc.com.ar

This module is maintained by the ADHOC SA.

To contribute to this module, please visit https://www.adhoc.com.ar.
