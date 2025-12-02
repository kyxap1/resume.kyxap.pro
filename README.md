# Resume Generator

This repository contains the source code and data for generating my resume in various formats and specializations (DevOps, SRE, DevSecOps).

## Setup

### Prerequisites
- Python 3
- `jq` (command-line JSON processor)
- `make`

### Python Environment

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Generate the resume for a specific specialization using `make`. The output will be generated at `html/index.html`.

- **DevOps**:
  ```bash
  make devops
  ```

- **SRE**:
  ```bash
  make sre
  ```

- **DevSecOps**:
  ```bash
  make devsecops
  ```

To clean up generated files:
```bash
make clean
```
