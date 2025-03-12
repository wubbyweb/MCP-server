from mcp.server.fastmcp import FastMCP
import aiohttp
import json
from datetime import datetime

# Initialize FastMCP server
mcp = FastMCP("weather_server")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Helper functions (implement API calls and data formatting here)

# Define tools
@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get the weather forecast for a given location."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        # First, get the grid endpoint for the coordinates
        points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
        async with session.get(points_url, headers=headers) as response:
            if response.status != 200:
                return f"Error: Unable to get forecast data (Status: {response.status})"
            
            points_data = await response.json()
            forecast_url = points_data["properties"]["forecast"]
        
        # Then, get the actual forecast
        async with session.get(forecast_url, headers=headers) as response:
            if response.status != 200:
                return f"Error: Unable to get forecast data (Status: {response.status})"
            
            forecast_data = await response.json()
            periods = forecast_data["properties"]["periods"]
            
            # Format the next 3 periods of forecast
            forecast_text = "Weather Forecast:\n\n"
            for period in periods[:3]:
                forecast_text += f"{period['name']}:\n"
                forecast_text += f"Temperature: {period['temperature']}°{period['temperatureUnit']}\n"
                forecast_text += f"Conditions: {period['shortForecast']}\n"
                forecast_text += f"Wind: {period['windSpeed']} {period['windDirection']}\n\n"
                
            return forecast_text

@mcp.tool()
async def get_alerts(area: str) -> str:
    """Get weather alerts for a given area."""
    # Implement alert retrieval logic here
    pass

# Run the server
if __name__ == "__main__":
    mcp.run()
