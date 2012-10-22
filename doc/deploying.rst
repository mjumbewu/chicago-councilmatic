Deploying Councilmatic
======================

Deploying to DotCloud
---------------------

Councilmatic can be deployed easily to PaaS services such as DotCloud.  In the
case of DotCloud, the configuration files necessary are included in the project.

1. Create the instance.  This should be something like:

    dotcloud create councilmatic
    dotcloud push councilmatic

2. Specify where to get the council data from.  Right now, Councilmatic only 
   supports DayStar's InSite (Legistar) system.  Hopefully soon, there will be
   more systems supported.  The source root is the root URL where the files
   can be found.
   
    dotcloud var set councilmatic COUNCILMATIC_SOURCE_ROOT=http://legistar.baltimorecitycouncil.com/
  
   Councilmatic uses Google's geocoder to determine locations mentioned in 
   legislation.  To give the geocoder some help, you should give it a hint of
   where to look for addresses.  For example, there may be a 1234 Market St. in
   many cities, so we should help the geocoder out and give it a better chance
   of picking the right one.  The geocoder bounds should be a comma-separated
   list of four floating point numbers representing the top-left lat,lng, and
   the bottom-right lat,lng.
   
    dotcloud var set councilmatic COUNCILMATIC_ADDRESS_BOUNDS=39.222146926442235,-76.81571960449219,39.386059865628575-76.46690368652344

