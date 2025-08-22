#@meta {desc: "zotsite build and test automation", date: "2025-08-22"}


## Build config
#
# type of project
PROJ_TYPE =		python
PROJ_MODULES =		python/doc python/package python/deploy
ADD_CLEAN +=		zotero-site
# add integration tests to test run
PY_TEST_ALL_TARGETS +=	testintegration


# Project
#
COLL_ARGS =		'^(?:NLP|Earth).*'
ENTRY= 			./zotsite
WEB_PKG_DIR=		$(MTARG)/site
SITE_DEMO =		doc/demo
PY_DOC_BUILD_HTML_DEPS += cpdemo


## Commands
#
define zotsite
	$(MAKE) $(PY_MAKE_ARGS) pyharn ARG="-c test-resources/zotsite.conf $(1)"
endef

define inttest
	@$(call zotsite,$(1)) | diff - $(2) || exit 1
	@printf "%s integration test ... ok\n" $(3)
endef

define inttestsort
	@$(call zotsite,$(1)) | sort | diff - $(2) || exit 1
	@printf "%s integration test ... ok\n" $(3)
endef


## Includes
#
include ./zenbuild/main.mk


## Targets
#
# export a subset of the collection
.PHONY:			exportsubset
exportsubset:
			@$(call zotsite,--collection $(COLL_ARGS))

# print a collections metadata
.PHONY:			print
print:
			@$(call zotsite,print --collection $(COLL_ARGS))


# test metadata output for entire library
.PHONY:			testprintall
testprintall:
			@$(call inttest,print --level warn $(PY_CLI_ARGS), \
			  test-resources/integration/export-all.txt,'print all')

# test metadata output for a collection
.PHONY:			testprintcol
testprintcol:
			@$(call inttest,print --level warn \
			  --collection $(COLL_ARGS) $(PY_CLI_ARGS), \
			  test-resources/integration/export-coll.txt,'print collection')

# test BetterBibtex citation key lookup
.PHONY:			testcitekey
testcitekey:
			@$(call inttestsort,citekey --level warn -k all, \
			   test-resources/integration/citekey.txt, \
			  'BetterBibtex citekey')

# test paper document (PDF) path lookup
.PHONY:			testdocpath
testdocpath:
			@$(call inttestsort,docpath --level warn -k all, \
			  test-resources/integration/docpath.txt, \
			  'document path lookup')

# all integration tests
.PHONY:			testintegration
testintegration:	testprintall testprintcol testcitekey testdocpath

# create the demo site
.PHONY:			demo
demo:			clean
			rm -fr $(SITE_DEMO)
			@$(call inttestsort,export -o $(SITE_DEMO) \
				--collection $(COLL_ARGS))
			touch $(SITE_DEMO)/.nojekyll

# copy the demo site to the GitHub pages install location
.PHONY:			cpdemo
cpdemo:
			@echo "copy zotsite demo"
			mkdir -p $(PY_DOC_BUILD_HTML)
			cp -r $(SITE_DEMO) $(PY_DOC_BUILD_HTML)
