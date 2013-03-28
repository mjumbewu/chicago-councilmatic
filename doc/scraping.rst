Using Scrapers with Councilmatic
================================

Councilmatic uses scrapers to gather legislative data. Originally there was only
one system supported.

All the data providers live in the ``phillyleg.management.scraper_wrappers.sources``
package (the top-level package is called ``phillyleg`` just because Councilmatic
was originally for Philadelphia; it should be renamed to ``legislation``).  They
are used by the `loadlegfiles` and `updatelegfiles` commands.  These commands
expect a certain API, and anything that adheres to that API can be used as a
data source.

Creating a new adapter
----------------------

A data adapter is a class that conforms to a certain interface:

* ``check_for_new_content``

  Check whether any new legislation has been released. Each piece of
  legislation will have a key denoting its index in some perfect ordering.
  The last key that was scraped should be stored in the DB. This key will be
  passed in to ``check_for_new_content`` by `updatelegfiles`.

  Return a 2-tuple containing the legislation key, and an object that can be
  used to retrieve the legislation content. If there are no new legislation,
  just return ``None, None``.

* ``scrape_legis_file``

  Given a legislation key and and retrieval object, return the legislation
  general attributes, the attachments, the action history, and the minutes.

  `record`
    - key
    - id
    - url
    - type
    - status
    - title
    - controlling_body
    - intro_date
    - final_date
    - version
    - contact
    - sponsors

  `attachments`
    -
