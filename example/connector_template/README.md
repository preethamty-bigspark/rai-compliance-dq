# RAI Compliance Framework - Template Connector

This package provides a template connector for the RAI Compliance framework, demonstrating how to create a connector for an external library.

## What is a Connector?

Connectors are modules that integrate external libraries with the RAI Compliance framework. They provide a standardized interface for metrics and analysis tools from other packages, allowing them to be used in compliance evaluations.

## Getting Started

1. Clone this template:
   ```bash
   git clone https://github.com/yourusername/rai-compliance-template
   cd rai-compliance-template
   ```

2. Edit the files to connect to your external library:
   - Update `pyproject.toml` with your package information
   - Modify `rai_compliance_template/connector.py` to implement your connector

3. Install in development mode:
   ```bash
   pip install -e .
   ```

4. Test your connector:
   ```python
   from rai_compliance.connectors import list_connectors
   print(list_connectors())  # Should show your connector
   ```

## How It Works

1. Your connector class inherits from `BaseConnector`
2. It implements required methods like `initialize()` and `evaluate_metric()`
3. The package's entry points register the connector with the framework
4. When the framework needs a metric, it can use your connector

## Customizing Your Connector

1. Change the class name from `TemplateConnector` to something meaningful
2. Update the class attributes (id, name, description, etc.)
3. Implement the required methods to interact with your external library
4. Add specific methods for each metric type your connector supports

## Documentation

For more information, see the [RAI Compliance Framework documentation](https://github.com/ai-advisory/rai-compliance).