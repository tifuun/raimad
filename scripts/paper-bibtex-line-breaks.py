#!/usr/bin/env python3
"""
Evil cursed regex shennanigans to make bibliography look the way I want it to.

RUN AFTER scripts/paper-bibtex-tidy.sh OTHERWISE WONT WORK
"""

import re

def breaklines(match):
    spacewidth = 1
    tabwidth = 8
    numtabs = 2
    maxlinelen = 80

    indent, field, opening, text, closing = match.groups()

    if match.span()[1] - match.span()[0] < maxlinelen or field in {
            'url', 'eprint'}:
        return match.string[match.span()[0]:match.span()[1]]

    words = text.split(' ')
    lines = [[]]
    linelen = 0
    while words:
        word = words.pop(0)
        if field == 'author' and word == 'and':
            lines.append(['and'])
            lines.append([])
            linelen = 0
            continue
        elif linelen + len(word) + spacewidth + tabwidth * numtabs > maxlinelen:
            lines.append([])
            linelen = 0
        lines[-1].append(word)
        linelen += len(word) + 1
    return '\n'.join((
            f"{indent}{field} = {opening}",
            *(
                f'\t\t{' '.join(line)}' for line in lines
                ),
            f"\t{closing}",
        ))

with open('paper/paper.tidy.bib') as f:
    bib = f.read()

bib = re.sub(
    r'(\s+)(\w+) = ({+)([^}]*)(}+)',
    breaklines,
    bib
    )

with open('paper/paper.bib', 'w') as f:
    f.write(bib)
