# Responsible AI Framework

A comprehensive toolkit for implementing responsible AI governance or regulatory compliance.

## Features

- **Regulatory Mapping**: Transform legal requirements into implementable rules
- **Rule Engine**: Define, manage and enforce responsible AI rules
- **Test Framework**: Metrics-based evaluation for AI systems
- **ML Lifecycle Integration**: Hooks for CI/CD pipelines and model evaluation
- **Plugin Architecture**: Extensible system for custom metrics and integrations

## Installation

You can install the package locally using:

```bash
pip install -e .
```

Once published to PyPI, you can install it using:

```bash
pip install rai-compliance
```

For additional features, install optional dependencies:

```bash
# For HTML report generation
pip install rai-compliance[html]

# For PyTorch support
pip install rai-compliance[torch]

# For TensorFlow support
pip install rai-compliance[tensorflow]


# For NLP support
pip install rai-compliance[nlp]

# For all optional dependencies
pip install rai-compliance[all]
```

## Usage

### CLI Commands

#### Validate a Manifest

```bash
rai-compliance validate your_governance_manifest.yaml
```

#### List Available Metrics

```bash
rai-compliance metrics
```

#### List Registered Data Types

```bash
rai-compliance data-types
```

#### List Installed Plugins

```bash
rai-compliance plugins
```

#### List Available Connectors

```bash
rai-compliance connectors
```

#### Visualize Pipeline Stages

```bash
rai-compliance pipeline your_governance_manifest.yaml
```

Generate a Mermaid diagram of pipeline stages and dependencies:

```bash
rai-compliance pipeline your_governance_manifest.yaml --mermaid
```

#### List and Filter Rules

```bash
rai-compliance rules your_governance_manifest.yaml
```

Filter rules by severity:

```bash
rai-compliance rules your_governance_manifest.yaml --severity critical
```

### Loading a governance manifest

```python
from rai_compliance import GovernanceFramework

# Load from a YAML file containing laws, rules, and metrics
framework = GovernanceFramework.from_yaml("your_governance_manifest.yaml")

# Apply the framework to a model or API
compliance_report = framework.evaluate_compliance(model=my_model)
print(compliance_report.summary())
```

### Plugin Architecture

The RAI Compliance framework uses a plugin architecture to support extensible metrics and external library integration. This allows you to:

1. Use metrics from external packages
2. Create your own custom metrics
3. Share metrics with the community
4. Support different data types through specialized metrics
5. Integrate with popular fairness, explainability, and governance libraries

#### Modular Connector Architecture

In addition to metrics plugins, the framework supports connectors to external libraries. Connectors are separate packages that:

1. Integrate with specialized libraries (AIF360, InterpretML, etc.)
2. Provide a standardized interface for their metrics
3. Handle dependency management and initialization
4. Transform data between formats

To create your own connector, use the template in `examples/connector_template` directory.

#### Using Connectors

To use external library connectors, install them alongside the core framework:

```bash
pip install rai-compliance
pip install rai-compliance-aif360  # Example connector for IBM AI Fairness 360
```

Connectors are automatically discovered when installed. You can see available connectors using the CLI:

```bash
rai-compliance connectors
```

The framework will automatically find connectors that support specific metrics. For example, if your manifest uses "demographic_parity" and you have the AIF360 connector installed, the framework will find and use it.

#### Using External Metric Packages

To use metrics from external packages, simply install them alongside the core framework:

```bash
pip install rai-compliance
pip install rai-compliance-fairness  # Example external metric package
```

The framework will automatically discover and load metrics from installed packages.

#### Creating Custom Metrics

You can create custom metrics in two ways:

##### 1. Inline Metrics

For simple use cases, you can define metrics directly in your code:

```python
from rai_compliance.metrics import register_metric

@register_metric("my_custom_metric")
def my_custom_metric(model, dataset, config):
    """
    My custom metric description.
    """
    # Implementation
    return {
        "value": 0.95,  # Score between 0 and 1
        "details": {"additional": "information"}
    }

# Use the metric in a manifest
framework = GovernanceFramework.from_yaml("manifest.yaml")
```

##### 2. Creating a Metric Package

For more complex metrics or to share with others, create a separate package:

1. Create a new Python package (e.g., `rai-compliance-mymetrics`)
2. Implement your metrics using the `@register_metric` decorator
3. Configure entry points in your package's `pyproject.toml`:

```toml
[project.entry-points."rai_compliance.metrics"]
my_custom_metric = "rai_compliance_mymetrics.module:my_custom_metric"
```

#### Data Type Support

The framework supports different data types through the `@supports_data_types` decorator. This allows metrics to specify which data types they can handle, and the framework will automatically validate that the data matches the expected type.

The core framework includes support for common data types:

- `tabular`: Pandas DataFrames and similar tabular data structures
- `text`: Strings and lists of strings
- `image`: PIL Images and numpy arrays with image shapes
- `audio`: Audio data (placeholder for future implementation)
- `video`: Video data (placeholder for future implementation)

Plugins can extend the framework to support additional data types without modifying the core package. For example, the Polars plugin (see Examples section) adds support for Polars DataFrames by registering a new data type and providing metrics that work with it.

```python
from rai_compliance.metrics import register_metric, supports_data_types

@register_metric("demographic_parity")
@supports_data_types("tabular")
def demographic_parity_check(model, dataset, config):
    """
    Measure statistical parity across demographic groups.
    """
    # Implementation for tabular data
    return {"value": score, "details": {...}}

@register_metric("pii_detection")
@supports_data_types("text")
def pii_detection_check(model, dataset, config):
    """
    Check for personally identifiable information in text.
    """
    # Implementation for text data
    return {"value": score, "details": {...}}
```

You can also specify multiple data types:

```python
@register_metric("content_safety")
@supports_data_types("text", "image")
def content_safety_check(model, dataset, config):
    """
    Check for unsafe content in text or images.
    """
    # Implementation that handles both text and image data
    return {"value": score, "details": {...}}
```

In your YAML manifest, you can specify the data type for each pipeline stage:

```yaml
pipeline_stages:
  - name: "data_ingestion"
    description: "Data collection and preprocessing"
    data_type: "tabular"  # This stage processes tabular data
    rules: 
      - "data_quality"
      
  - name: "text_processing"
    description: "Text data preprocessing"
    data_type: "text"  # This stage processes text data
    rules: 
      - "privacy_compliance"
```

You can also specify multiple data types for a stage:

```yaml
pipeline_stages:
  - name: "multimodal_analysis"
    description: "Combined analysis of text and images"
    data_type: ["text", "image"]  # This stage processes both text and images
    rules:
      - "content_safety"
```

### Enhanced Manifest Schema

The framework supports an enhanced manifest schema with additional features:

#### Multiple Data Types in Metadata

You can specify multiple data types that your AI system handles:

```yaml
metadata:
  data_type: ["tabular", "text"]  # System handles both tabular and text data
```

#### Pipeline Stage Dependencies

You can define dependencies between pipeline stages to model your ML workflow:

```yaml
pipeline_stages:
  - id: "data_collection"
    name: "Data Collection"
    description: "Collect raw data"
    dependencies: []  # No dependencies
    
  - id: "data_preprocessing"
    name: "Data Preprocessing"
    description: "Clean and transform data"
    dependencies: ["data_collection"]  # Depends on data collection
    
  - id: "model_training"
    name: "Model Training"
    description: "Train the model"
    dependencies: ["data_preprocessing"]  # Depends on preprocessing
```

Use the pipeline visualization command to see the dependencies:

```bash
rai-compliance pipeline manifest.yaml --mermaid
```

#### Rule Severity Levels

You can assign severity levels to rules to prioritize compliance issues:

```yaml
rules:
  - id: "data_quality"
    name: "Data Quality"
    description: "Ensure data quality standards"
    severity: "high"  # Can be low, medium, high, or critical
    tests: [...]
```

Filter rules by severity using the CLI:

```bash
rai-compliance rules manifest.yaml --severity critical
```

#### Test Enhancements

Tests can include additional metadata and constraints:

```yaml
tests:
  - id: "demographic_parity"
    name: "Demographic Parity"
    description: "Check for statistical parity"
    criteria:
      operator: "<"
      value: 0.2
    version: "1.0.0"  # Version of the test
    source: "fairness_metrics"  # Source package
    dependencies: ["data_quality.completeness"]  # Test dependencies
    applicable_models: ["classification"]  # Model types this applies to
    applicable_data: ["tabular"]  # Data types this applies to
    timeout: 60  # Maximum execution time in seconds
```

The framework will automatically validate that the data matches the expected type and will only run metrics that support that data type.

#### Metric Implementation Guidelines

When implementing metrics, follow these guidelines:

1. Use the `@register_metric` decorator with a unique ID
2. Use the `@supports_data_types` decorator to specify which data types the metric supports
3. Accept `model`, `dataset`, and `config` parameters
4. Return a dictionary with at least a `value` key (must be between 0 and 1)
5. Include a detailed docstring explaining what the metric measures
6. Add helpful details in the result for reporting

Example metric implementation:

```python
@register_metric("data_quality.completeness")
def completeness_check(model, dataset, config):
    """
    Measures the completeness of a dataset by calculating the ratio of non-missing values.
    
    Args:
        model: Not used for this metric
        dataset: Pandas DataFrame to evaluate
        config: Optional configuration with 'columns' to check
        
    Returns:
        Dictionary with evaluation results
    """
    # Implementation details...
    
    return {
        "value": completeness_score,  # Between 0 and 1
        "details": {
            "total_cells": total_cells,
            "missing_cells": missing_cells,
            "columns": column_details
        }
    }
```

#### Metric Value Ranges

All metrics in the RAI Compliance framework must return values in the range [0, 1], where:

- 0 typically represents the worst case (maximum issues)
- 1 typically represents the best case (no issues)

For metrics that naturally produce values outside this range, use the provided normalization utilities:

```python
from rai_compliance.utils.data_helpers import normalize_value, sigmoid_normalize

# For metrics with known bounds (e.g., accuracy from 0-100%)
raw_accuracy = calculate_accuracy(model, dataset)  # e.g., 87.5
normalized_accuracy = normalize_value(raw_accuracy, min_val=0, max_val=100)

# For unbounded metrics (e.g., MSE that could be very large)
error = calculate_mse(model, dataset)  # e.g., 245.7
normalized_error = sigmoid_normalize(error, scale=50.0)
```

Always include the raw value in the details for transparency:

```python
return {
    "value": normalized_value,  # Must be in [0, 1]
    "details": {
        "raw_value": raw_value,  # Original value before normalization
        # Other details...
    }
}
```

##### Example Implementations for Different Metric Types

###### Percentage Metrics

```python
@register_metric("accuracy_percentage")
def accuracy_percentage(model, dataset, config):
    """Calculate accuracy as a percentage and normalize to [0, 1]."""
    # Calculate raw accuracy (0-100%)
    raw_accuracy = calculate_raw_accuracy(model, dataset)  # e.g., 87.5%
    
    # Normalize to [0, 1]
    normalized = raw_accuracy / 100
    
    return {
        "value": normalized,
        "details": {"raw_accuracy": raw_accuracy}
    }
```

###### Error Metrics

```python
@register_metric("mean_squared_error")
def mean_squared_error(model, dataset, config):
    """Calculate MSE and normalize using sigmoid."""
    # Calculate raw MSE (unbounded)
    raw_mse = calculate_raw_mse(model, dataset)  # e.g., 245.7
    
    # Normalize using sigmoid (scale based on expected range)
    normalized = sigmoid_normalize(raw_mse, scale=50.0)
    
    return {
        "value": normalized,
        "details": {"raw_mse": raw_mse}
    }
```

###### Domain-Specific Metrics

```python
@register_metric("latency")
def latency_metric(model, dataset, config):
    """Calculate model latency and normalize based on thresholds."""
    # Calculate raw latency in milliseconds
    raw_latency = measure_latency(model, dataset)  # e.g., 120ms
    
    # Normalize using domain-specific thresholds
    # 50ms is considered good (0.0), 200ms is considered bad (1.0)
    normalized = normalize_value(
        raw_latency, 
        min_val=50,   # Good threshold
        max_val=200,  # Bad threshold
        invert=False  # Higher latency is worse, so no inversion needed
    )
    
    return {
        "value": normalized,
        "details": {"raw_latency_ms": raw_latency}
    }
```

## Documentation

TBA

## Examples

### Polars Plugin Example

The repository includes an example plugin for [Polars](https://pola.rs/) DataFrames in the `examples/polars_plugin` directory. This example demonstrates how to:

1. Create a plugin that supports a specific data type
2. Register metrics with the framework
3. Use the plugin in a YAML manifest
4. Evaluate compliance with Polars DataFrames

To run the example:

```bash
cd examples/polars_plugin
pip install -e .
python example.py
```

### Connector Template

The repository includes a template for creating custom connectors in the `examples/connector_template` directory. This template demonstrates how to:

1. Create a connector for an external library
2. Define supported metrics
3. Implement the connector interface
4. Register the connector via entry points

To use the template:

```bash
cp -r examples/connector_template my-connector
cd my-connector
# Edit files to implement your connector
pip install -e .
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/ai-advisory/rai-compliance.git
cd rai_compliance

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Resource Files

The RAI Compliance framework includes several resource files:

- `manifest_schema.yaml`: Schema for validating governance manifests


When creating plugins or extensions, you can access these resources using:

```python
from rai_compliance.resources import get_schema_path, read_schema

# Get path to a schema file
schema_path = get_schema_path("manifest_schema.yaml")

# Read schema contents directly
schema_content = read_schema("manifest_schema.yaml")
```

This approach ensures that resources are properly located regardless of how the package is installed.

### Running Tests

```bash
pytest
```

### CI/CD Pipeline

This project uses GitHub Actions for continuous integration and delivery. The following workflows are available:

#### Test Workflow

The test workflow runs on every push and pull request to ensure code quality and functionality:

```bash
# Run tests locally (same as CI)
pytest tests/ --cov=rai_compliance
```

#### Lint Workflow

The lint workflow checks code style and quality:

```bash
# Install linting tools
pip install flake8 black isort

# Run linters locally (same as CI)
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
black --check --diff .
isort --check --diff .
```

#### Security Workflow

The security workflow scans for vulnerabilities using CodeQL and Bandit:

```bash
# Run Bandit locally
pip install bandit
bandit -r rai_compliance
```

#### Publish Workflow

The publish workflow automatically builds and publishes the package to PyPI when a new release is created or a tag is pushed:

1. Create a new tag: `git tag -a v0.1.0 -m "Release v0.1.0"`
2. Push the tag: `git push origin v0.1.0`
3. The workflow will automatically build and publish the package

#### Dependabot

Dependabot is configured to check for dependency updates weekly and create pull requests for any updates found.

## License

Need to decide
