---
title: 'RAIMAD: Collaborative Development of On-Chip Astronomical Instruments'
tags:
  - Python
  - Astronomy
  - CAD
authors:
  - name: Nikita Soshnin
    orcid: "0009-0000-6638-5087"
    corresponding: true
    affiliation: "1"
  - name: Akira Endo
    orcid: "0000-0003-0379-2341"
    affiliation: "1"
  - name: Kenichi Karatsu
    orcid: "0000-0003-4562-5584"
    affiliation: "2"
  - name: Louis Marting
    orcid: "0009-0001-1747-9906"
    affiliation: "1"
  - name: Arend Moerman
    orcid: "0000-0002-0475-6134"
    affiliation: "1"
  - name: Leon Olde Scholtenhuis 
    orcid: "0000-0002-7115-6366"
    affiliation: "1"
affiliations:
  - name: >
        Faculty of Electrical Engineering,
        Mathematics and Computer Science,
        Delft University of Technology,
        Mekelweg 4, 2628 CD, Delft, The Netherlands
    index: 1
  - name: >
        SRON Netherlands Institute for Space Research,
        Niels Bohrweg 4, 2333 CA Leiden,
        The Netherlands
    index: 2
date: 18 February 2025
bibliography: paper.bib
---

\newcommand{\raimad}{\texttt{RAIMAD}}
\newcommand{\raidoc}{\texttt{RAIDOC}}
\newcommand{\raidex}{\texttt{RAIDEX}}
\newcommand{\pip}{\texttt{pip}}

\Huge THIS IS A VERY EARLY DRAFT IM JUST WRITING WHAT POPS INTO MY HEAD \normalsize

<!-- REQUIRED SECTION!! -->
# Summary

<!-- keep!! -->
\raimad is a parametric 2D computer aided design (CAD) program
that is optimised for the creation of mask files for on-chip
astronomical instruments,
such as spectrometers and cameras.

<!-- 
    this seems like a mishmash of different sections, but no,
    this is good  i think -- give overview of all the big ideas,
    then dug down deeper in the sections
-->
\raimad comes with a library of built-in
geometrical primitives,
including rectangles, circles, and arcs.
Users can combine these primitives into individual
components,
such as bandpass filters [@alejandro], waveguides,
and kinetic inductance detectors [@mkids-day-actual].
These components can then be assembled into a
complete mask file for an astronomical instrument.
This modular approach allows for
streamlined collaboration
and enables reuse of existing components among different
instruments.

<!--
    Same here -- CIF is not a technical detail,
    this part explains what RAIMAD actually produces.
    Just tucked the cif citation in here because
    we don't have a separate "output format"
    section where this can be elaborated
    (i think such a section would be iirelevant/too technical)
-->
\raimad designs can be exported as a \texttt{.cif}
(Caltech Intermediate Form)
file [@cif],
a format for storing mask files.
Using these files, a process engineer is
able to transfer the design onto the desired
substrate using general lithography techniques.

<!--
    TODO need MODULAR approach here already -- this is a big
    design decision and one that we arrived at after stumbling
    into pretty much every possible pitfall.
-->
\raimad components are created using Python [@python] code,
which allows for both simplicity and flexibility.
\raimad itself is written in pure Python,
making it easy to use on all major desktop operating systems.
In order to allow users to share visual previews of their designs,
a web-based component directory called \raidex has been developed.
The name \raimad
is a recursive acronym that stands
for \texttt{RAIMAD Astronomical Instrument MAsk Designer}.

<!-- REQUIRED SECTION!! -->
# Statement of Need

The development of \raimad was initiated in order to fulfill the needs in the
TIFUUN (Terahertz Integral Field Units with Unified Nanotechnology) project
[@tifuun; @nishimura], to quickly design
integral field units (IFUs) that are tailored to each astronomical science
question as open-hardware [@openhardware].
Previously, a small number of integrated superconducting
spectrometer chips were designed for TIFUUN's precursor project,
DESHIMA (Deep Spectroscopic High-redshift Mapper) [@deshima1; @deshima2],
using an internally developed script.
While that script proved to be a capable solution for the task at hand,
its narrow scope and reliance on the
end-of-life Python 2 made it unsuitable for use in TIFUUN.
\raimad aims to build on the success of the script used in DESHIMA
while also adhering to standard Python practices,
such as the PEP8 style guide and
relevant packaging conventions.
Furthermore, the Ruff linter [@ruff] and MyPy static checker [@mypy] are
employed to ensure code quality.

\raimad aims to be useful to the broader scientific community
by enabling collaboration through its modular approach to design.
All \raimad components have a uniform Python interface,
which streamlines the process of incorporating
freely available components into a novel design.
Existing components can be discovered in \raidex
and installed trivially
using `pip`, Python's standard package manager.
This fosters an accessible environment with a low barrier of entry.

<!-- REQUIRED SECTION!! -->
# State of the field

\raimad seeks to enrich
the growing ecosystem of analogue circuit CAD software
by focusing on the specific niche
of on-chip astronomical instrumentation.
To this end,
it draws key design inspirations from two existing programs with
similar goals: Qiskit Metal and KLayout.

Qiskit Metal is a software platform for quantum device design [@qiskit].
Conceptually, it shares many similarities with \raimad,
however its component library is geared towards quantum computing.
We determined that developing \raimad from scratch
would allow us more flexibility in implementation
compared to retrofitting Qiskit
for our specific use case.

KLayout is a mask file viewer and editor [@klay].
One notable strength of its Salt package manager is
its support for a wide variety of package formats,
including Ruby macros, fonts, and binary extensions.
In \raimad, we instead decided to establish a single uniform
interface for all components in order to reduce complexity.

<!-- -----NEW------ REQUIRED SECTION!! -->
# Software design
<!-- TODO style -->
The design of \raimad is good because
we arrived at it after srumbling head-first into every possible
bad design decision.

We have a modular component system:
every raimad design adheres to the same "compo" interface,
and compos can be put together to make larger compos.
This is important because it allows people to understand each
other's code more easily.
Instead of getting a zip with tons of random functions and classes,
we have compos.
Everyone knows what a compo is.
So it helps collaboration
by reducing the onboard time.

We take inspiration from python's gradual typing.
Compo authors can add annotations describing
what their classes contain (marks, layers, options),
that are human- and machine-parseable,
but they don't have to.
So an author can first write a compo quickly,
refine it,
and then add structured documentation using these annotations,
much like python's type hints.
Potentially, this can also be used to catch bugs early thru static analysis,
liky python's mypy.
We even had a demo of this.

Finally, we take inspiration from functional programming.
Compos are immutable.
Transformations are done using proxies,
which transfrom the coordinate system and layer mappings of compos that
stay the same.
The reason we do this is for optimizations:
to produce leaner CIF files.
But this is not implemented yet.
Oh well.


<!-- -----NEW------ REQUIRED SECTION!! -->
# Research Impact Statement
Some amazing people are doing amazing things with raimad.
But I don't really know the details.
Time to ask around!!

<!-- -----NEW------ REQUIRED SECTION!! -->
# AI usage disclosure
<!-- TODO style -->
\raimad makes limited use of AI-generated code.
Some functions regarding coordinate transformations
and test fixtures has been written using publically available
large language models.
All AI-generated code has been proof-read and edited by the author
to ensure it does what it needs to,
and that its code style is consistent with the rest of the project.
All code that originated from AI is clearly labeled using comment blocks.

<!-- non-required section... -->
# Availability

\raimad can be found on
[GitHub](https://github.com/tifuun/raimad)
and is available for any platform that
supports CPython,
including Linux, Mac OS, and Windows.
Documentation, installation instructions,
and contributor guidelines can be found on
the [\raidoc site](https://tifuun.github.io/raidoc/),
which also includes tutorials
and sample code.
Existing \raimad components are
tracked in [\raidex](https://tifuun.github.io/raidex/).

<!-- non-required section... -->
# Acknowledgements

We would like to thank Christiaan Slieker,
Dr. Ilke Ercan, and Martine van der Laag-Hoogendijk
of Delft University of Technology
for helping resolve administrative issues
in the early stages of RAIMAD development.

We would also like to thank the developers and maintainers
of the \texttt{typing-extensions} package [@typeext],
which is used in \raimad to maintain compatibility with
Python 3.10.

This work is supported by the European Union
(ERC Consolidator Grant No. 101043486 TIFUUN).
Views and opinions expressed are however those of the
authors only and do not necessarily reflect those of the
European Union or the
European Research Council Executive Agency.
Neither the European Union nor the
granting authority can be held responsible for them.

# References

