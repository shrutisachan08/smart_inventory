# SmartInventory – Intelligent Retail Management System

SmartInventory is a modular AI-powered retail automation system designed to optimize inventory management, staff assignment, and eco-friendly operations for modern retail chains like Walmart. Built with a Flask backend and React frontend, it integrates intelligent features like expiry monitoring, predictive restocking, geolocation-based staff tasking, and inter-store inventory balancing.

---

## Features

| #️⃣ | Feature                              | Status     | Summary                                                                 |
|-----|--------------------------------------|------------|-------------------------------------------------------------------------|
| 1️⃣ | Shelf Life & Expiry Monitoring    | ✅ Built    | Parses product data to flag items nearing expiry using threshold logic. |
| 2️⃣ | Predictive Restocking with AI     | ✅ Built    | Forecasts product demand and recommends reorder quantities using ML.    |
| 3️⃣ | Eco-Friendly Staff Tasks          | ✅ Built    | Tags sustainable items and assigns tasks to eco-rated nearby staff.     |
| 4️⃣ | Voice Assistant for Inventory     | 🔜 Planned  | Voice-based assistant for hands-free queries and commands.              |
| 5️⃣ | Inventory Redistribution          | ✅ Built    | Suggests stock transfers between stores based on real-time availability.|
| 6️⃣ | Smart Staff Routing                | ✅ Built    | Assigns restocking tasks to nearest idle staff using GPS logic.         |
| 7️⃣ | Loyalty System Integration         | 🔜 Planned  | Suggests stock based on purchase habits; loyalty-driven alerts.         |
| 8️⃣ | Offline Mode (Edge Computing)     | 🔜 Planned  | Edge hardware fallback to maintain ops during internet downtime.        |

---

## Tech Stack

###  Backend
- **Flask** — REST APIs to handle ML predictions, expiry alerts, and staff assignments
- **MongoDB** — Stores inventory, staff, and task records
- **Pandas, scikit-learn** — Data wrangling + ML for restocking prediction
- **Haversine formula** — Location-based staff assignment
- **CSV Parsing, datetime** — For expiry tracking

### Frontend
- **React.js + Vite**
- **Tailwind CSS** — Custom dashboards and clean UI
- **Axios** — API interaction
- **ShadCN UI, Lucide Icons** — Component styling

---

## Folder Structure
    smart_inventory/
    ├── backend/
    │   ├── app.py
    │   ├── db/                       # MongoDB connection
    │   ├── logic/                    # Expiry monitoring
    │   ├── models/                   # ML models and training
    │   ├── po_generator/             # Purchase order generation
    │   ├── routes/                   # API endpoints
    │   ├── service/                  # Core feature logic
    │   └── utils/                    # Helper utilities
    │
    ├── data/                         # Sample inventory & staff CSVs
    │
    ├── frontend/
    │   ├── public/
    │   └── src/
    │       ├── components/           # React feature components
    │       └── pages/                # Home & Dashboard pages
    │
    └── po_generator/
        └── output/                  # Generated POs (CSV + JSON)


## Architecture
```css
           [React Frontend] ↔ [Flask API]
                  ↓             ↑
        [MongoDB] ←→ [ML Model + Geospatial Logic]
```

## Getting Started

### Backend
```bash
    cd backend
    pip install -r requirements.txt
    python app.py 
```

### Frontend
```bash
    cd frontend
    npm install
    npm run dev
```

## Future Work
- Add voice command module with SpeechRecognition
- Loyalty-aware stock suggestions

## Contributors
- [Neha Singh](https://github.com/Nehayp21242929)
- [Shruti Sachan](https://github.com/shrutisachan08)
- [Akshita Mishra](https://github.com/akshitamishra13)
- [Ritika Singh](https://github.com/ritika1588)
