from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

import structlog
from .tools.get_city import get_city_by_name, get_cities_by_postal_code
from .tools.map import generate_map

logger = structlog.get_logger()

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/get_city")
async def get_city(city: str = None, postal_code: str = None):
    """
    Get city information by name or postal code.

    Args:
        city: City name to search for
        postal_code: Postal code to search for

    Returns:
        JSON response with city information containing nom_standard and dep_code
    """
    try:
        if city:
            # Search by city name
            cities = get_city_by_name(city)
            return JSONResponse({"type": "city_name", "input": city, "results": cities})
        elif postal_code:
            # Search by postal code
            cities = get_cities_by_postal_code(postal_code)
            return JSONResponse(
                {"type": "postal_code", "input": postal_code, "results": cities}
            )
        else:
            return JSONResponse(
                {"error": "Either 'city' or 'postal_code' parameter is required"},
                status_code=400,
            )
    except Exception as e:
        logger.error("Error in get_city endpoint", error=str(e))
        return JSONResponse({"error": f"An error occurred: {str(e)}"}, status_code=500)


@app.get("/map/{city_name}", response_class=HTMLResponse)
async def show_city_map(request: Request, city_name: str, dep_code: str = None):
    """
    Display a map page for the specified city.

    Args:
        city_name: City name to display on the map
        dep_code: Department code (optional)

    Returns:
        HTML response with the map template
    """
    logger.info("Showing city map", city_name=city_name, dep_code=dep_code)

    try:
        if not dep_code:
            return JSONResponse(
                {"error": "Department code is required to generate the map"},
                status_code=400,
            )

        # Convert dep_code to integer
        try:
            dep_code_int = int(dep_code)
        except ValueError:
            return JSONResponse(
                {"error": "Department code must be a valid integer"},
                status_code=400,
            )

        # Generate the map using the generate_map function
        folium_map = generate_map(city_name, dep_code_int)

        # Get the HTML content from the Folium map
        map_html = folium_map._repr_html_()
        map_html = map_html.replace(
            '<div class="folium-map"', '<div id="map" class="folium-map"'
        )

        # Get the center coordinates for fallback display
        center_lat = folium_map.location[0] if folium_map.location else 46.2276
        center_lon = folium_map.location[1] if folium_map.location else 2.2137

        return templates.TemplateResponse(
            "map.html",
            {
                "request": request,
                "city_name": city_name,
                "dep_code": dep_code,
                "latitude": center_lat,
                "longitude": center_lon,
                "map_html": map_html,
            },
        )

    except Exception as e:
        logger.error("Error in show_city_map endpoint", error=str(e))
        return JSONResponse(
            {"error": f"An error occurred while showing the city map: {str(e)}"},
            status_code=500,
        )


@app.get("/plot_city")
async def plot_city(city: str, dep_code: str = None):
    """
    Redirect to the map page for the specified city.

    Args:
        city: City name to plot on the map
        dep_code: Department code (optional)

    Returns:
        Redirect response to the map page
    """
    logger.info("Plotting city", city=city, dep_code=dep_code)

    url = f"/map/{city}"
    if dep_code:
        url += f"?dep_code={dep_code}"

    return RedirectResponse(url=url, status_code=302)
