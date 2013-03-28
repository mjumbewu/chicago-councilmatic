Maintenance and Administration
==============================

Once you have your scrapers configured, the bulk of the data in Councilmatic
should update itself. There are a few things that must be done manually for
now.

Loading Council Districts
-------------------------

Every so often, the way that a city is carved up into representative districts
is reconfigured. When this is done, you'll need to import the new district data
into Councilmatic. There is no nice way to do this.

**TODO: It would be great to have an extension for GeoDjango's admin that
        allowed you to upload a GeoJSON file into a model, or allowed you to
        point at a GeoJSON URL that was already out on the internet. Any
        takers?**

So, for now, you'll have to do this manually. Fortunately, it's not too hard.
I'm no GIS expert, and I manage to do it. I couldn't give detailed instructions
for every GIS data format. Generally though, what you'll want to do is start up
a management shell (``councilmatic/manage.py shell``), import your district GIS
data, create a ``CouncilDistrictPlan`` model instance for this district plan,
and create ``CouncilDistrict`` model instances for each of the district shapes
in your data.  For example::

    >>> from datetime import date
    >>> from phillyleg.models import CouncilDistrictPlan, CouncilDistrict
    >>>
    >>> districts_data = ...  # Do the magic to import your GIS data
    >>>
    >>> plan = CouncilDistrictPlan.objects.create(
    ...     date = date('2012-01-01')  # The date that the plan takes effect
    ... )
    >>>
    >>> for district_data in districts_data:
    ...     district = CouncilDistrict()
    ...     district.plan = plan
    ...     district.id = district_data['district number']
    ...     district.shape = district_data['shape as a GEOS object']
    ...     district.shape.srid = district_data['SRID of the imported data']
    ...     district.shape.transform(4326)
    ...     district.save()
    >>>

After you've done that, you'll want to set the tenures of your councilmembers.
In the Django admin, under the *Phillyleg* heading, select *Council Members*.
In each council member's admin page, there is a section to add council tenures
for that member.


Invalidating Locations
----------------------

The address and location parser is far from perfect, and it will pick up a few
false positives -- things that it thinks are locations but are not. When this
happens, if you delete the location then it could be read again in the future,
and you'll have to delete it each time it comes up. Instead, when you find an
invalid location, mark it as invalid (there is a ``valid`` attribute) so that
the next time it is parsed, it remains invalid.
