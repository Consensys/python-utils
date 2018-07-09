# A sample Makefile for facilitating docs building on ConsenSys-Utils.

# Docs directory

# Sphinx info
SPHINXOPTS=
SPHINXPROJ=ConsenSys-Utils
ROOTDIR=..
SOURCEDIR=.
BUILDDIR=_build

# Sphinx build executable
SPHINX_EXEC_PATH=$(ROOTDIR)/$(EXEC_PATH)
SPHINXBUILD=$(SPHINX_EXEC_PATH)sphinx-build

.PHONY: venv develop init clean-pyc clean-build clean-html clean build-html html

clean:
	@rm -rf $(BUILDDIR)

build-html:
	@echo "Building docs..."
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)
	@echo "Build finished. The HTML pages are in $(BUILDDIR)."

html: clean build-html
	@xdg-open $(BUILDDIR)/index.html