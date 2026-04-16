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
\newcommand{\compo}{\texttt{compo}}
\newcommand{\proxy}{\texttt{proxy}}
\newcommand{\tifuun}{TIFUUN}

<!--
\Huge THIS IS A VERY EARLY DRAFT IM JUST WRITING WHAT POPS INTO MY HEAD \normalsize
-->

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
and KIDs (kinetic inductance detectors) [@mkids-day-actual].
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
\raimad designs can be exported as a CIF
(Caltech Intermediate Form)
file [@cif],
a format for storing mask files.
Using these files, a process engineer is
able to transfer the design onto the desired
substrate using general lithography techniques.


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

The development of \raimad was initiated in order to fulfill the needs of the
\tifuun (Terahertz Integral Field Units with Unified Nanotechnology) project
[@tifuun; @nishimura], to quickly design
integral field units (IFUs) that are tailored to each astronomical science
question as open-hardware [@openhardware].
Previously, a small number of integrated superconducting
spectrometer chips were designed for \tifuun's precursor project,
DESHIMA (Deep Spectroscopic High-redshift Mapper) [@deshima1; @deshima2],
using an internally developed script.
While that script proved to be a capable solution for the task at hand,
its narrow scope and reliance on the
end-of-life Python 2 made it unsuitable for use in \tifuun.
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

One of the main design decisions of \raimad
is its balanced approach to mutability.
\raimad's Components,
once instantiated, are immutable.
Transformations, such as translation, rotations,
duplication, and layer reassignment,
are handled using Proxies,
which offer a mutable view of a Component.
Thus, the memory requirements of producing multiple
instances of a particular structure --
such as dozens of bridges on a coplanar waveguide --
are lowered,
since the underlying structure of the bridge is only stored
once in the Component object,
while the translations and rotations of each instance are stored
in a lightweight Proxy object.

<!-- we already said that modular approach is
    easier to understand for developers
    than a bunch of loose functions/methods.
    Now specifically I want to talk about why the compos are immutable.
    -->

This approach also allows for potential optimisations
in the CIF file produced by \raimad,
such as re-using parts of the geometry using the
Symbols
feature of the CIF format.
Such optimizations are critical for the future of the \tifuun project,
which will feature designs of a much higher complexity than DESHIMA.

A major design goal of \raimad was to make it feel idiomatic
to Python developers.
As such, we have adopted the concept of Python's Gradual Typing
into a feature called Annotations.
Annotations are a way to document the layers, options, and marked coordinate
points of \raimad Components
in a structured way.
Annotations are parsed by \raidex to generate structured documentation
and may, in the future,
be used for static checking of Components,
much like Python's MyPy.

<!-- -----NEW------ REQUIRED SECTION!! -->
# Research Impact Statement


\raimad is being used in the development
of preliminary chip designs
for \tifuun,
including a novel type of KIDs [@leonposter]
and a testbed for measuring transmission line losses [@pienthesis]
pictured in \autoref{fig:recursive}.
These works have not only established \raimad
as a versatile mask file creation tool,
but have also enriched the \raidex
component library with new devices.
Moreover,
recent developments in
fabrication techniques [@leonfab]
and high-efficiency filterbank designs [@louisbank]
signal advances for the \tifuun project as a whole,
wherein \raimad will figure as the central
mask file design tool.

<!-- Arend told me to call raimad a "bridge"
    between design and fabrication
    but I disagree here.
    A bridge is two-way.
    If we had some sort of design rule checker,
    something that might tell you
    "this wire is too thin for optical lithography,
    try e-beam instead",
    then it would be a bridge.
    Right now it's just a one-way funnel.
    -->

![
An example of a chip designed in \raimad{} [@pienthesis]
and rendered in KLayout.
Left: the entire chip on a 10cm wafer;
centre: an arrangement of four antennas, each one approximately 1mm across;
right: 2µm wide microstrips connected to each half of an antenna.
\label{fig:recursive}
](img/recursive-final.png)

<!--

![
A part of the chip designed and fabbed by @leonfab,
designed in \raimad,
rendered in KLayout.
](img/louis-ppc-chip.png)

![
The chip proposed by @pienthesis,
designed in \raimad,
rendered in KLayout.
](img/pien/chip.png)

![
Part of the T7011 chip designed in \raimad,
rendered in KLayout [@klay]
](img/t7011-closeup.png)

-->


<!-- -----NEW------ REQUIRED SECTION!! -->
# AI usage disclosure
<!-- TODO style -->
\raimad makes limited use of AI-generated code.
Some coordinate transformation functions
and test fixtures have been written using
publically available
gratis large language models,
such as ChatGPT [@chatgpt] and Perplexity [@perplexity].
Due to the software-as-a-service nature of these AI models,
the exact versions cannot be ascertained.
<!-- AI usage section description says versions of models
    need to be provided but we really can't say what versions
    because I just used the webui without logging in
    -->
All AI-generated code is marked as such using comments,
and has been proofread and edited by the author
to ensure correct functionality and consistency
with \raimad code style.

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
(ERC Consolidator Grant No. 101043486 \tifuun).
Views and opinions expressed are however those of the
authors only and do not necessarily reflect those of the
European Union or the
European Research Council Executive Agency.
Neither the European Union nor the
granting authority can be held responsible for them.

# References

