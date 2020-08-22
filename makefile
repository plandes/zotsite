## makefile automates the build and deployment for python projects

# build
PROJ_TYPE=		python
PROJ_MODULES=		git python-doc python-resources
WEB_PKG_DIR=		$(MTARG)/site
WEB_BROWSER=		firefox-repeat
PYTHON_BIN_ARGS ?=	export -o $(WEB_PKG_DIR)

# project
COLL_ARGS =		.*generalized\ distance\|Weighted\|.*Imperative\|Semantics
SITE_SAMPLE =		doc/sample
PY_DOC_BUILD_HTML_DEPS += cpdemo


include ./zenbuild/main.mk


## targets

.PHONY:			cpdemo
cpdemo:
			@echo "COPY DEMO"
			mkdir -p $(PY_DOC_BUILD_HTML)
			cp -r doc/demo $(PY_DOC_BUILD_HTML)

.PHONY:			web
web:
			open $(WEB_PKG_DIR)/index.html
			osascript -e 'tell application "Emacs" to activate'

.PHONY:			print
print:
			make PYTHON_BIN_ARGS='print --collection $(COLL_ARGS)' run

.PHONY:			export
export:
			mkdir -p $(MTARG)
			make PYTHON_BIN_ARGS='export -o $(WEB_PKG_DIR)' run

.PHONY:			selection
selection:
			mkdir -p $(MTARG)
			make PYTHON_BIN_ARGS='export -o $(WEB_PKG_DIR) --collection $(COLL_ARGS)' run

.PHONY:			display
display:		export
			if [ $(WEB_BROWSER) == 'firefox' ] ; then \
				open -a Firefox $(WEB_PKG_DIR)/index.html ; \
			elif [ '$(WEB_BROWSER)' == 'firefox-repeat' ] ; then \
				osascript src/as/refresh.scpt \
			else \
				osascript -e 'tell application "Safari" to set URL of document 1 to URL of document 1' ; \
			fi

.PHONY:			sample
sample:			clean
			rm -fr $(SITE_SAMPLE)
			make PYTHON_BIN_ARGS='export -o $(SITE_SAMPLE) --collection $(COLL_ARGS)' run
