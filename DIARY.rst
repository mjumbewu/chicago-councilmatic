SOAP Suds
=========

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


Search and Subscriptions
========================

I had some pretty good momentum going.  I was hooking up the search views to
the subscription mixins.  This wasn't trivial, but was proving to be altogether
doable.  The issue: I want to continue to use class-based views in the project,
but haystack has its own view classes that preceded the core class-based views.
What I ended up doing was writing my own ``SearchView`` class that created and
called a haystack ``SearchView`` in the ``dispatch`` method::

    def dispatch(self, *args, **kwargs):
        # Construct and run a haystack SearchView so that we can use the
        # resulting values.
        self.search_view = haystack.views.SearchView(form_class=forms.SimpleSearchForm)
        self.search_view(*args, **kwargs)

        # The, continue with the dispatch
        return super(SearchView, self).dispatch(*args, **kwargs)

This way, I can still have acces to the ``search_view`` members that I want
(like ``form`` for the search form, and ``results`` for the search results).
And ``dispatch`` is the first point of contact that I care about in class-based
views anyway.

So, I derived from ``generic.ListView``, had ``get_queryset`` return the
``self.search_view.results``, and things seemed to be going alright, until I
hit this wall::

    You must not use 8-bit bytestrings unless you use a text_factory that can
    interpret 8-bit bytestrings (like text_factory = str). It is highly
    recommended that you instead just switch your application to Unicode
    strings.

What?  I mean, it's nice that it recommends that I switch my application to
unicode, but I have no idea why this happened.  Some light searching turns up a
couple of StackOverflow posts about sqlite3.  `This guy
<http://stackoverflow.com/questions/3425320/sqlite3-programmingerror-you-must-not-use-8-bit-bytestrings-unless-you-use-a-tex/3425465#3425465>`_
wants me to convert the value I'm inserting into the DB to a ``buffer`` object.
Unfortunately, I don't think I'm inserting anything when this happens.  So, the
solution doesn't apply for me.

While trying to debug the 8-bit thing, I ran into another issue. In order to
subscribe to a search, I had to find a portion of a haystack ``SearchQuerySet``
that would pickle without evaluating the search. Eventually I found that
``searchqueryset.query.query_filter`` would do it, and I could reconstruct a
queryset by just passing the resultant value back into ``SearchQuerySet(...)``.

And then, after that I ran into a disappearing ``object_list`` bug.  This time,
even though I was deriving from ``ListView``, and my context was being returned
with an ``object_list`` variable in it (I know because I logged it as such),
it was not showing up in the template context (debug_toolbar couldn't find it
either).  Turns out this was because I was calling the ``search_view``, or
specifically, because it was calling ``search_view.create_response()``.  As
soon as I restricted what i was calling to what I neede to  from ``search_view``
everything worked out fine.

So, finally, I was free to return to my 8-bit problem.  Or so I thought!  While
I wasn't looking, the problem fixed itself.  I don't know which bit of tinkering
made it go away, but it's gone.  And, while I'd prefer to know why, I won't
complain for now.
