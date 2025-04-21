"""
Integration tests for Fujitsu Social Digital Twin MCP Server
Note: These tests require a valid API key to run
"""

import pytest
import os
import asyncio
from unittest import skipIf

# Import modules to test
from fujitsu_sdt_mcp.server import (
    list_simulations,
    list_simdata,
    get_digital_rehearsal_overview,
    get_simulation_metrics_explanation,
    create_natural_language_simulation_config
)

# Check environment variables
API_KEY_EXISTS = bool(os.environ.get("FUJITSU_API_KEY", ""))


@skipIf(not API_KEY_EXISTS, "Skipping tests because API key is not set")
class TestIntegration:
    """Integration tests
    
    Note: These tests connect to the actual API,
    so they require valid API keys and environment variables.
    """

    @pytest.mark.asyncio
    async def test_list_simulations(self):
        """Integration test for listing simulations"""
        result = await list_simulations()
        assert result["success"] is True
        assert "data" in result

    @pytest.mark.asyncio
    async def test_list_simdata(self):
        """Integration test for listing simulation data"""
        result = await list_simdata()
        assert result["success"] is True
        assert "data" in result


class TestResourcesIntegration:
    """Integration tests for resources"""
    
    def test_get_resources(self):
        """Test retrieving resources"""
        # Verify that resource retrieval works properly
        overview = get_digital_rehearsal_overview()
        assert isinstance(overview, str)
        assert len(overview) > 100
        
        explanation = get_simulation_metrics_explanation()
        assert isinstance(explanation, str)
        assert len(explanation) > 100


class TestNLPFunctionsIntegration:
    """Integration tests for NLP functions"""
    
    def test_natural_language_config_creation(self):
        """Test creating configuration from natural language"""
        # Traffic simulation
        traffic_description = "Investigating the causes of traffic congestion during morning rush hour in Tokyo"
        traffic_config = create_natural_language_simulation_config(traffic_description)
        assert traffic_config["simulationType"] == "traffic"
        assert "parameters" in traffic_config
        
        # Road pricing
        pricing_description = "Evaluating the effects of congestion-based variable road pricing in the city center"
        pricing_config = create_natural_language_simulation_config(pricing_description)
        assert pricing_config["simulationType"] == "road_pricing"
        assert "parameters" in pricing_config


if __name__ == "__main__":
    if not API_KEY_EXISTS:
        print("Warning: API key is not set, integration tests will be skipped")
    pytest.main(["-v"])
