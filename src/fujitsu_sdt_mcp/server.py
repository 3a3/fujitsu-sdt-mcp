"""
MCP Server for Fujitsu Social Digital Twin Digital Rehearsal API  
An MCP server implementation that provides natural language access to the Digital Rehearsal API
"""

import asyncio
import json
import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import TextContent

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

FUJITSU_API_BASE_URL = os.environ.get("FUJITSU_API_BASE_URL", "https://apigateway.research.global.fujitsu.com/sdtp")
FUJITSU_API_KEY = os.environ.get("FUJITSU_API_KEY", "")

mcp = FastMCP("fujitsu-digital-rehearsal")

async def get_http_client():
    return httpx.AsyncClient(
        base_url=FUJITSU_API_BASE_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {FUJITSU_API_KEY}"
        },
        timeout=30.0
    )

def format_api_error(status_code: int, error_detail: str) -> Dict[str, Any]:
    return {
        "success": False,
        "status_code": status_code,
        "error": error_detail
    }

def format_simulation_result(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "success": True,
        "data": result
    }

class FujitsuSocialDigitalTwinClient:
    
    def __init__(self, http_client: httpx.AsyncClient):
        self.client = http_client
    
    async def get_simulations(self) -> Dict[str, Any]:
        try:
            response = await self.client.get("/api/simulations")
            response.raise_for_status()
            return format_simulation_result(response.json())
        except httpx.HTTPStatusError as e:
            logger.error(f"Simulation list retrieval error: {e}")
            return format_api_error(e.response.status_code, str(e))
        except Exception as e:
            logger.error(f"Unexpected error retrieving simulations: {e}")
            return format_api_error(500, str(e))
    
    async def start_simulation(self, simdata_id: str) -> Dict[str, Any]:
        try:
            response = await self.client.post(
                "/api/simulations", 
                json={"simdataId": simdata_id}
            )
            response.raise_for_status()
            return format_simulation_result(response.json())
        except httpx.HTTPStatusError as e:
            logger.error(f"Simulation start error: {e}")
            return format_api_error(e.response.status_code, str(e))
        except Exception as e:
            logger.error(f"Unexpected error starting simulation: {e}")
            return format_api_error(500, str(e))
    
    async def get_simulation_result(self, simulation_id: str) -> Dict[str, Any]:
        try:
            response = await self.client.get(f"/api/simulations/{simulation_id}")
            response.raise_for_status()
            return format_simulation_result(response.json())
        except httpx.HTTPStatusError as e:
            logger.error(f"Simulation result retrieval error: {e}")
            return format_api_error(e.response.status_code, str(e))
        except Exception as e:
            logger.error(f"Unexpected error retrieving simulation results: {e}")
            return format_api_error(500, str(e))
    
    async def get_simulation_file(self, simulation_id: str, file_name: str) -> Dict[str, Any]:
        try:
            response = await self.client.get(f"/api/simulations/{simulation_id}/{file_name}")
            response.raise_for_status()
            return format_simulation_result(response.json())
        except httpx.HTTPStatusError as e:
            logger.error(f"Simulation file retrieval error: {e}")
            return format_api_error(e.response.status_code, str(e))
        except Exception as e:
            logger.error(f"Unexpected error retrieving simulation file: {e}")
            return format_api_error(500, str(e))
    
    async def get_metrics(self, simulation_id: str) -> Dict[str, Any]:
        try:
            response = await self.client.get(f"/api/metrics/{simulation_id}")
            response.raise_for_status()
            return format_simulation_result(response.json())
        except httpx.HTTPStatusError as e:
            logger.error(f"Metrics retrieval error: {e}")
            return format_api_error(e.response.status_code, str(e))
        except Exception as e:
            logger.error(f"Unexpected error retrieving metrics: {e}")
            return format_api_error(500, str(e))
    
    async def get_simdata_list(self) -> Dict[str, Any]:
        try:
            response = await self.client.get("/api/simdata")
            response.raise_for_status()
            return format_simulation_result(response.json())
        except httpx.HTTPStatusError as e:
            logger.error(f"Simulation data list retrieval error: {e}")
            return format_api_error(e.response.status_code, str(e))
        except Exception as e:
            logger.error(f"Unexpected error retrieving simulation data list: {e}")
            return format_api_error(500, str(e))
    
    async def get_simdata(self, simdata_id: str) -> Dict[str, Any]:
        try:
            response = await self.client.get(f"/api/simdata/{simdata_id}")
            response.raise_for_status()
            return format_simulation_result(response.json())
        except httpx.HTTPStatusError as e:
            logger.error(f"Simulation data retrieval error: {e}")
            return format_api_error(e.response.status_code, str(e))
        except Exception as e:
            logger.error(f"Unexpected error retrieving simulation data: {e}")
            return format_api_error(500, str(e))
    
    async def create_simdata(self, config: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = await self.client.post("/api/simdata", json=config)
            response.raise_for_status()
            return format_simulation_result(response.json())
        except httpx.HTTPStatusError as e:
            logger.error(f"Simulation data creation error: {e}")
            return format_api_error(e.response.status_code, str(e))
        except Exception as e:
            logger.error(f"Unexpected error creating simulation data: {e}")
            return format_api_error(500, str(e))

@mcp.resource("resource://digital_rehearsal_overview")
def get_digital_rehearsal_overview() -> str:
    """富士通デジタルリハーサル技術の概要"""
    return """
富士通のデジタルリハーサル技術は、実社会での実装前にデジタル空間でソーシャルソリューションの検証を可能にします。AIドリブンのビッグデータ分析と行動経済学を活用して人間と社会の行動を再現することで、政策や施策の影響を予測します。

主な特徴：
- デジタルツインを使用した社会行動予測
- 政策効果の事前検証
- マルチシナリオシミュレーション機能

ユースケース：
1. 交通最適化
2. e-モビリティ展開計画
3. 環境影響評価
4. 災害対策検証
5. 都市開発分析

このAPIは、様々なシミュレーションシナリオと分析ツールへのアクセスを提供します。
"""

@mcp.resource("resource://simulation_metrics_explanation")
def get_simulation_metrics_explanation() -> str:
    """シミュレーションメトリクスの説明"""
    return """
シミュレーションメトリクスの説明：

1. co2: 総CO2排出量（kg）
2. travelTime: 平均移動時間（分）
3. travelCost: 平均移動コスト（円）
4. trafficCountTotal: 総交通量
5. escooterUsageRate: eスクーター利用率（%）
6. escooterRevenue: eスクーター収益（円）
7. escooterOpportunityLoss: eスクーター機会損失（円）
8. bayCountWithLowBatteryScooters: バッテリー残量の少ないスクーターを含む充電ベイ数
9. bayAvailableRate: ベイ利用可能率（%）
10. toll: 通行料収入（円）

交通カテゴリ：
- car（車）, pedestrian（歩行者）, escooter（eスクーター）, bicycle（自転車）, truck（トラック）, lost（損失）, pt（公共交通）, park_ride（パーク&ライド）

距離カテゴリ（km）：
- car（車）, pedestrian（歩行者）, escooter（eスクーター）, bicycle（自転車）, bus（バス）, tram（路面電車）, subway（地下鉄）, rail（鉄道）
"""

@mcp.resource("resource://usecase_requirements")
def get_usecase_requirements() -> str:
    """各ユースケースで必要なファイル一覧"""
    return """
# ユースケース別必要ファイル一覧

## 1. e-scooter初期配備
- map.net.xml.gz（交通ネットワークマップデータ）
- station.csv（駅・バス停等の位置データ）
- od.csv.gz（起点-目的地移動データ）
- precondition.json（シミュレーション前提条件設定）

## 2. ダイナミックディスカウント
- map.net.xml.gz（交通ネットワークマップデータ）
- station.csv（駅・バス停等の位置データ）
- od.csv.gz（起点-目的地移動データ）
- precondition.json（シミュレーション前提条件設定）

## 3. 道路閉鎖
- map.net.xml.gz（交通ネットワークマップデータ）
- station.csv（駅・バス停等の位置データ）
- od.csv.gz（起点-目的地移動データ）
- road-closure.csv（閉鎖道路定義データ）
- precondition.json（シミュレーション前提条件設定）

## 4. ロードプライシング
- map.net.xml.gz（交通ネットワークマップデータ）
- station.csv（駅・バス停等の位置データ）
- od.csv.gz（起点-目的地移動データ）
- road-closure.csv（閉鎖道路定義データ）
- road-pricing.csv（道路課金設定データ）
- precondition.json（シミュレーション前提条件設定）

## 5. パーク&ライド
- map.net.xml.gz（交通ネットワークマップデータ）
- station.csv（駅・バス停等の位置データ）
- od.csv.gz（起点-目的地移動データ）
- parking.csv（駐車場定義データ）
- precondition.json（シミュレーション前提条件設定）
"""

@mcp.prompt()
def traffic_simulation_template(region: str, time_range: str, scenario: str, 
                               simulation_results: str) -> str:
    """Traffic simulation analysis template."""
    return f"""
Analyze traffic simulation results for Fujitsu's Social Digital Twin system.

Parameters:
- Region: {region}
- Time range: {time_range}
- Scenario: {scenario}

Results:
{simulation_results}

Analysis Focus:
1. Congestion hotspots
2. Travel time changes
3. CO2 impact
4. Key insights
5. Improvement proposals

Provide clear explanations using non-technical language. Conclude with 2-3 actionable recommendations.
    """

@mcp.prompt()
def escooter_optimization_template(scooter_count: str, deployment_strategy: str, 
                                  rebalancing_frequency: str, pricing_strategy: str,
                                  simulation_results: str) -> str:
    """E-scooter optimization analysis template."""
    return f"""
Analyze e-scooter deployment simulation results for Fujitsu's Social Digital Twin system.

Parameters:
- Scooters: {scooter_count}
- Strategy: {deployment_strategy}
- Rebalancing: Every {rebalancing_frequency} hours
- Pricing: {pricing_strategy}

Results:
{simulation_results}

Analysis Focus:
1. Utilization analysis
2. Revenue evaluation
3. Opportunity loss
4. Optimal locations/times
5. Improvement proposals

Provide insights for operators and policymakers. Conclude with 2-3 strategic recommendations.
    """

@mcp.prompt()
def scenario_comparison_template(scenario1_name: str, scenario1_results: str,
                                scenario2_name: str, scenario2_results: str) -> str:
    """Scenario comparison analysis template."""
    return f"""
Compare two simulation scenarios for Fujitsu's Social Digital Twin system.

Scenario 1: {scenario1_name}
{scenario1_results}

Scenario 2: {scenario2_name}
{scenario2_results}

Comparison Focus:
1. CO2 differences
2. Travel time/cost changes
3. Transportation mode shifts
4. Cost-effectiveness
5. Secondary impacts

Provide policy recommendations and suggest potential hybrid approaches based on analysis.
    """

@mcp.prompt()
def usecase_data_preparation(usecase: str) -> str:
    """ユースケース別のデータ準備ガイド"""
    
    guides = {
        "e-scooter初期配備": """
# e-scooter初期配備データ準備ガイド

## 必要ファイル
1. **map.net.xml.gz**: 交通ネットワークマップデータ
2. **station.csv**: 駅・バス停等の位置データ
3. **od.csv.gz**: 起点-目的地移動データ
4. **precondition.json**: シミュレーション前提条件設定

## シミュレーションパラメータ例
- 地域名: Toyosu
- 開始時間: 9時
- 終了時間: 18時
- eスクーター設置台数: 100台
- 課金設定: 初乗り料金100円、1分あたり20円

## アップロード手順
1. すべてのファイルを準備
2. ファイルをシステムにアップロード
3. シミュレーションパラメータを入力
4. シミュレーション開始
""",

        "ダイナミックディスカウント": """
# ダイナミックディスカウントデータ準備ガイド

## 必要ファイル
1. **map.net.xml.gz**: 交通ネットワークマップデータ
2. **station.csv**: 駅・バス停等の位置データ
3. **od.csv.gz**: 起点-目的地移動データ
4. **precondition.json**: シミュレーション前提条件設定

## シミュレーションパラメータ例
- 地域名: Kawasaki
- 開始時間: 7時
- 終了時間: 10時
- 割引時間帯: 7時-8時
- 割引率: 30%

## アップロード手順
1. すべてのファイルを準備
2. ファイルをシステムにアップロード
3. シミュレーションパラメータを入力
4. シミュレーション開始
""",

        "道路閉鎖": """
# 道路閉鎖データ準備ガイド

## 必要ファイル
1. **map.net.xml.gz**: 交通ネットワークマップデータ
2. **station.csv**: 駅・バス停等の位置データ
3. **od.csv.gz**: 起点-目的地移動データ
4. **road-closure.csv**: 閉鎖道路定義データ
5. **precondition.json**: シミュレーション前提条件設定

## シミュレーションパラメータ例
- 地域名: Toyosu
- 開始時間: 10時
- 終了時間: 11時
- 閉鎖道路ID: road1, road2

## アップロード手順
1. すべてのファイルを準備
2. ファイルをシステムにアップロード
3. シミュレーションパラメータを入力
4. シミュレーション開始
""",

        "ロードプライシング": """
# ロードプライシングデータ準備ガイド

## 必要ファイル
1. **map.net.xml.gz**: 交通ネットワークマップデータ
2. **station.csv**: 駅・バス停等の位置データ
3. **od.csv.gz**: 起点-目的地移動データ
4. **road-closure.csv**: 閉鎖道路定義データ
5. **road-pricing.csv**: 道路課金設定データ
6. **precondition.json**: シミュレーション前提条件設定

## シミュレーションパラメータ例
- 地域名: Toyosu
- 開始時間: 10時
- 終了時間: 11時
- 課金対象道路ID: road1, road2
- 課金額: 500円

## アップロード手順
1. すべてのファイルを準備
2. ファイルをシステムにアップロード
3. シミュレーションパラメータを入力
4. シミュレーション開始
""",

        "パーク&ライド": """
# パーク&ライドデータ準備ガイド

## 必要ファイル
1. **map.net.xml.gz**: 交通ネットワークマップデータ
2. **station.csv**: 駅・バス停等の位置データ
3. **od.csv.gz**: 起点-目的地移動データ
4. **parking.csv**: 駐車場定義データ
5. **precondition.json**: シミュレーション前提条件設定

## シミュレーションパラメータ例
- 地域名: Todoroki
- 開始時間: 15時
- 終了時間: 16時
- 駐車場容量: 200台
- 駐車料金: 100円

## アップロード手順
1. すべてのファイルを準備
2. ファイルをシステムにアップロード
3. シミュレーションパラメータを入力
4. シミュレーション開始
"""
    }
    
    if usecase in guides:
        return guides[usecase]
    else:
        return f"選択されたユースケース「{usecase}」のデータ準備ガイドは現在利用できません。以下のいずれかを選択してください：e-scooter初期配備、ダイナミックディスカウント、道路閉鎖、ロードプライシング、パーク&ライド"

@mcp.tool()
async def list_simulations(ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Returns a comprehensive list of all traffic simulations in the system, 
    including their IDs, names, status, and execution timeframes."""
    async with await get_http_client() as client:
        api_client = FujitsuSocialDigitalTwinClient(client)
        result = await api_client.get_simulations()
    return result

@mcp.tool()
async def start_simulation(simdata_id: str, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Launches a new traffic simulation using the provided simulation dataset configuration, 
    returning the simulation ID and initial status."""    
    try:
        if not simdata_id:
            return format_api_error(400, "simdataId required")
        
        async with await get_http_client() as client:
            api_client = FujitsuSocialDigitalTwinClient(client)
            result = await api_client.start_simulation(simdata_id)
        return result
    except Exception as e:
        logger.error(f"Simulation start error: {e}")
        return format_api_error(500, str(e))

@mcp.tool()
async def get_simulation_result(simulation_id: str, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Retrieves the complete results and output files from a finished traffic simulation, 
    including simulation status and generated result files."""
    try:
        if not simulation_id:
            return format_api_error(400, "simulationId required")
        
        async with await get_http_client() as client:
            api_client = FujitsuSocialDigitalTwinClient(client)
            result = await api_client.get_simulation_result(simulation_id)
        return result
    except Exception as e:
        logger.error(f"Result retrieval error: {e}")
        return format_api_error(500, str(e))

@mcp.tool()
async def get_metrics(simulation_id: str, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Retrieves comprehensive metrics and analytics data from a completed simulation, including 
    travel statistics, emissions data, and traffic flow information."""
    try:
        if not simulation_id:
            return format_api_error(400, "simulationId required")
        
        async with await get_http_client() as client:
            api_client = FujitsuSocialDigitalTwinClient(client)
            result = await api_client.get_metrics(simulation_id)
        return result
    except Exception as e:
        logger.error(f"Metrics retrieval error: {e}")
        return format_api_error(500, str(e))

@mcp.tool()
async def list_simdata(ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Returns a complete list of all simulation datasets available in the system, 
    which can be used as inputs for running new simulations."""
    async with await get_http_client() as client:
        api_client = FujitsuSocialDigitalTwinClient(client)
        result = await api_client.get_simdata_list()
    return result

@mcp.tool()
async def get_simdata(simdata_id: str, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Retrieves the complete configuration and parameter set for a specific simulation dataset, 
    including region settings, time ranges, and scenario parameters."""
    try:
        if not simdata_id:
            return format_api_error(400, "simdataId required")
        
        async with await get_http_client() as client:
            api_client = FujitsuSocialDigitalTwinClient(client)
            result = await api_client.get_simdata(simdata_id)
        return result
    except Exception as e:
        logger.error(f"Simdata retrieval error: {e}")
        return format_api_error(500, str(e))

@mcp.tool()
async def analyze_traffic_simulation(simulation_id: str, region: str = "unknown", 
                               scenario: str = "unknown", time_range: str = "unknown",
                               ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Conducts comprehensive analysis on simulation results, providing insights on traffic patterns, 
    bottlenecks, and optimization opportunities for the specified parameters."""
    try:
        if not simulation_id:
            return format_api_error(400, "simulationId required")
        
        async with await get_http_client() as client:
            api_client = FujitsuSocialDigitalTwinClient(client)
            metrics_result = await api_client.get_metrics(simulation_id)
        
        if not metrics_result.get("success"):
            return metrics_result
        
        analysis = {
            "region": region,
            "timeRange": time_range,
            "scenario": scenario,
            "metrics": metrics_result.get("data", {}).get("metrics", {}),
            "analysis": {
                "timestamp": datetime.now().isoformat(),
                "summary": "Traffic simulation analysis",
                "keyFindings": [
                    f"CO2: {metrics_result.get('data', {}).get('metrics', {}).get('co2', 0)}kg",
                    f"Avg travel time: {metrics_result.get('data', {}).get('metrics', {}).get('travelTime', 0)}min",
                    f"Total traffic: {metrics_result.get('data', {}).get('metrics', {}).get('trafficCountTotal', 0)}"
                ]
            }
        }
        return analysis
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return format_api_error(500, str(e))

@mcp.tool()
async def compare_scenarios(simulation_id1: str, simulation_id2: str, 
                     scenario1_name: str = "Scenario 1", scenario2_name: str = "Scenario 2",
                     ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Performs detailed comparative analysis between two simulation scenarios, highlighting differences 
    in traffic flow, emissions, travel times, and other key metrics."""
    try:
        if not simulation_id1 or not simulation_id2:
            return format_api_error(400, "Two simulation IDs required")
        
        async with await get_http_client() as client:
            api_client = FujitsuSocialDigitalTwinClient(client)
            metrics_result1 = await api_client.get_metrics(simulation_id1)
            metrics_result2 = await api_client.get_metrics(simulation_id2)
        
        if not metrics_result1.get("success") or not metrics_result2.get("success"):
            return format_api_error(500, "Metric retrieval failed")
        
        comparison = {
            "scenario1": {
                "name": scenario1_name,
                "metrics": metrics_result1.get("data", {}).get("metrics", {})
            },
            "scenario2": {
                "name": scenario2_name,
                "metrics": metrics_result2.get("data", {}).get("metrics", {})
            },
            "comparison": {
                "timestamp": datetime.now().isoformat(),
                "co2Difference": metrics_result2.get('data', {}).get('metrics', {}).get('co2', 0) - 
                                metrics_result1.get('data', {}).get('metrics', {}).get('co2', 0),
                "travelTimeDifference": metrics_result2.get('data', {}).get('metrics', {}).get('travelTime', 0) - 
                                        metrics_result1.get('data', {}).get('metrics', {}).get('travelTime', 0),
                "trafficCountDifference": metrics_result2.get('data', {}).get('metrics', {}).get('trafficCountTotal', 0) - 
                                         metrics_result1.get('data', {}).get('metrics', {}).get('trafficCountTotal', 0)
            }
        }
        return comparison
    except Exception as e:
        logger.error(f"Comparison error: {e}")
        return format_api_error(500, str(e))

@mcp.tool()
async def create_natural_language_simulation_config(description: str, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Converts a natural language description into a structured simulation configuration, 
    interpreting user requirements into technical parameters for traffic simulation."""
    try:
        if not description:
            return format_api_error(400, "Description required")
        
        config = {
            "simulationType": "unknown",
            "parameters": {}
        }
        
        description_lower = description.lower()
        
        if any(keyword in description_lower for keyword in ["traffic", "congestion", "road", "signal"]):
            config["simulationType"] = "traffic"
            
            regions = ["Tokyo", "Osaka", "Nagoya", "Fukuoka", "Sapporo", "Sendai", "Hiroshima", "Kyoto"]
            for region in regions:
                if region.lower() in description_lower:
                    config["parameters"]["region"] = region
                    break
            
            if "morning" in description_lower or "rush hour" in description_lower:
                config["parameters"]["timeRange"] = "morning_rush"
            elif "evening" in description_lower:
                config["parameters"]["timeRange"] = "evening_rush"
            elif "daytime" in description_lower:
                config["parameters"]["timeRange"] = "daytime"
            
        elif any(keyword in description_lower for keyword in ["scooter", "e-scooter", "electric"]):
            config["simulationType"] = "escooter"
            
            count_match = re.search(r'(\d+) scooters', description)
            if count_match:
                config["parameters"]["scooterCount"] = int(count_match.group(1))
            
            if "demand" in description_lower:
                config["parameters"]["deploymentStrategy"] = "demand_based"
            elif "grid" in description_lower:
                config["parameters"]["deploymentStrategy"] = "grid_based"
            elif "transit" in description_lower:
                config["parameters"]["deploymentStrategy"] = "transit_focused"
            
        elif any(keyword in description_lower for keyword in ["pricing", "toll", "congestion charge"]):
            config["simulationType"] = "road_pricing"
            
            if "city center" in description_lower:
                config["parameters"]["pricingZone"] = "city_center"
            elif "wider area" in description_lower:
                config["parameters"]["pricingZone"] = "wider_area"
            elif "major roads" in description_lower:
                config["parameters"]["pricingZone"] = "major_roads"
            
            if "fixed" in description_lower:
                config["parameters"]["priceModel"] = "fixed"
            elif "time variable" in description_lower:
                config["parameters"]["priceModel"] = "time_variable"
            elif "congestion" in description_lower:
                config["parameters"]["priceModel"] = "congestion_variable"
            
        else:
            config["simulationType"] = "generic"
            config["parameters"]["description"] = description
        
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        config["name"] = f"{config['simulationType']}_{current_time}"
        
        return config
    except Exception as e:
        logger.error(f"Config generation error: {e}")
        return format_api_error(500, str(e))

@mcp.tool()
async def create_simulation_from_usecase(usecase: str, uploaded_files: Dict[str, str], 
                                  simulation_params: Dict[str, Any], 
                                  ctx: Optional[Context] = None) -> Dict[str, Any]:
    """指定されたユースケースとアップロードされたファイルからシミュレーションを作成・実行します。"""
    try:
        required_files = _get_required_files_for_usecase(usecase)
        missing_files = [f for f in required_files if f not in uploaded_files]
        
        if missing_files:
            return {
                "success": False,
                "error": f"必要なファイルが不足しています: {', '.join(missing_files)}"
            }
        
        # パラメータのバリデーション
        if "region" not in simulation_params:
            return {"success": False, "error": "地域名(region)が指定されていません"}
        if "start" not in simulation_params:
            return {"success": False, "error": "開始時間(start)が指定されていません"}
        if "end" not in simulation_params:
            return {"success": False, "error": "終了時間(end)が指定されていません"}
        
        # ユースケース固有のパラメータを設定
        config = {
            "name": f"{usecase}_{simulation_params['region']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "usecase": _convert_usecase_to_api_format(usecase),
            "region": simulation_params["region"],
            "start": int(simulation_params["start"]),
            "end": int(simulation_params["end"]),
            "vtypes": {
                "car": True,
                "pedestrian": True,
                "escooter": "e-scooter初期配備" == usecase,
                "bicycle": True,
                "pt": True
            }
        }
        
        # ユースケース固有のパラメータを追加
        if usecase == "e-scooter初期配備":
            if "escooter_count" not in simulation_params:
                return {"success": False, "error": "eスクーター台数(escooter_count)が指定されていません"}
            
            config["escooter_count"] = int(simulation_params["escooter_count"])
            
            if "escooter_fee" in simulation_params:
                config["escooter_fee"] = int(simulation_params["escooter_fee"])
        
        elif usecase == "ダイナミックディスカウント":
            if "discount_percentage" not in simulation_params:
                return {"success": False, "error": "割引率(discount_percentage)が指定されていません"}
            
            config["discount_percentage"] = int(simulation_params["discount_percentage"])
            
            if "discount_hours" in simulation_params:
                if isinstance(simulation_params["discount_hours"], list):
                    config["discount_hours"] = simulation_params["discount_hours"]
                else:
                    config["discount_hours"] = [int(h) for h in str(simulation_params["discount_hours"]).split(",")]
        
        elif usecase == "パーク&ライド":
            if "parking_capacity" not in simulation_params:
                return {"success": False, "error": "駐車場容量(parking_capacity)が指定されていません"}
            
            if "parking_fee" not in simulation_params:
                return {"success": False, "error": "駐車料金(parking_fee)が指定されていません"}
            
            config["parking"] = [
                {
                    "id": "parking1",
                    "total": int(simulation_params["parking_capacity"]),
                    "charge": int(simulation_params["parking_fee"]),
                    "type": "car"
                }
            ]
            
            if "parking_locations" in simulation_params and isinstance(simulation_params["parking_locations"], list):
                for i, location in enumerate(simulation_params["parking_locations"]):
                    if i >= len(config["parking"]):
                        config["parking"].append({
                            "id": f"parking{i+1}",
                            "total": int(simulation_params["parking_capacity"]),
                            "charge": int(simulation_params["parking_fee"]),
                            "type": "car"
                        })
                    
                    if isinstance(location, list) and len(location) == 2:
                        config["parking"][i]["pos"] = location
        
        # ファイルパスをパラメータに追加
        file_paths = {}
        for file_key, file_path in uploaded_files.items():
            file_paths[file_key] = file_path
        
        config["input_files"] = file_paths
        
        # シミュレーションデータを作成
        async with await get_http_client() as client:
            api_client = FujitsuSocialDigitalTwinClient(client)
            simdata_result = await api_client.create_simdata(config)
            
            if not simdata_result.get("success"):
                return simdata_result
            
            simdata_id = simdata_result.get("data", {}).get("id")
            
            # シミュレーションを開始
            result = await api_client.start_simulation(simdata_id)
            
            if result.get("success"):
                return {
                    "success": True,
                    "usecase": usecase,
                    "simulation_id": result.get("data", {}).get("id"),
                    "simdata_id": simdata_id,
                    "status": "started",
                    "region": simulation_params["region"],
                    "time_range": f"{simulation_params['start']}時-{simulation_params['end']}時",
                    "config_summary": _get_config_summary(config)
                }
            else:
                return result
    except Exception as e:
        logger.error(f"Error creating simulation from usecase: {e}")
        return format_api_error(500, str(e))

def _get_required_files_for_usecase(usecase: str) -> list[str]:
    """ユースケースごとに必要なファイルのリストを返す"""
    required_files = {
        "e-scooter初期配備": ["map.net.xml.gz", "station.csv", "od.csv.gz", "precondition.json"],
        "ダイナミックディスカウント": ["map.net.xml.gz", "station.csv", "od.csv.gz", "precondition.json"],
        "道路閉鎖": ["map.net.xml.gz", "station.csv", "od.csv.gz", "road-closure.csv", "precondition.json"],
        "ロードプライシング": ["map.net.xml.gz", "station.csv", "od.csv.gz", "road-closure.csv", "road-pricing.csv", "precondition.json"],
        "パーク&ライド": ["map.net.xml.gz", "station.csv", "od.csv.gz", "parking.csv", "precondition.json"]
    }
    
    return required_files.get(usecase, [])

def _convert_usecase_to_api_format(usecase: str) -> str:
    """ユースケース名をAPI形式に変換"""
    mapping = {
        "e-scooter初期配備": "escooter-placement",
        "ダイナミックディスカウント": "dynamic-discount",
        "道路閉鎖": "road-closure",
        "ロードプライシング": "road-pricing",
        "パーク&ライド": "park-and-ride"
    }
    
    return mapping.get(usecase, "generic")

def _get_config_summary(config: Dict[str, Any]) -> str:
    """設定の要約を生成"""
    summary = []
    
    if "name" in config:
        summary.append(f"名前: {config['name']}")
    
    if "usecase" in config:
        summary.append(f"ユースケース: {config['usecase']}")
    
    if "region" in config:
        summary.append(f"地域: {config['region']}")
    
    if "start" in config and "end" in config:
        summary.append(f"時間範囲: {config['start']}時-{config['end']}時")
    
    if "escooter_count" in config:
        summary.append(f"eスクーター台数: {config['escooter_count']}台")
    
    if "escooter_fee" in config:
        summary.append(f"eスクーター料金: {config['escooter_fee']}円")
    
    if "discount_percentage" in config:
        summary.append(f"割引率: {config['discount_percentage']}%")
    
    if "discount_hours" in config:
        summary.append(f"割引時間帯: {', '.join(map(str, config['discount_hours']))}時")
    
    if "parking" in config and config["parking"]:
        parking = config["parking"][0]
        summary.append(f"駐車場容量: {parking.get('total', 0)}台")
        summary.append(f"駐車料金: {parking.get('charge', 0)}円")
    
    return "\n".join(summary)

def main():
    logging.info("Starting Fujitsu Social Digital Twin MCP Server...")
    
    if not FUJITSU_API_KEY:
        logging.warning("FUJITSU_API_KEY not configured")
    
    mcp.run()

if __name__ == "__main__":
    mcp.run()