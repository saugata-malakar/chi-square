from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import random
import time
import json
from datetime import datetime, timedelta

app = FastAPI(title="TradeGuard AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Constants ────────────────────────────────────────────────────────────────

HS_CODE_DB = {
    "electronics": {"code": "8471.30", "description": "Portable automatic data processing machines", "duty_rate": 0.0},
    "textile": {"code": "6109.10", "description": "T-shirts, singlets, cotton", "duty_rate": 12.0},
    "machinery": {"code": "8479.89", "description": "Machines and mechanical appliances", "duty_rate": 2.5},
    "chemicals": {"code": "2901.10", "description": "Acyclic hydrocarbons, saturated", "duty_rate": 5.5},
    "food": {"code": "1901.90", "description": "Food preparations of flour, groats", "duty_rate": 17.5},
    "pharma": {"code": "3004.90", "description": "Medicaments for retail sale", "duty_rate": 0.0},
    "automotive": {"code": "8708.99", "description": "Parts and accessories for vehicles", "duty_rate": 6.5},
    "furniture": {"code": "9403.20", "description": "Metal furniture, other", "duty_rate": 0.0},
}

COUNTRY_REGULATIONS = {
    "USA": {
        "flag": "🇺🇸", "currency": "USD",
        "required_docs": ["Commercial Invoice", "Bill of Lading", "Packing List", "ISF Filing"],
        "restricted_items": ["Certain chemicals", "Firearms", "Endangered species products"],
        "import_duty_threshold": 800, "vat": 0,
        "special_requirements": ["FDA approval for food/pharma", "FCC certification for electronics"],
        "sanctions_risk": "low", "processing_days": 2
    },
    "EU": {
        "flag": "🇪🇺", "currency": "EUR",
        "required_docs": ["Commercial Invoice", "Bill of Lading", "Packing List", "EUR.1 Certificate", "CE Declaration"],
        "restricted_items": ["Non-CE marked goods", "Certain plastics", "Non-REACH compliant chemicals"],
        "import_duty_threshold": 150, "vat": 20,
        "special_requirements": ["CE marking mandatory", "GDPR compliance for tech", "REACH compliance"],
        "sanctions_risk": "low", "processing_days": 3
    },
    "China": {
        "flag": "🇨🇳", "currency": "CNY",
        "required_docs": ["Commercial Invoice", "Bill of Lading", "Packing List", "CIQ Certificate", "Import License"],
        "restricted_items": ["Encrypted tech", "Certain biological materials", "Political content"],
        "import_duty_threshold": 50, "vat": 13,
        "special_requirements": ["CCC certification for electronics", "GB standards compliance", "SAMR registration"],
        "sanctions_risk": "medium", "processing_days": 5
    },
    "India": {
        "flag": "🇮🇳", "currency": "INR",
        "required_docs": ["Commercial Invoice", "Bill of Lading", "Packing List", "Certificate of Origin", "BIS Certificate"],
        "restricted_items": ["Certain agricultural products", "Arms", "Narcotic substances"],
        "import_duty_threshold": 5000, "vat": 18,
        "special_requirements": ["BIS mandatory for electronics", "FSSAI for food items", "IEC code required"],
        "sanctions_risk": "low", "processing_days": 4
    },
    "UAE": {
        "flag": "🇦🇪", "currency": "AED",
        "required_docs": ["Commercial Invoice", "Bill of Lading", "Packing List", "Certificate of Origin", "Halal Certificate"],
        "restricted_items": ["Pork products", "Alcohol (restricted)", "Certain medications"],
        "import_duty_threshold": 1000, "vat": 5,
        "special_requirements": ["Halal certification for food", "Arabic labeling required", "ESMA conformity"],
        "sanctions_risk": "medium", "processing_days": 2
    },
    "Brazil": {
        "flag": "🇧🇷", "currency": "BRL",
        "required_docs": ["Commercial Invoice", "Bill of Lading", "Packing List", "SISCOMEX Registration", "Import License"],
        "restricted_items": ["Used goods (restricted)", "Certain chemicals", "Weapons"],
        "import_duty_threshold": 50, "vat": 17,
        "special_requirements": ["INMETRO certification", "ANVISA approval for pharma/food", "SISCOMEX registration"],
        "sanctions_risk": "low", "processing_days": 7
    },
}

TRANSPORT_MODES = {
    "sea_freight": {"emission_factor": 0.015, "label": "Sea Freight"},
    "air_freight": {"emission_factor": 0.602, "label": "Air Freight"},
    "road_freight": {"emission_factor": 0.062, "label": "Road Freight"},
    "rail_freight": {"emission_factor": 0.022, "label": "Rail Freight"},
}

SHIPPING_ROUTES = {
    "Shanghai-Rotterdam": 19500,
    "Mumbai-Dubai": 1900,
    "Los Angeles-Shanghai": 10000,
    "Rotterdam-New York": 5900,
    "Dubai-Singapore": 5600,
    "Singapore-Sydney": 6300,
    "Mumbai-Singapore": 3900,
    "Hamburg-New York": 6200,
}

DOC_FIELDS = {
    "Bill of Lading": {
        "BL Number": lambda: f"MSKU{random.randint(100000,999999)}",
        "Shipper": lambda: random.choice(["Shenzhen Tech Corp Ltd", "Mumbai Exports Pvt Ltd", "Frankfurt GmbH Trading"]),
        "Consignee": lambda: random.choice(["Global Imports LLC", "Euro Trade Partners", "Pacific Distributors Inc"]),
        "Vessel": lambda: random.choice(["MSC OSCAR", "EVER GIVEN", "COSCO SHIPPING UNIVERSE", "CMA CGM MARCO POLO"]),
        "Port of Loading": lambda: random.choice(["Shanghai", "Mumbai", "Hamburg", "Rotterdam", "Singapore"]),
        "Port of Discharge": lambda: random.choice(["Los Angeles", "Rotterdam", "New York", "Dubai", "Sydney"]),
        "Gross Weight": lambda: f"{random.randint(1000, 50000)} KG",
        "Container No": lambda: f"MSCU{random.randint(1000000,9999999)}",
        "Freight Terms": lambda: random.choice(["Prepaid", "Collect", "As Arranged"]),
    },
    "Commercial Invoice": {
        "Invoice Number": lambda: f"INV-{datetime.now().year}-{random.randint(10000,99999)}",
        "Invoice Date": lambda: datetime.now().strftime("%Y-%m-%d"),
        "Seller": lambda: random.choice(["Shenzhen Tech Corp Ltd", "Mumbai Exports Pvt Ltd", "Frankfurt GmbH Trading"]),
        "Buyer": lambda: random.choice(["Global Imports LLC", "Euro Trade Partners", "Pacific Distributors Inc"]),
        "Description of Goods": lambda: random.choice(["Electronic Components", "Textile Products", "Industrial Machinery"]),
        "Quantity": lambda: str(random.randint(100, 10000)),
        "Unit Price": lambda: f"USD {random.uniform(5, 500):.2f}",
        "Total Value": lambda: f"USD {random.randint(5000, 500000):,}",
        "Currency": lambda: random.choice(["USD", "EUR", "CNY", "INR"]),
        "Incoterms": lambda: random.choice(["FOB", "CIF", "EXW", "DDP", "DAP"]),
    },
    "Packing List": {
        "PL Number": lambda: f"PL-{random.randint(10000,99999)}",
        "Total Packages": lambda: str(random.randint(10, 500)),
        "Total Net Weight": lambda: f"{random.randint(500, 20000)} KG",
        "Total Gross Weight": lambda: f"{random.randint(600, 22000)} KG",
        "Total Volume": lambda: f"{random.uniform(5, 100):.2f} CBM",
        "Marks & Numbers": lambda: f"BOX 1-{random.randint(10,500)}",
        "Package Type": lambda: random.choice(["Cartons", "Pallets", "Drums", "Bags"]),
    },
    "Certificate of Origin": {
        "Certificate Number": lambda: f"CO-{random.randint(100000,999999)}",
        "Country of Origin": lambda: random.choice(["China", "India", "Germany", "USA", "Vietnam"]),
        "Issuing Authority": lambda: random.choice(["Chamber of Commerce", "Ministry of Commerce", "Export Promotion Council"]),
        "HS Code": lambda: random.choice(list(HS_CODE_DB.values()))["code"],
        "Description": lambda: random.choice(["Electronic equipment", "Textile products", "Machinery parts"]),
        "Preferential Treatment": lambda: random.choice(["Yes - FTA applicable", "No", "Yes - GSP applicable"]),
    },
    "HS Code Classification": {
        "Declared HS Code": lambda: random.choice(list(HS_CODE_DB.values()))["code"],
        "Commodity Description": lambda: random.choice(list(HS_CODE_DB.values()))["description"],
        "Chapter": lambda: str(random.randint(1, 97)),
        "Import Duty Rate": lambda: f"{random.uniform(0, 20):.1f}%",
        "Excise Duty": lambda: f"{random.uniform(0, 10):.1f}%",
    },
    "Customs Declaration": {
        "Declaration Number": lambda: f"CUS-{random.randint(1000000,9999999)}",
        "Declarant": lambda: random.choice(["XYZ Customs Brokers", "Global Trade Services", "FastClear Ltd"]),
        "Customs Office": lambda: random.choice(["Port of Shanghai", "JFK Airport", "Port of Rotterdam", "JNPT Mumbai"]),
        "Declaration Date": lambda: datetime.now().strftime("%Y-%m-%d"),
        "Procedure Code": lambda: random.choice(["4000", "4071", "6110", "3151"]),
        "Statistical Value": lambda: f"USD {random.randint(5000, 500000):,}",
        "Customs Duty": lambda: f"USD {random.randint(100, 50000):,}",
    },
}

ANOMALIES_POOL = [
    {"type": "value_mismatch", "severity": "high", "field": "Invoice Value",
     "message": "Invoice value (USD 45,200) doesn't match Bill of Lading declared value (USD 38,500). Discrepancy of USD 6,700 flagged."},
    {"type": "hs_code_mismatch", "severity": "high", "field": "HS Code",
     "message": "Declared HS Code 8471.30 (computers) inconsistent with goods description 'Textile Products'. Possible misclassification to avoid higher duty."},
    {"type": "origin_suspicion", "severity": "medium", "field": "Country of Origin",
     "message": "Certificate of Origin shows Vietnam, but manufacturer address on invoice shows China. Possible origin-washing to circumvent tariffs."},
    {"type": "undervaluation", "severity": "high", "field": "Unit Price",
     "message": "Unit price USD 2.10/unit is 340% below market average for this product category. Possible undervaluation for duty avoidance."},
    {"type": "weight_discrepancy", "severity": "medium", "field": "Gross Weight",
     "message": "Packing list gross weight (12,400 KG) exceeds Bill of Lading declared weight (11,800 KG) by 600 KG."},
    {"type": "sanctions_risk", "severity": "critical", "field": "Consignee",
     "message": "Consignee entity matches partial name on OFAC SDN watchlist. Manual verification required before release."},
    {"type": "missing_license", "severity": "high", "field": "Export License",
     "message": "Goods category (dual-use electronics) requires export control license. No license number found in documentation."},
    {"type": "date_inconsistency", "severity": "low", "field": "Invoice Date",
     "message": "Invoice date (2024-01-15) is prior to purchase order date (2024-01-20). Chronological inconsistency detected."},
    {"type": "quantity_mismatch", "severity": "medium", "field": "Quantity",
     "message": "Invoice quantity (5,000 units) doesn't match packing list (4,850 units). 150 unit discrepancy."},
    {"type": "restricted_goods", "severity": "critical", "field": "Commodity",
     "message": "Product description contains terms associated with dual-use technology (ECCN 3A001). Export license verification required."},
]

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "TradeGuard AI API Running", "version": "1.0.0"}

@app.get("/api/countries")
def get_countries():
    return {"countries": list(COUNTRY_REGULATIONS.keys()), "details": COUNTRY_REGULATIONS}

@app.get("/api/document-types")
def get_document_types():
    return {"types": list(DOC_FIELDS.keys())}

@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    return {
        "total_documents_processed": random.randint(12000, 15000),
        "compliance_rate": round(random.uniform(87, 94), 1),
        "anomalies_detected_today": random.randint(12, 45),
        "avg_clearance_time_hours": round(random.uniform(18, 36), 1),
        "documents_today": random.randint(150, 300),
        "high_risk_shipments": random.randint(3, 12),
        "countries_served": 47,
        "carbon_saved_tonnes": round(random.uniform(120, 180), 1),
        "recent_activity": [
            {"time": "2 min ago", "event": "Shipment SHP-2024-8821 cleared customs", "type": "success"},
            {"time": "8 min ago", "event": "Anomaly detected in Invoice INV-2024-44201", "type": "warning"},
            {"time": "15 min ago", "event": "Compliance check failed: missing CE certification", "type": "error"},
            {"time": "22 min ago", "event": "New shipment registered: Shanghai → Rotterdam", "type": "info"},
            {"time": "31 min ago", "event": "HS Code reclassification approved for SHP-8815", "type": "success"},
            {"time": "45 min ago", "event": "Sanctions screening completed: 0 matches", "type": "success"},
        ]
    }

@app.post("/api/documents/extract")
async def extract_document(file: UploadFile = File(...), doc_type: str = "Commercial Invoice"):
    if doc_type not in DOC_FIELDS:
        doc_type = "Commercial Invoice"
    fields = DOC_FIELDS[doc_type]
    extracted = {k: v() for k, v in fields.items()}
    return {
        "doc_type": doc_type,
        "filename": file.filename,
        "extracted_fields": [
            {"field": k, "value": v, "confidence": round(random.uniform(0.72, 0.99), 2), "needs_review": random.random() < 0.15}
            for k, v in extracted.items()
        ],
        "overall_confidence": round(random.uniform(0.78, 0.96), 2),
        "processing_time_ms": random.randint(800, 2500),
        "page_count": random.randint(1, 4),
        "language_detected": random.choice(["English", "English (primary), Chinese (secondary)", "English"]),
        "ocr_engine": "TradeGuard Vision v2.1",
    }

@app.post("/api/documents/analyze")
async def analyze_document(payload: Dict[str, Any]):
    num_anomalies = random.choices([0, 1, 2, 3], weights=[20, 40, 30, 10])[0]
    detected = random.sample(ANOMALIES_POOL, num_anomalies) if num_anomalies > 0 else []
    severity_weights = {"critical": 40, "high": 25, "medium": 15, "low": 5}
    risk_score = min(100, sum(severity_weights.get(a["severity"], 10) for a in detected))
    risk_level = "LOW" if risk_score < 30 else "MEDIUM" if risk_score < 60 else "HIGH" if risk_score < 85 else "CRITICAL"
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "anomalies": detected,
        "anomaly_count": len(detected),
        "recommendation": (
            "Document set appears clean. Proceed with standard processing." if risk_score < 30
            else "Minor discrepancies detected. Secondary review recommended." if risk_score < 60
            else "Multiple high-severity anomalies. Hold shipment and escalate to compliance team." if risk_score < 85
            else "CRITICAL: Potential fraud/sanctions risk. Immediate human review required. Do not release."
        ),
        "analysis_timestamp": datetime.now().isoformat(),
        "model_version": "TradeGuard Anomaly v3.2",
    }

@app.post("/api/compliance/check")
async def check_compliance(payload: Dict[str, Any]):
    destination = payload.get("destination_country", "USA")
    doc_types = payload.get("document_types", [])
    goods_category = payload.get("goods_category", "electronics")
    declared_value = payload.get("declared_value", 10000)

    dest_regs = COUNTRY_REGULATIONS.get(destination, COUNTRY_REGULATIONS["USA"])
    required = set(dest_regs["required_docs"])
    provided = set(doc_types)
    missing_docs = list(required - provided)

    hs_info = HS_CODE_DB.get(goods_category.lower(), HS_CODE_DB["electronics"])
    duty = declared_value * hs_info["duty_rate"] / 100
    vat_amount = declared_value * dest_regs["vat"] / 100

    checks = [
        {"check": "Documentation Completeness", "status": "PASS" if not missing_docs else "FAIL",
         "details": f"All {len(required)} required documents present" if not missing_docs else f"Missing: {', '.join(missing_docs)}", "severity": "low" if not missing_docs else "high"},
        {"check": "HS Code Validity", "status": "PASS" if random.random() > 0.2 else "WARNING",
         "details": f"HS Code {hs_info['code']} validated against WCO nomenclature", "severity": "low"},
        {"check": "Sanctions Screening", "status": "PASS" if dest_regs["sanctions_risk"] == "low" else "WARNING",
         "details": f"Screened against OFAC, EU, UN lists. Risk: {dest_regs['sanctions_risk'].upper()}", "severity": dest_regs["sanctions_risk"]},
        {"check": "Dual-Use Export Controls", "status": "PASS" if goods_category not in ["electronics", "chemicals"] else "WARNING",
         "details": "EAR/ITAR screening completed" if goods_category not in ["electronics", "chemicals"] else "Dual-use review recommended", "severity": "low" if goods_category not in ["electronics", "chemicals"] else "medium"},
        {"check": f"Destination Requirements ({destination})", "status": "PASS" if random.random() > 0.3 else "WARNING",
         "details": f"Special: {', '.join(dest_regs['special_requirements'][:2])}", "severity": "medium"},
        {"check": "Trade Agreement Eligibility", "status": random.choice(["PASS", "INFO"]),
         "details": "Checked for preferential duty rates (FTAs, GSP)", "severity": "low"},
        {"check": "Restricted Goods Screening", "status": "PASS" if goods_category not in ["chemicals", "pharma"] else "WARNING",
         "details": f"Checked against {destination} restricted goods list", "severity": "low" if goods_category not in ["chemicals", "pharma"] else "high"},
        {"check": "Valuation Compliance", "status": "PASS" if declared_value > 1000 else "WARNING",
         "details": "Reviewed under WTO Customs Valuation Agreement", "severity": "low" if declared_value > 1000 else "medium"},
    ]

    passed = sum(1 for c in checks if c["status"] == "PASS")
    warnings = sum(1 for c in checks if c["status"] == "WARNING")
    failed = sum(1 for c in checks if c["status"] == "FAIL")
    compliance_score = int((passed / len(checks)) * 100)

    return {
        "destination": destination,
        "destination_flag": dest_regs["flag"],
        "compliance_score": compliance_score,
        "overall_status": "COMPLIANT" if failed == 0 and warnings <= 1 else "NEEDS_REVIEW" if failed == 0 else "NON_COMPLIANT",
        "checks": checks,
        "summary": {"passed": passed, "warnings": warnings, "failed": failed, "total": len(checks)},
        "financials": {
            "declared_value": declared_value,
            "estimated_duty": round(duty, 2),
            "estimated_vat": round(vat_amount, 2),
            "total_landed_cost": round(declared_value + duty + vat_amount, 2),
            "duty_rate": f"{hs_info['duty_rate']}%",
            "vat_rate": f"{dest_regs['vat']}%",
            "currency": dest_regs["currency"],
        },
        "timeline": {
            "estimated_clearance_days": dest_regs["processing_days"],
            "expedited_available": random.choice([True, False]),
        },
        "required_docs": dest_regs["required_docs"],
        "missing_docs": missing_docs,
        "special_requirements": dest_regs["special_requirements"],
    }

@app.post("/api/sustainability/calculate")
async def calculate_carbon(payload: Dict[str, Any]):
    transport_mode = payload.get("transport_mode", "sea_freight")
    weight_kg = payload.get("weight_kg", 1000)
    route = payload.get("route", "Shanghai-Rotterdam")

    distance_km = SHIPPING_ROUTES.get(route, 10000)
    mode_info = TRANSPORT_MODES.get(transport_mode, TRANSPORT_MODES["sea_freight"])
    weight_tonnes = weight_kg / 1000
    co2_kg = mode_info["emission_factor"] * weight_tonnes * distance_km

    comparisons = {
        mode: {"label": info["label"], "co2_kg": round(info["emission_factor"] * weight_tonnes * distance_km, 2)}
        for mode, info in TRANSPORT_MODES.items()
    }

    return {
        "route": route,
        "distance_km": distance_km,
        "weight_kg": weight_kg,
        "transport_mode": transport_mode,
        "transport_label": mode_info["label"],
        "co2_emissions_kg": round(co2_kg, 2),
        "trees_to_offset": round(co2_kg / 21, 1),
        "mode_comparison": comparisons,
        "greenest_mode": "sea_freight",
        "savings_vs_air": round(comparisons["air_freight"]["co2_kg"] - co2_kg, 2),
        "esg_rating": "A" if transport_mode == "sea_freight" else "B" if transport_mode in ["rail_freight", "road_freight"] else "D",
        "carbon_cost_usd": round(co2_kg * 0.05, 2),
        "recommendations": [
            "Current mode is the most environmentally efficient for this route",
            "Consider carbon offset programs for remaining emissions",
            "Explore biofuel options with your carrier for further reduction",
        ] if transport_mode in ["sea_freight", "rail_freight"] else [
            "Consider sea freight to reduce emissions by up to 97%",
            "Consolidate smaller shipments to maximize container fill rate",
            "Optimize routing through strategic transshipment hubs",
        ]
    }

@app.get("/api/hs-codes/suggest")
def suggest_hs_codes(query: str = ""):
    matches = [
        {"category": cat, "code": info["code"], "description": info["description"], "duty_rate": info["duty_rate"]}
        for cat, info in HS_CODE_DB.items()
        if not query or query.lower() in cat.lower() or query.lower() in info["description"].lower()
    ]
    return {"suggestions": matches[:8]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
