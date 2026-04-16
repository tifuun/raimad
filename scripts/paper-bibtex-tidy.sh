#!/bin/sh

bibtex-tidy \
	--curly \
	--numeric \
	--tab \
	--no-align \
	--sort=key \
	--duplicates=key \
	--no-escape \
	--sort-fields \
	--trailing-commas \
	--no-remove-dupe-fields \
	--enclosing-braces=title \
	--v2 \
	--no-modify \
	--output=paper/paper.tidy.bib \
	paper/paper.bib

