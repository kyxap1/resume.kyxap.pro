.PHONY: all clean devops devsecops

# Python interpreter
PYTHON := $(shell if [ -f .venv/bin/python3 ]; then echo .venv/bin/python3; else echo python3; fi)

# Common JSON files
BASE_JSON = specialties/_common.json
OTHERS_JSON = companies/*.json skills/_common.json

# Build macro
# $(1): role name
# $(2): specialty JSON file
# $(3): additional skills JSON files
define build_resume
	@echo "Building $(1) resume..."
	@mkdir -p html
	jq -s -f filters/merge.jq --arg role "$(1)" $(BASE_JSON) $(2) $(OTHERS_JSON) $(3) > html/resume.json
	$(PYTHON) scripts/render_resume.py html/resume.json -o html/index.html --pdf html/resume.pdf
	@echo "Done! Open html/index.html and html/resume.pdf"
endef

# Default target
all: devsecops

# Build for DevOps specialization
devops:
	$(call build_resume,devops,specialties/devops.json,skills/devops.json)

# Build for Site Reliability Engineer specialization
sre:
	$(call build_resume,sre,specialties/sre.json,skills/sre.json)

# Build for DevSecOps specialization
devsecops:
	$(call build_resume,devsecops,specialties/devsecops.json,skills/devops.json skills/devsecops.json)

# Clean build artifacts
clean:
	rm -f html/*
