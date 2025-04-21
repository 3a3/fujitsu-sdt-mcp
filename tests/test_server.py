"""
Tests for Fujitsu Social Digital Twin MCP Server
"""

import pytest
import json
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock

# Import modules to test
from fujitsu_sdt_mcp.server import (
    mcp,
    FujitsuSocialDigitalTwinClient,
    format_api_error,
    format_simulation_result,
    get_digital_rehearsal_overview,
    get_simulation_metrics_explanation,
    get_scenario_examples,
    list_simulations,
    start_simulation,
    get_simulation_result,
    get_metrics,
    list_simdata,
    get_simdata,
    analyze_traffic_simulation,
    compare_scenarios,
    create_natural_language_simulation_config
)


class TestUtilityFunctions:
    """Tests for utility functions"""

    def test_format_api_error(self):
        """Test the API error formatting function"""
        result = format_api_error(404, "Resource not found")
        assert result["success"] is False
        assert result["status_code"] == 404
        assert result["error"] == "Resource not found"

    def test_format_simulation_result(self):
        """Test the simulation result formatting function"""
        sample_data = {"key": "value"}
        result = format_simulation_result(sample_data)
        assert result["success"] is True
        assert result["data"] == sample_data


class TestResources:
    """Tests for resource definitions"""

    def test_digital_rehearsal_overview(self):
        """Test the digital rehearsal overview resource"""
        overview = get_digital_rehearsal_overview()
        assert isinstance(overview, str)
        assert "Digital Rehearsal" in overview
        assert "traffic optimization" in overview

    def test_simulation_metrics_explanation(self):
        """Test the simulation metrics explanation resource"""
        explanation = get_simulation_metrics_explanation()
        assert isinstance(explanation, str)
        assert "co2" in explanation
        assert "travelTime" in explanation

    def test_scenario_examples(self):
        """Test the scenario examples resource"""
        examples = get_scenario_examples()
        assert isinstance(examples, str)
        assert "Traffic Optimization Scenario" in examples
        assert "Road Pricing Scenario" in examples


class TestAPIClient:
    """Tests for the API client"""

    @pytest.fixture
    def mock_client(self):
        """Create a mock HTTP client"""
        client = AsyncMock()
        return client

    @pytest.mark.asyncio
    async def test_get_simulations(self, mock_client):
        """Test fetching simulations list"""
        # Setup mock response
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "simulations": [
                {
                    "id": "sim-123",
                    "name": "Test Simulation",
                    "status": "finished"
                }
            ]
        }
        mock_response.raise_for_status = AsyncMock()
        mock_client.get.return_value = mock_response

        # Instantiate client and call method
        client = FujitsuSocialDigitalTwinClient(mock_client)
        result = await client.get_simulations()

        # Verify results
        assert result["success"] is True
        assert "data" in result
        assert "simulations" in result["data"]
        assert result["data"]["simulations"][0]["id"] == "sim-123"
        mock_client.get.assert_called_once_with("/api/simulations")


class TestTools:
    """Tests for tool implementations"""

    @pytest.fixture
    def mock_api_client(self):
        """Create a mock API client"""
        with patch("fujitsu_sdt_mcp.server.get_http_client") as mock_get_client:
            client = AsyncMock()
            api_client = MagicMock()
            
            # Mock API client methods
            api_client.get_simulations = AsyncMock()
            api_client.get_simulations.return_value = {
                "success": True,
                "data": {
                    "simulations": [
                        {
                            "id": "sim-123",
                            "name": "Test Simulation",
                            "status": "finished"
                        }
                    ]
                }
            }
            
            mock_get_client.return_value.__aenter__.return_value = client
            mock_get_client.return_value.__aexit__.return_value = None
            
            with patch("fujitsu_sdt_mcp.server.FujitsuSocialDigitalTwinClient") as mock_client_class:
                mock_client_class.return_value = api_client
                yield api_client

    @pytest.mark.asyncio
    async def test_list_simulations(self, mock_api_client):
        """Test the list simulations tool"""
        result = await list_simulations()
        assert result["success"] is True
        assert "data" in result
        assert "simulations" in result["data"]
        mock_api_client.get_simulations.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_simulation(self, mock_api_client):
        """Test the start simulation tool"""
        mock_api_client.start_simulation.return_value = {
            "success": True,
            "data": {
                "id": "sim-123",
                "status": "running"
            }
        }
        
        result = await start_simulation("simdata-123")
        assert result["success"] is True
        assert result["data"]["status"] == "running"
        mock_api_client.start_simulation.assert_called_once_with("simdata-123")


class TestNLPFunctions:
    """Tests for NLP-related functions"""

    def test_create_traffic_config(self):
        """Test creating traffic simulation config"""
        description = "Investigating traffic congestion during morning rush hour in Tokyo"
        result = create_natural_language_simulation_config(description)
        
        assert result["simulationType"] == "traffic"
        assert "parameters" in result
        assert result["parameters"].get("region") == "Tokyo"
        assert result["parameters"].get("timeRange") == "morning_rush"

    def test_create_escooter_config(self):
        """Test creating e-scooter simulation config"""
        description = "Testing the effects of deploying 100 e-scooters with a demand-based strategy"
        result = create_natural_language_simulation_config(description)
        
        assert result["simulationType"] == "escooter"
        assert "parameters" in result
        assert result["parameters"].get("scooterCount") == 100
        assert result["parameters"].get("deploymentStrategy") == "demand_based"


if __name__ == "__main__":
    pytest.main(["-v"])
