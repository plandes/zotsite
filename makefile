## makefile automates the build and deployment for python projects

PROJ_TYPE=		python
PROJ_MODULES=		doc

WEB_PKG_DIR=		$(MTARG)/site
WEB_BROWSER=		firefox-repeat
PYTHON_BIN_ARGS ?=	export -o $(WEB_PKG_DIR)

include ./zenbuild/main.mk

.PHONY:		web
web:
		open $(WEB_PKG_DIR)/index.html
		osascript -e 'tell application "Emacs" to activate'

.PHONY:		export
export:
		mkdir -p $(MTARG)
#		make PYTHON_BIN_ARGS='export -o $(WEB_PKG_DIR)' run
		make PYTHON_BIN_ARGS='export -o $(WEB_PKG_DIR) --collection Detection$$' run

.PHONY:		print
print:
#		make PYTHON_BIN_ARGS='print --collection GANN$$' run
		make PYTHON_BIN_ARGS='print --collection .*Toward' run
#		make PYTHON_BIN_ARGS='print --collection Detection$$' run

.PHONY:		selection
selection:
		mkdir -p $(MTARG)
#		make PYTHON_BIN_ARGS='export -o $(WEB_PKG_DIR) --collection .*Toward' run
		make PYTHON_BIN_ARGS='export -o $(WEB_PKG_DIR) --collection Detection$$' run

.PHONY:		display
display:	export
		if [ $(WEB_BROWSER) == 'firefox' ] ; then \
			open -a Firefox $(WEB_PKG_DIR)/index.html ; \
		elif [ '$(WEB_BROWSER)' == 'firefox-repeat' ] ; then \
			osascript src/as/refresh.scpt \
		else \
			osascript -e 'tell application "Safari" to set URL of document 1 to URL of document 1' ; \
		fi
