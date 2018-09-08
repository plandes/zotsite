## makefile automates the build and deployment for python projects

PROJ_TYPE=		python
PROJ_MODULES=		doc

WEB_PKG_DIR=		$(MTARG)/site
WEB_LIB=		lib/site
WEB_SRC=		src/site
WEB_BROWSER=		firefox
PYTHON_BIN_ARGS ?=	export -o $(WEB_PKG_DIR)

MTARG_PYDIST_RES ?=	$(MTARG_PYDIST_BDIR)/zensols/zotsite/resources
PY_RESOURCES +=		$(WEB_LIB) $(WEB_SRC)

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
		mkdir -p $(MTARG)
		make PYTHON_BIN_ARGS='export -o $(WEB_PKG_DIR) --staticdirs $(WEB_LIB),$(WEB_SRC)' run

.PHONY:		display
display:	web-package
		if [ $(WEB_BROWSER) == 'firefox' ] ; then \
			open -a Firefox $(WEB_PKG_DIR)/index.html ; \
		else \
			osascript -e 'tell application "Safari" to set URL of document 1 to URL of document 1' ; \
		fi
