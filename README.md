# **FastAPI RFP Processing API**  

## 📌 **Project Overview**
This FastAPI-based API fetches Request for Proposal (RFP) data from the Socrata Open Data API, processes it, and generates structured outputs.

---

## 🚀 **Getting Started**
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/calderondl/cwssg-fastapi-rfp-project.git
cd cwssg-fastapi-rfp-project
```

### 2️⃣ **Set Up a Virtual Environment**
```bash
python -m venv venv
venv\Scripts\activate # On Windows
```

### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Run the FastAPI Server**
```bash
uvicorn app.main:app --reload
```

---

## 📊 **API Endpoints**
### 🔹 **Home Route**
```http
GET /
```
✅ Returns a welcome message.

### 🔹 **Generate & Process Data**
```http
GET /generate_data
```
✅ Fetches, cleans, and processes data.  
✅ Saves results as CSV files.  
✅ Returns the process summary.

---

## 🛠 **Project Structure**
```
📦 cwssg-fastapi-rfp-project
   📂 app
     📜 main.py           # FastAPI app entry point
     📜 data_fetcher.py   # Fetch data from API
     📜 data_processor.py # Process and clean data
     📜 routes.py         # API route definitions     
   📂 output              # Processed CSV files (auto-generated)
   📜 requirements.txt    # Python dependencies
   📜 README.md           # Documentation
```

---

## 📂 **Generated CSV Files**
The API saves the processed data into the `output/` directory:
- 📄 `rfp_data.csv` → **Main RFP Table**
- 📄 `billed_entities.csv` → **Billed Entities**
- 📄 `contacts.csv` → **Contacts**
- 📄 `services.csv` → **Services**
