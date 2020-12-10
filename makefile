## makefile automates the build and deployment for python projects

# build
PROJ_TYPE=		python
PROJ_MODULES=		git python-doc python-resources python-doc-deploy
WEB_PKG_DIR=		$(MTARG)/site
WEB_BROWSER=		firefox-repeat
PYTHON_BIN_ARGS ?=	export -o $(WEB_PKG_DIR)

# project
COLL_ARGS =		.*generalized\ distance\|Weighted\|.*Imperative\|Semantics
SITE_DEMO =		doc/demo
PY_DOC_BUILD_HTML_DEPS += cpdemo


include ./zenbuild/main.mk


## targets

.PHONY:			cpdemo
cpdemo:
			@echo "copy zotsite demo"
			mkdir -p $(PY_DOC_BUILD_HTML)
			cp -r $(SITE_DEMO) $(PY_DOC_BUILD_HTML)

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

.PHONY:			demo
demo:			clean
			rm -fr $(SITE_DEMO)
			make PYTHON_BIN_ARGS='export -o $(SITE_DEMO) --collection $(COLL_ARGS)' run
			touch $(SITE_DEMO)/.nojekyll
