## (@)Id: makefile automates the build and deployment for python projects

## Build config
#
# type of project
PROJ_TYPE =		python
PROJ_MODULES =		git python-resources python-cli python-doc python-doc-deploy
INFO_TARGETS +=		appinfo
ADD_CLEAN +=		zotero-site

# Project
#
COLL_ARGS =		.*generalized\ distance\|Weighted\|.*Imperative\|Semantics
ENTRY= 			./zotsite
WEB_PKG_DIR=		$(MTARG)/site
SITE_DEMO =		doc/demo
PY_DOC_BUILD_HTML_DEPS += cpdemo

# add app configuration to command line arguments
PY_CLI_ARGS +=		-c test-resources/zotsite.conf


include ./zenbuild/main.mk


.PHONY:			appinfo
appinfo:
			@echo "app-resources-dir: $(RESOURCES_DIR)"

.PHONY:			zsrun
zsrun:
			$(ENTRY) $(PYTHON_BIN_ARGS)

.PHONY:			export
export:
			$(ENTRY) $(PY_CLI_ARGS)

.PHONY:			exportsubset
exportsubset:
			$(ENTRY) --collection $(COLL_ARGS) $(PY_CLI_ARGS)

.PHONY:			print
print:
			$(ENTRY) print --collection $(COLL_ARGS) $(PY_CLI_ARGS)

.PHONY:			testprint
testprint:
			$(eval EXPECTED=10)
			$(eval LINES=$(shell make print | wc -l))
			@if [ $(LINES) -lt $(EXPECTED) ] ; then \
				echo "expecting at least $(EXPECTED) lines but got $(LINES)" ; \
				exit 1 ; \
			fi

.PHONY:			testall
testall:		test testprint

.PHONY:			cpdemo
cpdemo:
			@echo "copy zotsite demo"
			mkdir -p $(PY_DOC_BUILD_HTML)
			cp -r $(SITE_DEMO) $(PY_DOC_BUILD_HTML)

.PHONY:			demo
demo:			clean
			rm -fr $(SITE_DEMO)
			make PYTHON_BIN_ARGS='export -o $(SITE_DEMO) --collection $(COLL_ARGS)' zsrun
			touch $(SITE_DEMO)/.nojekyll
