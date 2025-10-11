## Multi Store

An store is an organizational entity that could be part of a company or not (cross to all companies).

This module add a new concept "stores" in some point similar to multicompany. Similarities:

1. User can have multiple stores available (store_ids)
2. User can be active only in one store (store_id) which can be set up in his own preferences
3. There is a group "multi store" that gives users the availability to see multi store fields

It is intended to be used for:
- security reazons, for eg. limit users to some journals
- information, for eg. sales by shop

Only a few models are directly linked (Direct Linked Models) to shops (for eg. journals and warehouses). The other models are linked by a related field (Related Linked Models) to those models (for eg. the invoice store comes from the journal store)

Security rules for models (in generally):

1. Direct Linked Models:
   - Records can only see if same store or not store set, this is done this way so they can not choose none autorhized records on M2O fields

2. Related Linked Models:
   - Records can be seen by everyone, no matters the store
   - Create, unlink and write is only allow if same store or not store set
