## (@)Id: makefile automates the build and deployment for python projects


## Build config
#
# type of project
PROJ_TYPE =		python
PROJ_MODULES =		git python-resources python-cli python-doc python-doc-deploy
INFO_TARGETS +=		appinfo
ADD_CLEAN +=		zotero-site
# add app configuration to command line arguments
PY_CLI_ARGS +=		-c test-resources/zotsite.conf
# add integration tests to test run
PY_TEST_DEPS +=		testintegration


# Project
#
COLL_ARGS =		"^(?:NLP|Earth).*"
ENTRY= 			./zotsite
WEB_PKG_DIR=		$(MTARG)/site
SITE_DEMO =		doc/demo
PY_DOC_BUILD_HTML_DEPS += cpdemo



## Includes
#
include ./zenbuild/main.mk


## Targets
#
.PHONY:			appinfo
appinfo:
			@echo "app-resources-dir: $(RESOURCES_DIR)"

# export all
.PHONY:			export
export:
			$(ENTRY) $(PY_CLI_ARGS)

# export a subset of the collection
.PHONY:			exportsubset
exportsubset:
			$(ENTRY) --collection $(COLL_ARGS) $(PY_CLI_ARGS)

# print a collections metadata
.PHONY:			print
print:
			$(ENTRY) print --collection $(COLL_ARGS) $(PY_CLI_ARGS)

# test metadata output for entire library
.PHONY:			testprintall
testprintall:
			@$(ENTRY) print --level warn $(PY_CLI_ARGS) | \
				diff - test-resources/integration/export-all.txt || \
				exit 1
			@echo "print all integration test ... ok"

# test metadata output for a collection
.PHONY:			testprintcol
testprintcol:
			@$(ENTRY) print --level warn \
				--collection $(COLL_ARGS) $(PY_CLI_ARGS) | \
				diff - test-resources/integration/export-coll.txt || \
				exit 1
			@echo "Print collection integration test ... ok"

# all integration tests
.PHONY:			testintegration
testintegration:	testprintall testprintcol

# create the demo site
.PHONY:			demo
demo:			clean
			rm -fr $(SITE_DEMO)
			$(ENTRY) $(PY_CLI_ARGS) \
				export -o $(SITE_DEMO) \
				--collection $(COLL_ARGS)
			touch $(SITE_DEMO)/.nojekyll

# copy the demo site to the GitHub pages install location
.PHONY:			cpdemo
cpdemo:
			@echo "copy zotsite demo"
			mkdir -p $(PY_DOC_BUILD_HTML)
			cp -r $(SITE_DEMO) $(PY_DOC_BUILD_HTML)
