# CI/CD Integration with RAI Compliance Core

This directory contains examples and guidance for integrating RAI Compliance Core into CI/CD pipelines.

## Overview

The RAI Compliance Core provides a dedicated command for CI/CD integration: `ci-evaluate`. This command allows you to:

1. Load models and datasets from files
2. Run compliance evaluations
3. Generate reports in various formats
4. Set exit codes based on compliance results

## Basic Usage

```bash
rai-compliance ci-evaluate manifest.yaml \
  --model-path model.pkl \
  --dataset-path data.csv \
  --output-format json \
  --output-file compliance-report.json \
  --strict
```

## GitHub Actions Example

Here's an example GitHub Actions workflow that runs compliance checks:

```yaml
name: RAI Compliance Check

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  compliance:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install rai-compliance
        pip install -r requirements.txt
    
    - name: Run compliance check
      run: |
        rai-compliance ci-evaluate governance_manifest.yaml \
          --model-path models/trained_model.pkl \
          --dataset-path data/test_data.csv \
          --output-format json \
          --output-file compliance-report.json \
          --strict
    
    - name: Upload compliance report
      uses: actions/upload-artifact@v3
      with:
        name: compliance-report
        path: compliance-report.json
```

## GitLab CI Example

Here's an example GitLab CI configuration:

```yaml
stages:
  - test
  - compliance

compliance_check:
  stage: compliance
  image: python:3.10
  script:
    - pip install rai-compliance
    - pip install -r requirements.txt
    - rai-compliance ci-evaluate governance_manifest.yaml \
        --model-path models/trained_model.pkl \
        --dataset-path data/test_data.csv \
        --output-format json \
        --output-file compliance-report.json \
        --strict
  artifacts:
    paths:
      - compliance-report.json
    when: always
```

## Jenkins Pipeline Example

Here's an example Jenkins pipeline:

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.10'
        }
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install rai-compliance'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Compliance Check') {
            steps {
                sh '''
                rai-compliance ci-evaluate governance_manifest.yaml \
                  --model-path models/trained_model.pkl \
                  --dataset-path data/test_data.csv \
                  --output-format json \
                  --output-file compliance-report.json \
                  --strict
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'compliance-report.json', fingerprint: true
        }
    }
}
```

## Advanced Usage

### Using Model Adapters

If your model requires special handling, you can use a model adapter:

```bash
rai-compliance ci-evaluate manifest.yaml \
  --model-path model.h5 \
  --model-format tensorflow \
  --model-adapter my_package.adapters.TensorFlowAdapter \
  --dataset-path data.csv
```

### Providing Additional Context

You can provide additional context as a JSON file:

```bash
rai-compliance ci-evaluate manifest.yaml \
  --model-path model.pkl \
  --dataset-path data.csv \
  --context-file context.json
```

### Evaluating Specific Pipeline Stages

To evaluate a specific pipeline stage:

```bash
rai-compliance ci-evaluate manifest.yaml \
  --model-path model.pkl \
  --dataset-path data.csv \
  --stage "model_training"
```

## Exit Codes

- `0`: Compliance check passed or ran without the `--strict` flag
- `1`: Compliance check failed with the `--strict` flag
- Other non-zero codes: Error during execution

## Output Formats

- `text`: Human-readable summary (default)
- `json`: Machine-readable JSON format
- `html`: HTML report (requires `--output-file`)
