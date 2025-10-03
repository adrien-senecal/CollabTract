# CollabTract v1.0

**Smart Door-to-Door and Flyering Route Planner**

CollabTract is a web application designed to help optimize door-to-door distribution routes and flyering campaigns. Version 1.0 provides city search functionality and interactive mapping capabilities for French cities and addresses.

## 🚀 Features

### Core Functionality

- **City Search**: Search for French cities by name or postal code
- **Interactive Maps**: Generate detailed maps with address markers for selected cities
- **Address Visualization**: Display all addresses within a city with precise location markers
- **Fuzzy Search**: Intelligent city name matching with similarity scoring
- **Department Support**: Full support for all French departments including overseas territories

### Technical Features

- **FastAPI Backend**: Modern, fast web framework with automatic API documentation
- **Interactive Web Interface**: Bootstrap-based responsive UI
- **Real-time Data**: Automatic download of latest address data from official French sources
- **Caching**: Local storage of downloaded data for improved performance
- **Error Handling**: Comprehensive error handling and logging

## 🏗️ Architecture

### Project Structure

```
CollabTract/
├── src/
│   ├── app.py                 # FastAPI application and routes
│   ├── settings.py            # Configuration settings
│   ├── requirements.txt       # Production dependencies
│   ├── requirements-dev.txt   # Development dependencies
│   ├── templates/
│   │   ├── index.html        # Main search interface
│   │   └── map.html          # Map display template
│   └── tools/
│       ├── __init__.py       # Package initialization
│       ├── get_city.py       # City search functionality
│       ├── map.py            # Map generation with Folium
│       ├── csv_loading.py    # Address data loading
│       └── validation.py     # Input validation utilities
├── data/
│   └── csv/                  # Local data storage
│       ├── communes-france-2025.csv.gz
│       └── adresses-*.csv.gz
└── README.md
```

### API Endpoints

#### `GET /`

- **Description**: Main application interface
- **Response**: HTML page with city search form

#### `GET /get_city`

- **Description**: Search for cities by name or postal code
- **Parameters**:
  - `city` (optional): City name to search for
  - `postal_code` (optional): Postal code to search for
- **Response**: JSON with matching cities and department codes

#### `GET /map/{city_name}`

- **Description**: Display interactive map for a specific city
- **Parameters**:
  - `city_name`: Name of the city to map
  - `dep_code` (query param): Department code (required)
- **Response**: HTML page with interactive map

#### `GET /plot_city`

- **Description**: Redirect to map page for a city
- **Parameters**:
  - `city`: City name
  - `dep_code` (optional): Department code
- **Response**: Redirect to map page

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

   - Enter a city name or postal code in the search form
   - The system will return matching cities with department codes

2. **Select a City**

   - Choose from the search results
   - Click "Sélectionner" to view the map

3. **View the Map**
   - Interactive map displays all addresses in the selected city
   - Each marker shows the complete address
   - Zoom and pan to explore the area

### Advanced Features

- **Fuzzy Search**: The system uses intelligent matching to find cities even with slight spelling variations
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

The application includes validation functions and error handling for:

- Department code validation
- File path validation
- City name fuzzy matching
- Address data loading

## 📝 API Documentation

When running the application, interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔮 Future Versions

Version 1.0 focuses on city search and mapping. Planned features for future versions include:

- Route optimization algorithms
- Multi-city campaign planning
- Export functionality for GPS devices
- Team coordination features
- Performance analytics

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
