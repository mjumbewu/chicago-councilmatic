As ugly as SOAP is, SUDS makes it wonderfully painless.  Just point it at a WSDL
file URL and let it rip!

Ok, that's not exactly what happened.  At first I was getting strange errors
that I couldn't make sense of.  First I got this one::

    suds.TypeNotFound: Type not found: '(schema, http://www.w3.org/2001/XMLSchema, )'

But StackOverflow came to my rescue with `this little gem
<http://stackoverflow.com/questions/1329190/python-suds-type-not-found-xscomplextype/1360535#1360535>`_.
I also got the following error on some requests::

    WebFault: Server raised fault: 'Server was unable to process request. ---> Object reference not set to an instance of an object.'

It appears that my problem here was that did not know how to construct complex
objects to send.  Some of the methods in this particular service require an
``Options`` structure.  I saw this by doing::

    >>> print client
    #
    #  Suds ( https://fedorahosted.org/suds/ )  version: 0.4 GA  build: R699-20100913
    #
    #  Service ( Main ) tns="http://legistar.com/"
    #     Prefixes (1)
    #        (MainSoap)
    #           Methods (176):
    #              ...
    #              BodyGetAll(xs:string PartnerGUID, xs:string GovernmentGUID, BodyOptions Options, )
    #              ...
    #           Types (253):
    #              ...
    #              BodyOptions
    #              ...

With a little more exploring, I found that the ``client`` object has a method
named ``factory`` (NOTE: using ``dir(...)`` on your objects works, but something
like `bpython <http://bpython-interpreter.org/>`_ is great for exploring.  To
get bpython running in a virtualenv session, run::

    python -m bpython.cli

Thanks `Ronny Pfannschmidt <http://groups.google.com/group/python-virtualenv/browse_thread/thread/4c9d88177caf7fa8#msg_1efc437afc2a89b1>`_).
So, using ``options = client.factory('BodyOptions')`` and settting the values
in ``options`` did the trick.

Anyways, once I set up my ``client`` correctly, it went pretty smoothly.  The
API isn't all that well documented, so I have to feel my way around and discover
what things mean.
