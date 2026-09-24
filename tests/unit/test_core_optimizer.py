import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Add project root to Python path first
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import project modules
from gepa_optimizer.core.optimizer import GepaOptimizer
from gepa_optimizer.models import OptimizationConfig

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

@pytest.mark.asyncio
async def test_train_basic(mocker, mock_env_vars):
    # Mock the GEPA optimize function
    mock_gepa = mocker.patch('gepa.optimize')
    mock_gepa.return_value = 'optimized_prompt'
    
    # Mock the custom adapter to avoid real API calls
    mock_adapter = mocker.patch('gepa_optimizer.core.optimizer.CustomGepaAdapter')
    
    # Mock the converter to return proper data
    mock_converter = mocker.patch('gepa_optimizer.core.optimizer.UniversalConverter')
    mock_converter.return_value.convert.return_value = ([{"input": "Hello", "output": "World"}], [])
    
    config = OptimizationConfig(
        model="openai/gpt-4o",
        reflection_model="openai/gpt-4o",
        max_iterations=5,
        max_metric_calls=10,
        batch_size=2
    )
    
    optimizer = GepaOptimizer(config=config)
    data = [{"input": "Hello", "output": "World"}]
    
    result = await optimizer.train(
        seed_prompt="You are a test prompt",
        dataset=data,
        max_metric_calls=1
    )
    
    assert result is not None
    assert hasattr(result, 'status')
    assert hasattr(result, 'prompt')

@pytest.mark.asyncio
async def test_train_invalid_input(mocker, mock_env_vars):
    # Mock the GEPA optimize function
    mock_gepa = mocker.patch('gepa.optimize')
    mock_gepa.return_value = 'optimized_prompt'
    
    with pytest.raises(ValueError) as exc_info:
        config = OptimizationConfig(
            model="",  # Invalid empty model name
            reflection_model="openai/gpt-4o",
            max_iterations=5,
            max_metric_calls=10,
            batch_size=2
        )
        
    assert "Model name is required" in str(exc_info.value)

@pytest.mark.asyncio
async def test_train_empty_dataset(mocker, mock_env_vars):
    # Mock the GEPA optimize function
    mock_gepa = mocker.patch('gepa.optimize')
    mock_gepa.return_value = 'optimized_prompt'
    
    # Mock the custom adapter to avoid real API calls
    mocker.patch('gepa_optimizer.core.optimizer.CustomGepaAdapter')
    
    # Mock the converter to return empty datasets
    mock_converter = mocker.patch('gepa_optimizer.core.optimizer.UniversalConverter')
    mock_converter.return_value.convert.return_value = ([], [])  # Return empty train and validation sets
    
    config = OptimizationConfig(
        model="openai/gpt-4o",
        reflection_model="openai/gpt-4o",
        max_iterations=5,
        max_metric_calls=10,
        batch_size=2
    )
    
    optimizer = GepaOptimizer(config=config)
    
    result = await optimizer.train(
        seed_prompt="You are a test prompt",
        dataset=[],
        max_metric_calls=1
    )
    
    assert result.status == 'failed'
    assert "Dataset appears to be empty after conversion" in result.error_message
