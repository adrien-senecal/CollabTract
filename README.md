# CollabTract v1.1.0

**Smart Door-to-Door and Flyering Route Planner**

CollabTract is a web application designed to help optimize door-to-door distribution routes and flyering campaigns. Version 1.1 provides advanced city search functionality, interactive mapping capabilities, and intelligent clustering for route optimization in French cities and addresses.

## 🚀 Features

### Core Functionality

- **City Search**: Search for French cities by name or postal code
- **Interactive Maps**: Generate detailed maps with address markers for selected cities
- **Address Visualization**: Display all addresses within a city with precise location markers
- **Route Clustering**: Intelligent K-means clustering for optimal route planning
- **Color-coded Routes**: Automatic generation of distinct colors for different routes
- **Fuzzy Search**: Intelligent city name matching with similarity scoring
- **Department Support**: Full support for all French departments including overseas territories

### Technical Features

- **FastAPI Backend**: Modern, fast web framework with automatic API documentation
- **Machine Learning**: Scikit-learn integration for K-means clustering algorithms
- **Interactive Web Interface**: Bootstrap-based responsive UI
- **Real-time Data**: Automatic download of latest address data from official French sources
- **Caching**: Local storage of downloaded data for improved performance
- **Error Handling**: Comprehensive error handling and logging
- **Color Generation**: HSV-based distinct color generation for route visualization

## 🏗️ Architecture

### Project Structure

```
CollabTract/
├── src/
│   ├── app.py                 # FastAPI application and routes
│   ├── settings.py            # Configuration settings
│   ├── requirements.txt       # Production dependencies
│   ├── requirements-dev.txt   # Development dependencies
│   └── tools/
│       ├── __init__.py       # Package initialization
│       ├── get_city.py       # City search functionality
│       ├── map.py            # Map generation with Folium and clustering
│       ├── csv_loading.py    # Address data loading
│       ├── validation.py     # Input validation utilities
│       └── color_code.py     # Color generation for route visualization
├── data/
│   └── csv/                  # Local data storage
│       ├── communes-france-2025.csv.gz
│       └── adresses-*.csv.gz
└── README.md
```

### API Endpoints

#### `GET /get_city`

- **Description**: Search for cities by name or postal code
- **Parameters**:
  - `city` (optional): City name to search for
  - `postal_code` (optional): Postal code to search for
- **Response**: JSON with matching cities and department codes

#### `POST /map`

- **Description**: Generate interactive map with clustering for route optimization
- **Request Body**: MapRequest object with the following fields:
  - `city_name` (string): Name of the city to map
  - `dep_code` (int|string): Department code
  - `cluster_nbr` (int, optional): Number of clusters for route optimization (default: 1)
  - `clustering_method` (string, optional): Clustering algorithm (default: "kmeans")
  - `cluster_colors` (list[string], optional): Custom hex colors for clusters
- **Response**: HTML content of the interactive map with clustered addresses

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd CollabTract
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r src/requirements.txt
   ```

   **Key Dependencies:**

   - `fastapi`: Modern web framework for building APIs
   - `uvicorn`: ASGI server for running FastAPI applications
   - `folium`: Interactive map generation
   - `scikit-learn`: Machine learning library for clustering algorithms
   - `pandas`: Data manipulation and analysis
   - `structlog`: Structured logging
   - `thefuzz`: Fuzzy string matching for city search

4. **Run the application**

   ```bash
   uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`
   - API documentation available at `http://localhost:8000/docs`

## 📊 Data Sources

### French Address Database (Base Adresse Locale)

- **Source**: [adresse.data.gouv.fr](https://adresse.data.gouv.fr)
- **Format**: CSV files compressed with gzip
- **Coverage**: All French departments and overseas territories
- **Update Frequency**: Automatic download of latest data

### French Municipalities Database

- **Source**: Official French municipalities data
- **Format**: CSV with postal codes and department codes
- **Coverage**: All French municipalities

## 🔧 Configuration

### Environment Variables

The application uses the following configuration (defined in `src/settings.py`):

- `CSV_FOLDER`: Path to local data storage (default: `./data/csv`)
- `COMMUNES_FRANCE_FILENAME`: Name of the municipalities file

### Data Management

- Address data is automatically downloaded when first requested
- Data is cached locally for improved performance
- Supports all French departments including overseas territories (971-989, 2A, 2B)

## 🎯 Usage

### Basic Workflow

1. **Search for a City**

   ```bash
   curl "http://localhost:8000/get_city?city=Paris"
   ```

2. **Generate a Map with Clustering**

   ```bash
   curl -X POST "http://localhost:8000/map" \
        -H "Content-Type: application/json" \
        -d '{
          "city_name": "Paris",
          "dep_code": 75,
          "cluster_nbr": 5,
          "clustering_method": "kmeans"
        }'
   ```

3. **Custom Route Colors**

   ```bash
   curl -X POST "http://localhost:8000/map" \
        -H "Content-Type: application/json" \
        -d '{
          "city_name": "Lyon",
          "dep_code": 69,
          "cluster_nbr": 3,
          "cluster_colors": ["#ff0000", "#00ff00", "#0000ff"]
        }'
   ```

### Advanced Features

- **Route Clustering**: Automatically groups addresses into optimal delivery routes using K-means clustering
- **Color Generation**: Automatic generation of distinct colors for different routes using HSV color space
- **Fuzzy Search**: Intelligent matching to find cities even with slight spelling variations
- **Department Validation**: Automatic validation of department codes
- **Error Handling**: Comprehensive error messages for invalid inputs

## 🧪 Development

### Development Dependencies

```bash
pip install -r src/requirements-dev.txt
```

### Code Quality

- **Logging**: Structured logging with `structlog`
- **Type Hints**: Full type annotation support
- **Error Handling**: Comprehensive exception handling
- **Validation**: Input validation for all user inputs

### Testing

The application includes comprehensive testing and validation:

- **Jupyter Notebook**: `src/test.ipynb` for interactive development and API testing
- **Validation Functions**: Department code validation, file path validation
- **City Search Testing**: Fuzzy matching algorithms and postal code lookup
- **Map Generation Testing**: Clustering algorithms and color generation
- **API Testing**: Endpoint validation and error handling

## 📝 API Documentation

When running the application, interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔮 Future Versions

Version 1.1 includes route clustering and optimization. Planned features for future versions include:

- Advanced route optimization algorithms (TSP, genetic algorithms)
- Multi-city campaign planning
- Export functionality for GPS devices
- Team coordination features
- Performance analytics and route efficiency metrics
- Real-time traffic integration
- Delivery time estimation

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🤝 Contributing

Contributions are welcome! Please ensure:

- Code follows Python best practices
- Type hints are included
- Error handling is comprehensive
- Documentation is updated

## 📞 Support

For issues, questions, or contributions, please refer to the project repository or contact the development team.
