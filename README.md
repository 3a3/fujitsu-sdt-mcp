[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/3a3-fujitsu-sdt-mcp-badge.png)](https://mseep.ai/app/3a3-fujitsu-sdt-mcp)

# Fujitsu Social Digital Twin MCP Server

[![smithery badge](https://smithery.ai/badge/@3a3/fujitsu-sdt-mcp)](https://smithery.ai/server/@3a3/fujitsu-sdt-mcp)

This project integrates [Fujitsu's Social Digital Twin and Digital Rehearsal API](https://portal.research.global.fujitsu.com/converging-technology/) with the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), allowing Large Language Models (LLMs) to access Fujitsu's Digital Rehearsal API through natural language.

<a href="https://glama.ai/mcp/servers/@3a3/fujitsu-sdt-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@3a3/fujitsu-sdt-mcp/badge" alt="Fujitsu Social Digital Twin Server MCP server" />
</a>

## Overview

Fujitsu's Social Digital Twin recreates not only the state of people and objects in the digital space based on real-world data, but also entire economic and social activities. Its core function, "Digital Rehearsal," enables users to simulate human and social behavior in a digital space before implementing measures in the real world, allowing for advance verification of their effects and impacts.

This project uses MCP to bridge the gap between LLMs and the Digital Rehearsal API, enabling users to run simulations and analyze results using natural language.

## Key Features

- Retrieve and display simulation lists
- Start simulations
- Retrieve and analyze simulation results
- Manage simulation data
- Analyze traffic simulations
- Compare scenarios
- Generate simulation configurations from natural language

## Prerequisites

- Python 3.13 or higher
- Access to Fujitsu API Gateway (API Key)
- MCP-compatible LLM client (e.g., Claude Desktop)

## Installation

### Installing via Smithery

To install Fujitsu Social Digital Twin Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@3a3/fujitsu-sdt-mcp):

```bash
npx -y @smithery/cli install @3a3/fujitsu-sdt-mcp --client claude
```

### 1. Clone the Repository

```bash
git clone https://github.com/3a3/fujitsu-sdt-mcp.git
cd fujitsu-sdt-mcp
```

### 2. Set Up Environment

**Using uv (recommended)**:

First, install uv:

```bash
# Install uv using pip
pip install uv

# Or using curl (Linux/macOS)
curl -sSf https://astral.sh/uv/install.sh | sh
```

Then, set up your environment with uv:

```bash
# Create virtual environment
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Unix/MacOS:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

Alternatively, you can use the provided setup script:

```bash
# Make the script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### 3. Set Environment Variables

```bash
# Windows:
set FUJITSU_API_BASE_URL=https://apigateway.research.global.fujitsu.com/sdtp
set FUJITSU_API_KEY=your_api_key_here

# Unix/MacOS:
export FUJITSU_API_BASE_URL=https://apigateway.research.global.fujitsu.com/sdtp
export FUJITSU_API_KEY=your_api_key_here
```

Alternatively, you can create a `.env` file with the following settings:

```
FUJITSU_API_BASE_URL=https://apigateway.research.global.fujitsu.com/sdtp
FUJITSU_API_KEY=your_api_key_here
```

## Usage

### Starting the MCP Server

```bash
python -m fujitsu_sdt_mcp
```

The server communicates using standard I/O with MCP clients.

### Using the Interactive Client

A simple client is also provided for direct interaction with the MCP server:

```bash
python client.py
```

When you start the client, a list of available resources and tools will be displayed, and you can call them from the command line.

### Setup with Claude Desktop

To use the server with MCP-compatible LLM clients such as Claude Desktop:

1. Open Claude Desktop
2. Go to Settings > Developer Settings > Edit Config File
3. Add the following settings:

```json
"command": "uvx",
"args": [
    "fujitsu-sdt-mcp"
],
"env": {
    "FUJITSU_API_BASE_URL": "https://apigateway.research.global.fujitsu.com/sdtp",
    "FUJITSU_API_KEY": "your_api_key_here"
}
```

4. Restart Claude Desktop

## Resources and Tools

### Resources

- `resource://digital_rehearsal_overview`: Overview of Digital Rehearsal technology
- `resource://simulation_metrics_explanation`: Explanation of simulation metrics
- `resource://scenario_examples`: Example scenarios

### Tools

- `list_simulations`: Retrieve a list of simulations
- `start_simulation`: Start a simulation
- `get_simulation_result`: Retrieve simulation results
- `get_metrics`: Retrieve simulation metrics
- `list_simdata`: Retrieve a list of simulation data
- `get_simdata`: Retrieve simulation data
- `analyze_traffic_simulation`: Analyze traffic simulation
- `compare_scenarios`: Compare scenarios
- `create_natural_language_simulation_config`: Generate simulation settings from natural language

## Usage Examples

### Retrieving a List of Simulations

```
tool list_simulations
```

### Starting a Simulation

```
tool start_simulation {"simdataId": "your_simdata_id"}
```

### Analyzing Traffic Simulation

```
tool analyze_traffic_simulation {"simulationId": "your_simulation_id", "region": "Tokyo", "timeRange": "morning rush hour", "scenario": "traffic optimization"}
```

### Generating Simulation Settings from Natural Language

```
tool create_natural_language_simulation_config {"description": "I want to run a traffic optimization simulation during morning rush hour in Tokyo"}
```

## Example LLM Interaction

```
User: I want to run a traffic simulation during morning rush hour in Tokyo

Claude: I can help you run a traffic simulation for Tokyo's morning rush hour. Here's how we can set it up.

First, let's generate simulation settings from your natural language description:
[Tool execution: create_natural_language_simulation_config]

Generated settings:
{
  "simulationType": "traffic",
  "parameters": {
    "region": "Tokyo",
    "timeRange": "morning_rush"
  },
  "name": "traffic_20250416_123045"
}

Next, let's check available simulation data:
[Tool execution: list_simdata]

From this data, I can start a simulation using Tokyo's morning traffic data.
I've selected the appropriate simulation data ID and will start the simulation:
[Tool execution: start_simulation]

The simulation has started. The simulation ID is "sim_12345".
It will take some time for the results to be available. Once complete, I'll analyze them.

(After simulation completes)
Let's analyze the simulation results:
[Tool execution: analyze_traffic_simulation]

Analysis results:
- CO2 emissions: 1,250kg
- Average travel time: 42 minutes
- Total traffic volume: 15,700 vehicles

From these results, I can see that the Shibuya-Shinjuku route experiences particularly severe congestion.
Here are some potential improvements:
1. Optimize traffic signal control
2. Implement one-way traffic on certain roads during specific times
3. Increase public transportation frequency

Would you like to see a more detailed analysis?
```

## Contributing

Please report bugs or feature requests via GitHub Issues. Pull requests are welcome.

## License

This project is released under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Fujitsu Corporation - Development of Social Digital Twin technology
- Model Context Protocol (MCP) - Enabling seamless integration with LLMs
