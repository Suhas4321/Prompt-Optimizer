# 🚀 GEPA Universal Prompt Optimizer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **An alpha-stage Python framework for experimenting with prompt optimization
> across text, vision, and multimodal tasks using configurable evaluators and
> token budgets.**

[Try the Hugging Face demo](https://huggingface.co/spaces/Suhasdev/Universal-prompt-Optimizer)

## 🎯 What is GEPA Optimizer?

GEPA Optimizer is a sophisticated framework that automatically improves prompts for Large Language Models (LLMs) by iteratively evaluating and refining them based on performance metrics. Think of it as "AutoML for prompts" - it takes your initial prompt and dataset, then uses advanced optimization techniques to create a better-performing prompt.

### Key Capabilities

- **🔄 Universal Prompt Optimization**: Works with any LLM provider (OpenAI, Anthropic, Google, Hugging Face)
- **👁️ Multi-Modal Support**: Optimize prompts for vision-capable models (GPT-4V, Claude-3, Gemini)
- **📊 Advanced Evaluation**: Comprehensive metrics for UI tree extraction and general prompt performance
- **🧪 Research-oriented implementation**: Async execution, validation, logging, and extension points for experimentation
- **⚙️ Flexible Configuration**: Easy-to-use configuration system for any optimization scenario
- **💰 Cost Optimization**: Built-in budget controls and cost estimation
- **🎨 UI Tree Extraction**: Specialized for optimizing UI interaction and screen understanding tasks
- **🔧 Extensible Architecture**: Create custom evaluators and adapters for any use case

## 🚀 Quick Start

### Installation

The package is not currently published on PyPI. Install it from source:

```bash
git clone https://github.com/Suhas4321/Prompt-Optimizer.git
cd Prompt-Optimizer
python -m pip install -e .
```

### Basic Usage

```python
import asyncio
from gepa_optimizer import GepaOptimizer, OptimizationConfig

async def optimize_prompt():
    # Configure your optimization
    config = OptimizationConfig(
        model="openai/gpt-4o",                    # Your target model
        reflection_model="openai/gpt-4o",         # Model for self-reflection
        max_iterations=10,                        # Budget: optimization rounds
        max_metric_calls=50,                      # Budget: evaluation calls
        batch_size=4                              # Batch size for evaluation
    )
    
    # Initialize optimizer
    optimizer = GepaOptimizer(config=config)
    
    # Your training data
    dataset = [
        {"input": "What is artificial intelligence?", "output": "AI is a field of computer science..."},
        {"input": "Explain machine learning", "output": "Machine learning is a subset of AI..."},
        {"input": "What are neural networks?", "output": "Neural networks are computing systems..."}
    ]
    
    # Optimize your prompt
    result = await optimizer.train(
        seed_prompt="You are a helpful AI assistant that explains technical concepts clearly.",
        dataset=dataset
    )
    
    print(f"✅ Optimization completed!")
    print(f"📈 Performance improvement: {result.improvement_percent:.2f}%")
    print(f"🎯 Optimized prompt: {result.prompt}")
    print(f"⏱️ Time taken: {result.optimization_time:.2f}s")

# Run the optimization
asyncio.run(optimize_prompt())
```

### UI Tree Extraction (Vision Models)

```python
import asyncio
from gepa_optimizer import GepaOptimizer, OptimizationConfig

async def optimize_ui_prompt():
    config = OptimizationConfig(
        model="openai/gpt-4o",                    # Vision-capable model
        reflection_model="openai/gpt-4o",
        max_iterations=15,
        max_metric_calls=75,
        batch_size=3
    )
    
    optimizer = GepaOptimizer(config=config)
    
    # UI screenshot data with images and JSON trees
    dataset = {
        'json_dir': 'json_tree',           # Directory with ground truth JSON files
        'screenshots_dir': 'screenshots',  # Directory with UI screenshots
        'type': 'ui_tree_dataset'          # Dataset type
    }
    
    result = await optimizer.train(
        seed_prompt="Analyze the UI screenshot and extract all elements as JSON.",
        dataset=dataset
    )
    
    print(f"🎯 Optimized UI prompt: {result.prompt}")
    print(f"📊 Improvement: {result.improvement_percent:.2f}%")

asyncio.run(optimize_ui_prompt())
```

### Universal Custom Use Cases

```python
import asyncio
from gepa_optimizer import (
    GepaOptimizer, OptimizationConfig, ModelConfig,
    BaseEvaluator, BaseLLMClient, VisionLLMClient
)

class CustomEvaluator(BaseEvaluator):
    """Your custom evaluation logic for any use case"""
    
    def evaluate(self, predicted: str, expected: str) -> Dict[str, float]:
        # Implement your custom metrics
        accuracy = calculate_accuracy(predicted, expected)
        relevance = calculate_relevance(predicted, expected)
        
        return {
            "accuracy": accuracy,
            "relevance": relevance,
            "composite_score": (accuracy + relevance) / 2
        }

async def custom_optimization():
    # Create your custom components
    llm_client = VisionLLMClient(
        provider="openai",
        model_name="gpt-4o",
        api_key="your-api-key"
    )
    evaluator = CustomEvaluator()
    
    # Configure optimization
    config = OptimizationConfig(
        model="openai/gpt-4o",
        reflection_model="openai/gpt-4o",
        max_iterations=10,
        max_metric_calls=50
    )
    
    # Use universal adapter
    optimizer = GepaOptimizer(
        config=config,
        adapter_type="universal",
        llm_client=llm_client,
        evaluator=evaluator
    )
    
    # Your custom dataset
    dataset = [
        {"input": "Your input", "output": "Expected output"},
        # ... more examples
    ]
    
    result = await optimizer.train(
        seed_prompt="Your initial prompt",
        dataset=dataset
    )
    
    print(f"🎯 Optimized prompt: {result.prompt}")

asyncio.run(custom_optimization())
```

## 📚 Comprehensive Examples

### 1. Multi-Provider Setup

```python
from gepa_optimizer import OptimizationConfig, ModelConfig

# Using different providers for main and reflection models
config = OptimizationConfig(
    model=ModelConfig(
        provider="openai",
        model_name="gpt-4o",
        api_key="your-openai-key",
        temperature=0.7
    ),
    reflection_model=ModelConfig(
        provider="anthropic",
        model_name="claude-3-opus-20240229",
        api_key="your-anthropic-key",
        temperature=0.5
    ),
    max_iterations=30,
    max_metric_calls=200,
    batch_size=6
)
```

### 2. Budget and Cost Control

```python
config = OptimizationConfig(
    model="openai/gpt-4o",
    reflection_model="openai/gpt-3.5-turbo",  # Cheaper reflection model
    max_iterations=20,
    max_metric_calls=100,
    batch_size=4,
    max_cost_usd=50.0,                        # Budget limit
    timeout_seconds=1800                      # 30 minute timeout
)

# Check estimated costs before running
cost_estimate = config.get_estimated_cost()
print(f"💰 Estimated cost range: {cost_estimate}")
```

### 3. Advanced Configuration

```python
config = OptimizationConfig(
    model="openai/gpt-4o",
    reflection_model="openai/gpt-4o",
    max_iterations=50,
    max_metric_calls=300,
    batch_size=8,
    
    # Advanced settings
    early_stopping=True,
    learning_rate=0.02,
    multi_objective=True,
    objectives=["accuracy", "relevance", "clarity"],
    
    # Data settings
    train_split_ratio=0.85,
    min_dataset_size=5,
    
    # Performance settings
    parallel_evaluation=True,
    use_cache=True
)
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    GEPA Universal Prompt Optimizer              │
├─────────────────────────────────────────────────────────────────┤
│  User Interface Layer                                           │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │  GepaOptimizer  │  │ optimize_prompt │                      │
│  │   (Main API)    │  │   (Convenience) │                      │
│  └─────────────────┘  └─────────────────┘                      │
├─────────────────────────────────────────────────────────────────┤
│  Core Processing Layer                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │CustomGepaAdapter│  │UniversalAdapter │  │UniversalConverter│ │
│  │  (UI Tree)      │  │  (Universal)    │  │ (Data Converter)│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  Evaluation & LLM Layer                                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │UITreeEvaluator  │  │BaseEvaluator    │  │VisionLLMClient  │ │
│  │ (UI Metrics)    │  │ (Custom Metrics)│  │  (LLM Interface)│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  Data & Utility Layer                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   DataLoader    │  │  APIKeyManager  │  │    Exceptions   │ │
│  │ (File Loading)  │  │ (Key Management)│  │   (Error Handling)│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
gepa-optimizer/
├── gepa_optimizer/              # Main package
│   ├── core/                   # Core optimization engine
│   │   ├── optimizer.py        # Main GepaOptimizer class
│   │   ├── custom_adapter.py   # UI tree GEPA integration
│   │   ├── universal_adapter.py # Universal GEPA integration
│   │   ├── base_adapter.py     # Base adapter class
│   │   └── result.py           # Result processing
│   ├── models/                 # Configuration and data models
│   │   ├── config.py           # Configuration classes
│   │   ├── dataset.py          # Dataset models
│   │   └── result.py           # Result models
│   ├── data/                   # Data conversion and validation
│   │   ├── converters.py       # Universal data converter
│   │   ├── loaders.py          # File loading utilities
│   │   └── validators.py       # Data validation
│   ├── evaluation/             # Evaluation metrics and analysis
│   │   ├── ui_evaluator.py     # UI tree evaluation metrics
│   │   └── base_evaluator.py   # Base evaluator class
│   ├── llms/                   # LLM client integrations
│   │   ├── vision_llm.py       # Multi-modal LLM client
│   │   └── base_llm.py         # Base LLM client class
│   ├── utils/                  # Utilities and helpers
│   │   ├── api_keys.py         # API key management
│   │   ├── exceptions.py       # Custom exceptions
│   │   ├── helpers.py          # Helper functions
│   │   ├── logging.py          # Logging utilities
│   │   └── metrics.py          # Metrics utilities
│   └── cli.py                  # Command-line interface
├── tests/                      # Test suite
├── examples/                   # Usage examples
├── docs/                       # Documentation
└── requirements.txt            # Dependencies
```

## 🔧 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- API keys for your chosen LLM providers

### Environment Setup

1. **Install the package:**
   ```bash
   python -m pip install -e .
   ```

2. **Set up environment variables:**
   ```bash
   # For OpenAI
   export OPENAI_API_KEY="your-openai-api-key"
   
   # For Anthropic
   export ANTHROPIC_API_KEY="your-anthropic-api-key"
   
   # For Google Gemini
   export GOOGLE_API_KEY="your-google-api-key"
   
   # For Hugging Face
   export HUGGINGFACE_API_KEY="your-hf-api-key"
   ```

3. **Or use a .env file:**
   ```env
   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   GOOGLE_API_KEY=your-google-api-key
   HUGGINGFACE_API_KEY=your-hf-api-key
   ```

## 📖 Documentation

| Resource | Description |
|----------|-------------|
| [Examples](examples/) | Practical examples and tutorials |
| [Architecture diagrams](docs/architecture_diagrams.md) | Components and data flow |
| [Clean architecture diagram](docs/clean_architecture_diagram.md) | Layered system view |
| [Detailed implementation analysis](DETAILED_LLD_ANALYSIS.md) | Current implementation notes |

## 🎯 Use Cases

- **🤖 Chatbot Optimization**: Improve response quality and consistency
- **🖥️ UI Automation**: Optimize prompts for screen understanding and interaction
- **📝 Content Generation**: Enhance prompts for creative writing, summaries, etc.
- **💻 Code Generation**: Optimize prompts for programming tasks
- **👁️ Multi-modal Applications**: Vision + text prompt optimization
- **🎯 Domain-Specific Tasks**: Fine-tune prompts for specialized domains
- **📊 Data Analysis**: Optimize prompts for data interpretation and analysis
- **🔍 Search & Retrieval**: Improve search query optimization
- **📚 Educational Content**: Optimize prompts for learning and teaching
- **🎨 Creative Writing**: Enhance prompts for creative and artistic tasks


Performance depends on the model, dataset, evaluator, sample size, and
optimization budget. This repository does not claim a universal improvement
percentage; treat the included examples as experiments to reproduce and
measure for a specific task.

## 🔒 Security & Privacy

- API keys can be loaded from environment variables or a local `.env` file;
  `.env` files are excluded by `.gitignore`.
- Prompts and evaluation samples are sent to the configured model provider.
  Review that provider's data policy before using sensitive material.
- Logs may contain prompts, model outputs, feedback, and scores. Do not use
  confidential datasets without first configuring appropriate log handling.
- This is an alpha research project. It has not undergone a security or
  compliance audit.

## 🧪 Testing & Validation

The GEPA Universal Prompt Optimizer includes comprehensive test suites that demonstrate the library's capabilities across different use cases. Each test file showcases specific features and provides real-world examples of optimization.

### 🧪 Test Suite Overview

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gepa_optimizer

# Run specific test categories
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests

# Run individual test files
python test_customer_service_optimization.py
python test_text_generation.py
python test_ui_optimization.py
```

### 📋 Test Files Documentation

#### 1. 🎯 Customer Service Optimization Test
**File:** `test_customer_service_optimization.py`

**Purpose:** Demonstrates universal adapter with custom business-specific evaluation metrics for customer service applications.

**What it tests:**
- ✅ **Universal Adapter**: Shows how the universal adapter works with any use case
- ✅ **Custom Evaluation Metrics**: Business-specific metrics (helpfulness, empathy, solution focus, professionalism)
- ✅ **Real Dataset**: Uses actual customer service data from Bitext dataset (27K responses)
- ✅ **Multi-Modal Support**: Works with text-only models for customer service optimization
- ✅ **Measurable Improvements**: Shows concrete performance gains

**Key Features Demonstrated:**
```python
class CustomerServiceEvaluator(BaseEvaluator):
    """Custom evaluator with business-specific metrics"""
    
    def evaluate(self, predicted: str, expected: str) -> Dict[str, float]:
        return {
            "helpfulness": self._calculate_helpfulness(predicted, expected),
            "empathy": self._calculate_empathy(predicted),
            "solution_focus": self._calculate_solution_focus(predicted),
            "professionalism": self._calculate_professionalism(predicted),
            "composite_score": weighted_average
        }
```

**Dataset:** 
- **Source**: Bitext Customer Support Training Dataset (27K responses)
- **Format**: CSV with columns: flags, instruction, category, intent, response
- **Categories**: ACCOUNT, ORDER, REFUND, CONTACT, INVOICE
- **Sample Size**: 50 interactions for optimization

**Evaluation note:** results vary with the dataset, evaluator, model, and
budget. Record the seed, configuration, baseline score, optimized score, and
token usage when reporting an experiment.

**Run the test:**
```bash
python test_customer_service_optimization.py
```

---

#### 2. 📝 Text Generation Optimization Test
**File:** `test_text_generation.py`

**Purpose:** Demonstrates universal implementation with custom evaluation metrics for general text generation tasks.

**What it tests:**
- ✅ **Custom Evaluation Logic**: User-defined metrics for text generation quality
- ✅ **Universal Adapter**: Works with any text generation use case
- ✅ **Multi-Metric Evaluation**: Accuracy, relevance, completeness, clarity
- ✅ **Weighted Scoring**: Configurable metric weights for different priorities
- ✅ **Real API Integration**: Full end-to-end optimization with actual LLM calls

**Key Features Demonstrated:**
```python
class TextGenerationEvaluator(BaseEvaluator):
    """Custom evaluator for text generation tasks"""
    
    def evaluate(self, predicted: str, expected: str) -> Dict[str, float]:
        return {
            "accuracy": self._calculate_accuracy(predicted, expected),
            "relevance": self._calculate_relevance(predicted, expected),
            "completeness": self._calculate_completeness(predicted, expected),
            "clarity": self._calculate_clarity(predicted),
            "composite_score": weighted_average
        }
```

**Dataset:**
- **Type**: Technical explanation dataset
- **Samples**: AI/ML concept explanations
- **Format**: Input-output pairs for technical Q&A
- **Size**: 2 detailed samples for testing

**Evaluation note:** use a held-out validation set and report the configured
metrics rather than assuming a fixed improvement range.

**Run the test:**
```bash
python test_text_generation.py
```

---

#### 3. 🖥️ UI Tree Optimization Test
**File:** `test_ui_optimization.py`

**Purpose:** Demonstrates specialized UI tree extraction optimization using vision models and screenshot analysis.

**What it tests:**
- ✅ **Vision Model Integration**: Multi-modal optimization with image + text
- ✅ **UI Tree Extraction**: Specialized for screen understanding tasks
- ✅ **File-based Dataset**: Works with directories of images and JSON files
- ✅ **Legacy Adapter**: Uses the original UI-specific adapter
- ✅ **Screenshot Analysis**: Real UI screenshot processing

**Key Features Demonstrated:**
```python
# UI-specific dataset configuration
dataset = {
    'json_dir': 'json_tree',           # Ground truth JSON files
    'screenshots_dir': 'screenshots',  # UI screenshots
    'type': 'ui_tree_dataset'          # Dataset type
}

# Vision-capable model configuration
config = OptimizationConfig(
    model="openai/gpt-4o",             # Vision model
    reflection_model="openai/gpt-4o",
    max_iterations=10,
    max_metric_calls=20
)
```

**Dataset Requirements:**
- **Images**: Screenshots in `screenshots/` directory (.jpg, .jpeg, .png)
- **JSON**: Ground truth UI trees in `json_tree/` directory (.json)
- **Format**: Matching filenames between images and JSON files
- **Content**: UI screenshots with corresponding element trees

**Evaluation note:** vision-model results and cost depend on image complexity,
provider latency, model choice, and the number of evaluation calls.

**Run the test:**
```bash
python test_ui_optimization.py
```

### 🎯 Test Results Summary

| Test File | Use Case | Adapter Type | Dataset |
|-----------|----------|--------------|---------|
| `test_customer_service_optimization.py` | Customer Service | Universal | CSV sample |
| `test_text_generation.py` | Text Generation | Universal | Technical Q&A |
| `test_ui_optimization.py` | UI Tree Extraction | Legacy | Screenshots + JSON |

### 🔧 Test Configuration

**Prerequisites for running tests:**
1. **API Keys**: Set `OPENAI_API_KEY` in environment or `.env` file
2. **Dependencies**: Install all requirements (`pip install -r requirements.txt`)
3. **Data Files**: For UI test, ensure `screenshots/` and `json_tree/` directories exist
4. **CSV Dataset**: For customer service test, place `Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv` in root directory

**Environment Setup:**
```bash
# Create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_customer_service_optimization.py
python test_text_generation.py
python test_ui_optimization.py
```

### 📊 Understanding Test Output

Each test provides detailed output including:

1. **Configuration Details**: Model settings, iteration counts, batch sizes
2. **Dataset Information**: Sample counts, data structure, validation results
3. **Optimization Progress**: Real-time iteration logs, score improvements
4. **Final Results**: Before/after prompt comparison, performance metrics
5. **Success Indicators**: Clear pass/fail status with detailed explanations

**Example Output:**
```
✅ Optimization completed!
   - Status: completed
   - Iterations: 4
   - Time: 265.63s

📝 PROMPT COMPARISON
🌱 SEED PROMPT: "You are a customer service agent..."
🚀 OPTIMIZED PROMPT: "You are a customer service agent specializing in..."

🎉 Customer Service Optimization Test PASSED!
```

### 🚀 Extending Tests

You can create your own test files by following the patterns in the existing tests:

1. **Create Custom Evaluator**: Inherit from `BaseEvaluator`
2. **Define Your Metrics**: Implement evaluation logic for your use case
3. **Prepare Dataset**: Format your data according to the expected structure
4. **Configure Optimization**: Set up `OptimizationConfig` with your parameters
5. **Run and Validate**: Execute optimization and verify results

This comprehensive test suite ensures that the GEPA Universal Prompt Optimizer works reliably across different domains and use cases, providing confidence in its production readiness.

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes and add tests**
4. **Run tests**: `pytest`
5. **Submit a pull request**

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **🐛 Issues**: [GitHub Issues](https://github.com/Suhas4321/Prompt-Optimizer/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/Suhas4321/Prompt-Optimizer/discussions)
- **📧 Email**: s8hasgrylls@gmail.com
- **📚 Documentation**: [Repository documentation](docs/)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Suhas4321/Prompt-Optimizer&type=Date)](https://star-history.com/#Suhas4321/Prompt-Optimizer&Date)

---

** Made with ❤️ **
