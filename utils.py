import re

q_re = re.compile(r'(<?https?://www.wikidata.org/entity/)?(Q[0-9]+)>?')
p_re = re.compile(r'(<?https?://www.wikidata.org/entity/)?(P[0-9]+)>?')

def to_q(url):
    """
    Normalizes a Wikidata item identifier

    >>> to_q('Q1234')
    u'Q1234'
    >>> to_q('<http://www.wikidata.org/entity/Q801> ')
    u'Q801'
    """
    if type(url) != str:
        return
    match = q_re.match(url.strip())
    if match:
        return match.group(2)

def to_p(url):
    """
    Normalizes a Wikidata property identifier

    >>> to_p('P1234')
    u'P1234'
    >>> to_p('<http://www.wikidata.org/entity/P801> ')
    u'P801'
    """
    if type(url) != str:
        return
    match = p_re.match(url.strip())
    if match:
        return match.group(2)

