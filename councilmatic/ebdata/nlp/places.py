#   Copyright 2007,2008,2009,2011 Everyblock LLC, OpenPlans, and contributors
#
#   This file is part of ebdata
#
#   ebdata is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   ebdata is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with ebdata.  If not, see <http://www.gnu.org/licenses/>.
#

import re

"""
Factories that return 'grabber' and 'tagger' functions, for finding
and marking up text that looks like...  well, anything, but in this
context we are typically looking for names of db.Locations and
db.Places.

In each case, the factory is passed a list of strings to treat as
phrases to match, and returns a function that takes a ``text`` argument.

'Tagger' functions return text where each matched phrase is replaced
by itself wrapped in the ``pre`` and ``post`` arguments.

'Grabber' functions return a list of 3-tuples, each of the form
(start, end, phrase), where ``phrase``v is the text that was matched,
and ``start`` and ``end`` are the indexes of where that text was found
in the original text.

'paranoid' means whether you care about avoiding nested tags.
e.g. you might not want to create <span>South<span>Boston</span></span>.
Longer phrases will be matched before shorter phrases.

TODO: docstrings for each of these
"""

def loose_phrase_grabber(phrases):
    """
    Given a list of strings ('phrases'), returns a phrase grabber
    function that does not care about markup around phrases.
    """
    def grab_phrases(text):
        phrases.sort(key=len, reverse=True)
        tags = []
        def handle_match(m):
            # Note the start & end positions,
            # and take care to preserve the length of the input
            # by replacing the match with whitespace.
            tags.append((m.start(), m.end(), m.group()))
            return ' '*(m.end() - m.start())

        for phrase in phrases:
            # don't bother buiding and exhaustively searching unless
            # we at least weakly see this phrase in the text, 
            # re compiling and searching is not cheap added up 
            # over all locations.
            if phrase in text:
                text = re.sub(r'\b%s\b' % phrase, handle_match, text)

            # TODO: we could actually do this in linear time entirely without
            # regexes. (str.find is average linear)
            # something like (UNTESTED):
            # start = 0
            # while True:
            #     start = text.find(phrase, start)
            #     if start == -1:
            #         break
            #     end = start + len(phrase)
            #     tags.append((start, end, phrase))
            #     start += 1
            # text = text.replace(phrase, ' ' * len(phrase))
            # Would need to profile that though.
        tags.sort()
        return tags

    return grab_phrases

def paranoid_phrase_grabber(phrases, pre, post):
    """
    Returns a phrase grabber function that ignores occurrences of the phrases
    within the pre / post tags.
    """
    def handle_match(m):
        # Unlike a normal re.sub(), this allows the replacement to have
        # dynamic length.
        return ' ' * len(m.group())
    nuke_tags = re.compile('%s.*?%s' % (re.escape(pre), re.escape(post)))
    loose_grabber = loose_phrase_grabber(phrases)

    def grab_phrases(text):
        text = nuke_tags.sub(handle_match, text)
        return loose_grabber(text)

    return grab_phrases

def phrase_tagger(phrases, pre='<span>', post='</span>', paranoid=True):
    """Returns a phrase tagger function.
    If ``paranoid==True``, avoids tagging inside existing tags.
    """
    if paranoid:
        grabber = paranoid_phrase_grabber(phrases, pre, post)
    else: 
        grabber = loose_phrase_grabber(phrases)

    def tag_phrases(text):
        out_text = []
        curpos = 0
        for tag in grabber(text):
            out_text += [text[curpos:tag[0]], pre, tag[2], post]
            curpos = tag[1]
        out_text.append(text[curpos:])
        return ''.join(out_text)

    return tag_phrases

