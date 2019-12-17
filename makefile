## makefile automates the build and deployment for python projects

PROJ_TYPE=		python
PROJ_MODULES=		doc

WEB_PKG_DIR=		$(MTARG)/site
WEB_LIB=		lib/site
WEB_SRC=		src/site
WEB_BROWSER=		firefox-repeat
PYTHON_BIN_ARGS ?=	export -o $(WEB_PKG_DIR)

#MTARG_PYDIST_RES ?=	$(MTARG_PYDIST_BDIR)/zensols/zotsite/resources
#PY_RESOURCES +=		$(WEB_LIB) $(WEB_SRC)

# make build dependencies
_ :=	$(shell [ ! -d .git ] && git init ; [ ! -d zenbuild ] && \
	  git submodule add https://github.com/plandes/zenbuild && make gitinit )

include ./zenbuild/main.mk

.PHONY:		web
web:
		open $(WEB_SRC)/index.html
		osascript -e 'tell application "Emacs" to activate'

.PHONY:		export
export:
		mkdir -p $(MTARG)
		make PYTHON_BIN_ARGS='export -o $(WEB_PKG_DIR)' run

.PHONY:		print
print:
		make PYTHON_BIN_ARGS='print -w 2 --collection Detection$$' run

.PHONY:		selection
selection:
		mkdir -p $(MTARG)
		make PYTHON_BIN_ARGS='export -o $(WEB_PKG_DIR) --staticdirs $(WEB_LIB),$(WEB_SRC) --collection Detection$$' run

.PHONY:		display
display:	export
		if [ $(WEB_BROWSER) == 'firefox' ] ; then \
			open -a Firefox $(WEB_PKG_DIR)/index.html ; \
		elif [ '$(WEB_BROWSER)' == 'firefox-repeat' ] ; then \
			osascript src/as/refresh.scpt \
		else \
			osascript -e 'tell application "Safari" to set URL of document 1 to URL of document 1' ; \
		fi
