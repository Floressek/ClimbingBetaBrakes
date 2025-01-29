# Climbing Route Creator

## Overview
Climbing Route Creator is a mobile application that helps climbers create, share, and discover climbing routes. Using advanced computer vision technology (Roboflow API), the app automatically detects holds on climbing wall photos and allows users to create routes by selecting holds and adding descriptions. Think of it as a collaborative platform for climbers to share their favorite routes and discover new challenges.

## Key Features and project structure
```mermaid
sequenceDiagram
    actor User
    participant App as ClimbingApp
    participant SW as StartupWindow
    participant LW as LoadingWindow
    participant DW as DetectionWorker
    participant MW as MainWindow
    participant RID as RouteInfoDialog
    participant HV as HoldViewer
    participant RR as RouteRepository
    participant RIP as RouteImageProcessor
    participant RC as RoboflowClient
    participant API as Roboflow API
    participant Hold as Hold Objects

    User->>App: Start Application
    activate App
    
    App->>App: Initialize QApplication
    App->>App: Initialize ProjectConfig
    App->>RC: Initialize RoboflowClient
    activate RC
    
    # Główna różnica - MainWindow jest tworzone przed StartupWindow
    App->>MW: Create MainWindow (hidden)
    activate MW
    MW->>HV: Create HoldViewer
    activate HV
    MW->>RR: Initialize RouteRepository
    activate RR
    
    App->>SW: Create StartupWindow
    activate SW
    App->>LW: Create LoadingWindow
    activate LW
    
    User->>SW: Upload Image
    SW->>SW: Validate & Copy Image
    SW->>App: image_uploaded Signal
    
    App->>SW: Hide
    App->>LW: Show & Start Animation
    App->>MW: Set Current Image Path
    MW->>HV: Load Image
    
    App->>DW: Create & Start Detection
    activate DW
    
    DW->>RC: Detect Holds
    RC->>API: API Request
    API-->>RC: Response with Detections
    
    # Hold objects są tworzone w DetectionWorker
    loop For each detection
        DW->>Hold: Create Hold Object
    end
    
    DW-->>App: detection_completed Signal
    DW-->>App: holds List
    deactivate DW
    
    App->>HV: Set Holds
    App->>LW: Hide
    App->>MW: Show
    
    User->>HV: Click on Hold
    HV->>HV: Check Click Location
    HV->>HV: Update Hold Selection State
    HV->>HV: Update View
    
    User->>MW: Click "Save Route"
    MW->>RID: Show Dialog
    activate RID
    User->>RID: Enter Route Info
    RID-->>MW: Route Info
    deactivate RID
    
    MW->>MW: Generate UUIDs for Holds
    MW->>RR: Save Route Model
    RR->>RR: Create JSON
    
    MW->>RIP: Add Info Overlay
    activate RIP
    RIP->>RIP: Process & Save Image
    RIP-->>MW: Saved Image Path
    deactivate RIP
    
    MW-->>User: Success Message / Error message
    
    deactivate RR
    deactivate HV
    deactivate MW
    deactivate LW
    deactivate SW
    deactivate RC
    deactivate App
```
### Project Structure
```
climbing_route_creator/              # Główny katalog projektu
│
├── src/                            # Kod źródłowy aplikacji
│   ├── __init__.py
│   ├── main.py                    # Punkt startowy aplikacji
│   │
│   ├── api/                       # Moduł komunikacji z Roboflow
│   │   ├── __init__.py
│   │   ├── models.py             # Klasy reprezentujące dane z API
│   │   └── roboflow_client.py    # Klient API Roboflow
│   │
│   ├── core/                      # Logika biznesowa aplikacji
│   │   ├── __init__.py
│   │   ├── hold.py              # Reprezentacja chwytu w aplikacji
│   │   ├── connection.py        # Reprezentacja połączeń między chwytami
│   │   └── movement_type.py     # Typy ruchów (hands/feet)
│   │
│   ├── gui/                       # Interfejs użytkownika
│   │   ├── __init__.py
│   │   ├── main_window.py       # Główne okno aplikacji
│   │   ├── resources/           # Zasoby GUI (ikony, style)
│   │   │   ├── icons/
│   │   │   ├── styles/
│   │   │   └── loading.gif
│   │   ├── workers/            # Wątki robocze
│   │   │   ├── __init__.py
│   │   │   └── detection_worker.py  # Wątek do detekcji chwytów
│   │   └── widgets/             # Komponenty GUI
│   │       ├── __init__.py
│   │       ├── hold_viewer.py   # Widget do wyświetlania chwytów
│   │       ├── route_toolbar.py # Pasek narzędzi trasy
│   │       ├── route_info_dialog.py # Dialog informacji o trasie
│   │       ├── loading_window.py    # Okno ładowania
│   │       └── startup_window.py    # Okno startowe
│   │
│   ├── utils/                     # Narzędzia pomocnicze
│   │   ├── __init__.py
│   │   ├── config.py           # Konfiguracja aplikacji
│   │   ├── logger.py           # Konfiguracja logowania
│   │   └── route_image_processor.py # Przetwarzanie obrazów tras
│   │
│   └── storage/                   # Warstwa przechowywania danych
│       ├── __init__.py
│       ├── models/              # Modele danych
│       │   ├── __init__.py
│       │   └── route_model.py  # Model trasy do zapisu
│       └── repositories/        # Implementacje zapisu
│           ├── __init__.py
│           └── route_repository.py # Repozytorium tras
│
├── data/                          # Dane aplikacji
│   ├── routes/                   # Zapisane trasy (JSON)
│   ├── images/                   # Obrazy ścian
│   └── exports/                  # Wygenerowane obrazy z trasami
│
├── logs/                          # Logi aplikacji
│
├── setup.py                       # Skrypt instalacyjny
├── pyproject.toml                # Konfiguracja narzędzi
├── README.md                     # Dokumentacja projektu
└── .gitignore
```

The application allows users to:
- Automatically detect climbing holds in photos using computer vision
- Create routes by selecting holds and adding descriptions
- Add connection lines (Bézier curves) between holds to represent climbing movements
- Share routes with other climbers
- Browse and discover routes created by the climbing community

## Technical Requirements
- Python 3.12 or higher
- PyQt5 for the user interface
- Roboflow API key for hold detection
- System operacyjny: Windows 10/11, Linux (Ubuntu 20.04+), macOS (10.15+)
- Additional dependencies listed in pyproject.toml

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/climbing-route-creator.git
cd climbing-route-creator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install poetry
poetry install
poetry update
```

4. Set up your Roboflow API key:
Create a `.env` file in the project root and add your API key:
```env
ROBOFLOW_API_KEY=your_api_key_here
```

## Getting Started

1. Run the application:
```bash
python src/main.py
```
```mermaid
sequenceDiagram
    participant U as User
    participant SW as StartupWindow
    participant DW as DetectionWorker
    participant RC as RoboflowClient
    participant H as HoldViewer

    U->>SW: Przesyła zdjęcie
    SW->>DW: Inicjuje detekcję
    activate DW
    DW->>RC: Wysyła zapytanie do API
    RC-->>DW: Zwraca wykryte chwyty
    DW->>H: Tworzy obiekty Hold
    deactivate DW
    H-->>U: Wyświetla chwyty

    Note over U,H: Użytkownik może teraz<br/>zaznaczać chwyty
```
2. To create a new route:
   - Click "New Route" and select a photo of a climbing wall
   - Wait for automatic hold detection
   - Click on holds to create your route
   - Add descriptions and difficulty rating
   - Save and share your route
```mermaid
stateDiagram-v2
    [*] --> StartupWindow
    StartupWindow --> LoadingWindow: Upload Image
    LoadingWindow --> MainWindow: Detection Complete
    
    state MainWindow {
        [*] --> RouteEditing
        RouteEditing --> HandSelection
        RouteEditing --> FootSelection
        HandSelection --> ConnectionEditing
        FootSelection --> ConnectionEditing
        ConnectionEditing --> SaveRoute
        SaveRoute --> RouteInfoDialog
        RouteInfoDialog --> SaveComplete
        SaveComplete --> [*]
    }
    
    MainWindow --> [*]: Close Application
```
## Project Structure
The project follows a modular architecture for maintainability and testability:
- `src/api/`: Roboflow API integration
- `src/core/`: Core business logic
- `src/gui/`: User interface components
- `src/storage/`: Data persistence layer
- `src/utils/`: Utility functions and configuration

## Development

For development, install additional dependencies:
```bash
pip install poetry
poetry install
poetry update
```

Run tests:
```bash
pytest
```

## Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create a new branch for your feature
3. Write tests for your changes
4. Submit a pull request

Please ensure your code follows our style guidelines and includes appropriate tests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Roboflow for providing the hold detection API
- The climbing community for inspiration and feedback
- All contributors who have helped improve this project

## Contact
For questions or suggestions, please open an issue in the GitHub repository or contact the maintainers.

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![Python Version](https://img.shields.io/badge/PyQt5-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/badge/build-passing-success)

