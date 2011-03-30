all:
	pdflatex structural_paraphrases.tex; bibtex structural_paraphrases; pdflatex structural_paraphrases.tex; pdflatex structural_paraphrases.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *~