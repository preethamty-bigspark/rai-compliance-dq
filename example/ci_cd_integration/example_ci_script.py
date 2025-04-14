#!/usr/bin/env python
"""
Example script demonstrating how to run RAI compliance checks in a CI/CD pipeline.

This script can be used as a template for integrating RAI Compliance Core
into your CI/CD workflows or automated testing scripts.
"""

import argparse
import json
import os
import sys
from datetime import datetime

# Try to import RAI Compliance Core
try:
    from rai_compliance import GovernanceFramework
    from rai_compliance.utils.data_helpers import get_data_type
except ImportError:
    print("Error: RAI Compliance Core is not installed.")
    print("Install it with: pip install rai-compliance")
    sys.exit(1)


def load_model(model_path, model_format):
    """Load a model from a file."""
    print(f"Loading model from {model_path} (format: {model_format})")

    if model_format == "pickle":
        import pickle

        with open(model_path, "rb") as f:
            return pickle.load(f)
    elif model_format == "joblib":
        import joblib

        return joblib.load(model_path)
    elif model_format == "tensorflow":
        import tensorflow as tf

        return tf.keras.models.load_model(model_path)
    elif model_format == "pytorch":
        import torch

        return torch.load(model_path)
    elif model_format == "sklearn":
        import pickle

        with open(model_path, "rb") as f:
            return pickle.load(f)
    else:
        raise ValueError(f"Unsupported model format: {model_format}")


def load_dataset(dataset_path, dataset_format):
    """Load a dataset from a file."""
    print(f"Loading dataset from {dataset_path} (format: {dataset_format})")

    if dataset_format == "csv":
        import pandas as pd

        return pd.read_csv(dataset_path)
    elif dataset_format == "json":
        import pandas as pd

        return pd.read_json(dataset_path)
    elif dataset_format == "parquet":
        import pandas as pd

        return pd.read_parquet(dataset_path)
    elif dataset_format == "pickle":
        import pickle

        with open(dataset_path, "rb") as f:
            return pickle.load(f)
    else:
        raise ValueError(f"Unsupported dataset format: {dataset_format}")


def apply_adapter(model, adapter_path):
    """Apply a model adapter."""
    if not adapter_path:
        return model

    print(f"Applying adapter: {adapter_path}")

    try:
        module_path, class_name = adapter_path.rsplit(".", 1)
        module = __import__(module_path, fromlist=[class_name])
        adapter_class = getattr(module, class_name)
        return adapter_class(model)
    except (ImportError, AttributeError) as e:
        print(f"Error applying adapter: {e}")
        sys.exit(1)


def save_report(report, output_format, output_file):
    """Save the compliance report."""
    if output_format == "json":
        output = report.to_dict()
        if output_file:
            with open(output_file, "w") as f:
                json.dump(output, f, indent=2)
            print(f"JSON report saved to {output_file}")
        else:
            print(json.dumps(output, indent=2))
    elif output_format == "html":
        if not output_file:
            print("Error: HTML output requires an output file")
            sys.exit(1)
        report.to_html(output_file)
        print(f"HTML report saved to {output_file}")
    else:
        # Text output
        summary = report.summary()
        print("\n=== Compliance Report Summary ===")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(
            f"Overall compliance: {'PASSED' if summary.get('passed', False) else 'FAILED'}"
        )
        print(
            f"Rules passed: {summary.get('rules_passed', 0)}/{summary.get('rules_total', 0)}"
        )
        print(
            f"Tests passed: {summary.get('tests_passed', 0)}/{summary.get('tests_total', 0)}"
        )

        if output_file:
            with open(output_file, "w") as f:
                f.write("=== Compliance Report Summary ===\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(
                    f"Overall compliance: {'PASSED' if summary.get('passed', False) else 'FAILED'}\n"
                )
                f.write(
                    f"Rules passed: {summary.get('rules_passed', 0)}/{summary.get('rules_total', 0)}\n"
                )
                f.write(
                    f"Tests passed: {summary.get('tests_passed', 0)}/{summary.get('tests_total', 0)}\n"
                )
            print(f"Text report saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Run RAI compliance checks in a CI/CD pipeline"
    )

    parser.add_argument("manifest_file", help="Path to the manifest file")
    parser.add_argument("--model-path", help="Path to the model file")
    parser.add_argument(
        "--model-format",
        choices=["pickle", "joblib", "tensorflow", "pytorch", "sklearn"],
        default="pickle",
        help="Format of the model file",
    )
    parser.add_argument(
        "--model-adapter", help="Adapter class for the model (module.ClassName)"
    )
    parser.add_argument("--dataset-path", help="Path to the dataset file")
    parser.add_argument(
        "--dataset-format",
        choices=["csv", "json", "parquet", "pickle"],
        default="csv",
        help="Format of the dataset file",
    )
    parser.add_argument(
        "--context-file", help="Path to a JSON file with additional context"
    )
    parser.add_argument("--stage", help="Pipeline stage to evaluate")
    parser.add_argument(
        "--output-format",
        choices=["text", "json", "html"],
        default="text",
        help="Output format",
    )
    parser.add_argument("--output-file", help="Path to save the output")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with non-zero code if compliance fails",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Show detailed error information"
    )

    args = parser.parse_args()

    try:
        # Load framework from manifest
        framework = GovernanceFramework.from_yaml(args.manifest_file)
        print(f"Loaded framework from {args.manifest_file}")

        # Load model if specified
        model = None
        if args.model_path:
            model = load_model(args.model_path, args.model_format)

            # Apply adapter if specified
            if args.model_adapter:
                model = apply_adapter(model, args.model_adapter)

        # Load dataset if specified
        dataset = None
        if args.dataset_path:
            dataset = load_dataset(args.dataset_path, args.dataset_format)
            print(f"Dataset type: {get_data_type(dataset)}")

        # Load context if specified
        context = {}
        if args.context_file:
            with open(args.context_file, "r") as f:
                context = json.load(f)
            print(f"Loaded context from {args.context_file}")

        # Run evaluation
        print("Running compliance evaluation...")
        report = framework.evaluate_compliance(
            model=model, dataset=dataset, context=context, stage=args.stage
        )

        # Save report
        save_report(report, args.output_format, args.output_file)

        # Exit with appropriate code
        if args.strict and not report.passed:
            print("Compliance check failed in strict mode")
            sys.exit(1)

    except Exception as e:
        print(f"Error in compliance evaluation: {e}")
        if args.debug:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
