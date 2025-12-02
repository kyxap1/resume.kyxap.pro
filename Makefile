.PHONY: all clean devops devsecops

# Default target
all: devops

# Build for DevOps specialization
devops:
	@echo "Building DevOps resume..."
	@mkdir -p html
	jq -s -f filters/merge.jq --arg role "devops" specialties/_common.json specialties/devops.json companies/*.json skills/_common.json skills/devops.json > html/resume.json
	python3 scripts/render_resume.py html/resume.json -o html/index.html
	@echo "Done! Open html/index.html"

# Build for Site Reliability Engineer specialization
sre:
	@echo "Building SRE resume..."
	@mkdir -p html
	jq -s -f filters/merge.jq --arg role "sre" specialties/_common.json specialties/sre.json companies/*.json skills/_common.json skills/sre.json > html/resume.json
	python3 scripts/render_resume.py html/resume.json -o html/index.html
	@echo "Done! Open html/index.html"

# Build for DevSecOps specialization
devsecops:
	@echo "Building DevSecOps resume..."
	@mkdir -p html
	jq -s -f filters/merge.jq --arg role "devsecops" specialties/_common.json specialties/devsecops.json companies/*.json skills/_common.json skills/devops.json skills/devsecops.json > html/resume.json
	python3 scripts/render_resume.py html/resume.json -o html/index.html
	@echo "Done! Open html/index.html"

# Clean build artifacts
clean:
	rm -f html/*
