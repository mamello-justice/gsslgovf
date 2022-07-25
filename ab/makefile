file=annotated-bibliography

all:
	pdflatex $(file).tex
	bibtex $(file)
	pdflatex $(file).tex
	pdflatex $(file).tex

bib:
	@python3 ./scripts/bib2tex.py references.bib

clean:
	rm -rf $(file).{aux,bbl,blg,lof,log,lot,out,synctex.gz,toc}
