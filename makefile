## makefile automates the build and deployment for python projects

PROJ_TYPE=	python

WEB_PKG_DIR=	$(MTARG)/site
WEB_SRC=	src/site
PYTHON_BIN_ARGS ?= export -o $(WEB_PKG_DIR)

# make build dependencies
_ :=	$(shell [ ! -d .git ] && git init ; [ ! -d zenbuild ] && \
	  git submodule add https://github.com/plandes/zenbuild && make gitinit )

include ./zenbuild/main.mk

.PHONY:		web
web:
		open $(WEB_SRC)/index.html
		osascript -e 'tell application "Emacs" to activate'

.PHONY:		web-package
web-package:
		mkdir -p $(WEB_PKG_DIR)
		rsync -rltpgoDuv -d $(WEB_SRC)/* $(WEB_PKG_DIR)
		make run
