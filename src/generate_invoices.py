"""
TASK 1.4: Synthetic Invoice PDF Generation (replaces MIDD .rar download)
Generates 6 realistic multi-layout supplier invoice PDFs using reportlab.
Each PDF mimics a different MIDD layout type.
"""
import os
import sqlite3
from datetime import datetime, timedelta
import random

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_RIGHT, TA_CENTER
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False
    print("reportlab not installed. Run: pip install reportlab")

INVOICE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/invoices"))
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/erp_logs.db"))

random.seed(42)

SUPPLIERS = [
    {"name": "Apex Construction LLC",    "vendor_id": "V001", "address": "45 Industrial Blvd, Houston TX 77001"},
    {"name": "TechBuild Materials Inc",  "vendor_id": "V002", "address": "220 Supplier Ave, Chicago IL 60601"},
    {"name": "GlobalCivil Partners Ltd", "vendor_id": "V003", "address": "99 Engineering Way, Dallas TX 75201"},
    {"name": "PrimeStar Services Corp",  "vendor_id": "V004", "address": "12 Commerce Lane, Atlanta GA 30301"},
    {"name": "Northern Logistics Co",    "vendor_id": "V005", "address": "33 Freight Drive, Detroit MI 48201"},
    {"name": "SouthWest Build Group",    "vendor_id": "V006", "address": "78 Contractors Rd, Phoenix AZ 85001"},
]

SERVICE_ITEMS = [
    ("Concrete Foundation Work",    "cubic yard",  185.00,  195.00),
    ("Electrical Wiring - Phase 1", "unit",        320.00,  350.00),
    ("HVAC Installation",           "unit",       2500.00, 2750.00),
    ("Steel Frame Assembly",        "ton",        1200.00, 1350.00),
    ("Project Management Fee",      "hour",        150.00,  175.00),
    ("Safety Inspection Services",  "unit",        400.00,  420.00),
    ("Site Clearing & Grading",     "acre",        800.00,  900.00),
    ("Plumbing Rough-In",           "unit",       1100.00, 1200.00),
]

def make_invoice_data(supplier: dict, inv_num: str, items_subset: list, layout: int):
    inv_date = datetime(2025, random.randint(1, 12), random.randint(1, 28))
    due_date = inv_date + timedelta(days=30)
    line_items = []
    for name, unit, contract_rate, invoice_rate in items_subset:
        qty = random.randint(5, 50)
        line_items.append({
            "description": name,
            "unit": unit,
            "qty": qty,
            "contract_rate": contract_rate,
            "invoice_rate": invoice_rate,
            "total": round(qty * invoice_rate, 2),
        })
    subtotal = round(sum(i["total"] for i in line_items), 2)
    tax = round(subtotal * 0.08, 2)
    grand_total = round(subtotal + tax, 2)
    return {
        "invoice_number": inv_num,
        "supplier": supplier,
        "invoice_date": inv_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "line_items": line_items,
        "subtotal": subtotal,
        "tax": tax,
        "grand_total": grand_total,
        "layout": layout,
    }

def build_pdf_layout1(doc_path: str, inv: dict):
    """Layout 1: Standard single-column table invoice."""
    doc = SimpleDocTemplate(doc_path, pagesize=A4, topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    elements = []

    # Header
    elements.append(Paragraph(f"<b>INVOICE</b>", styles["Title"]))
    elements.append(Paragraph(f"Invoice #: {inv['invoice_number']}", styles["Normal"]))
    elements.append(Paragraph(f"Date: {inv['invoice_date']}   Due: {inv['due_date']}", styles["Normal"]))
    elements.append(Spacer(1, 5*mm))

    # Supplier
    elements.append(Paragraph(f"<b>From:</b> {inv['supplier']['name']}", styles["Normal"]))
    elements.append(Paragraph(inv['supplier']['address'], styles["Normal"]))
    elements.append(Spacer(1, 5*mm))

    # Line items table
    table_data = [["#", "Description", "Unit", "Qty", "Rate (USD)", "Total (USD)"]]
    for i, item in enumerate(inv["line_items"], 1):
        table_data.append([
            str(i),
            item["description"],
            item["unit"],
            str(item["qty"]),
            f"${item['invoice_rate']:,.2f}",
            f"${item['total']:,.2f}",
        ])
    table = Table(table_data, colWidths=[10*mm, 65*mm, 25*mm, 15*mm, 28*mm, 28*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F8F8")]),
        ("ALIGN", (3, 0), (-1, -1), "RIGHT"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 5*mm))

    # Totals
    totals_data = [
        ["Subtotal:", f"${inv['subtotal']:,.2f}"],
        ["Tax (8%):",  f"${inv['tax']:,.2f}"],
        ["TOTAL DUE:", f"${inv['grand_total']:,.2f}"],
    ]
    totals_table = Table(totals_data, colWidths=[140*mm, 30*mm])
    totals_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("LINEABOVE", (0, 2), (-1, 2), 1, colors.black),
    ]))
    elements.append(totals_table)
    doc.build(elements)


def build_pdf_layout2(doc_path: str, inv: dict):
    """Layout 2: Two-section invoice with header box and condensed table."""
    doc = SimpleDocTemplate(doc_path, pagesize=A4, topMargin=15*mm, bottomMargin=15*mm)
    styles = getSampleStyleSheet()
    elements = []

    # Header box
    header_data = [
        [Paragraph(f"<b>{inv['supplier']['name']}</b>", styles["Normal"]),
         Paragraph(f"<b>TAX INVOICE</b>", styles["Title"])],
        [Paragraph(inv['supplier']['address'], styles["Normal"]),
         Paragraph(f"Invoice #: {inv['invoice_number']}\nDate: {inv['invoice_date']}", styles["Normal"])],
    ]
    header_table = Table(header_data, colWidths=[95*mm, 80*mm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A5276")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 8*mm))

    # Items
    table_data = [["Description", "Unit", "Qty", "Unit Price", "Amount"]]
    for item in inv["line_items"]:
        table_data.append([
            item["description"], item["unit"], item["qty"],
            f"${item['invoice_rate']:,.2f}", f"${item['total']:,.2f}",
        ])
    table = Table(table_data, colWidths=[70*mm, 25*mm, 15*mm, 32*mm, 33*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E86C1")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 6*mm))
    elements.append(Paragraph(f"<b>Grand Total (incl. 8% tax): ${inv['grand_total']:,.2f}</b>", styles["Normal"]))
    doc.build(elements)


def build_pdf_layout3(doc_path: str, inv: dict):
    """Layout 3: Minimal two-column layout with no grid lines."""
    doc = SimpleDocTemplate(doc_path, pagesize=A4)
    styles = getSampleStyleSheet()
    right_style = ParagraphStyle("right", parent=styles["Normal"], alignment=TA_RIGHT)
    elements = []

    elements.append(Paragraph(f"<b>{inv['supplier']['name'].upper()}</b>", styles["Heading1"]))
    elements.append(Paragraph(inv["supplier"]["address"], styles["Normal"]))
    elements.append(Spacer(1, 6*mm))
    elements.append(Paragraph(f"INVOICE NO: {inv['invoice_number']}  |  DATE: {inv['invoice_date']}", styles["Normal"]))
    elements.append(Spacer(1, 8*mm))

    for item in inv["line_items"]:
        row_data = [[
            Paragraph(f"{item['description']} ({item['qty']} {item['unit']})", styles["Normal"]),
            Paragraph(f"${item['total']:,.2f}", right_style),
        ]]
        row_table = Table(row_data, colWidths=[135*mm, 40*mm])
        row_table.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ]))
        elements.append(row_table)

    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph(f"Subtotal: ${inv['subtotal']:,.2f}  |  Tax: ${inv['tax']:,.2f}  |  <b>Total: ${inv['grand_total']:,.2f}</b>", styles["Normal"]))
    doc.build(elements)


def seed_erp_db(invoices: list):
    """Seed SQLite ERP database with actual delivery records."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS erp_delivery_logs")
    c.execute("""
        CREATE TABLE erp_delivery_logs (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT NOT NULL,
            vendor_id      TEXT NOT NULL,
            vendor_name    TEXT NOT NULL,
            item_desc      TEXT NOT NULL,
            unit           TEXT NOT NULL,
            qty_ordered    INTEGER,
            qty_delivered  INTEGER,
            contract_rate  REAL,
            invoice_date   TEXT
        )
    """)
    rows = []
    for inv in invoices:
        for item in inv["line_items"]:
            # Occasionally simulate a delivery short-shipment
            qty_delivered = item["qty"] if random.random() > 0.15 else item["qty"] - random.randint(1, 3)
            rows.append((
                inv["invoice_number"],
                inv["supplier"]["vendor_id"],
                inv["supplier"]["name"],
                item["description"],
                item["unit"],
                item["qty"],
                max(qty_delivered, 1),
                item["contract_rate"],
                inv["invoice_date"],
            ))
    c.executemany("""
        INSERT INTO erp_delivery_logs
            (invoice_number, vendor_id, vendor_name, item_desc, unit, qty_ordered, qty_delivered, contract_rate, invoice_date)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, rows)
    conn.commit()
    conn.close()
    print(f"ERP DB seeded with {len(rows)} delivery log records at:\n  {DB_PATH}")


def main():
    if not REPORTLAB_OK:
        return

    os.makedirs(INVOICE_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    invoices = []
    layouts = [build_pdf_layout1, build_pdf_layout2, build_pdf_layout3]

    for i, supplier in enumerate(SUPPLIERS):
        inv_num = f"INV-2025-{str(i+1).zfill(4)}"
        items_subset = random.sample(SERVICE_ITEMS, k=random.randint(3, 5))
        layout_idx = i % len(layouts)
        inv = make_invoice_data(supplier, inv_num, items_subset, layout_idx + 1)
        invoices.append(inv)

        pdf_path = os.path.join(INVOICE_DIR, f"{inv_num}.pdf")
        layouts[layout_idx](pdf_path, inv)
        print(f"Generated: {pdf_path}  (Layout {layout_idx+1}, Supplier: {supplier['name']})")

    seed_erp_db(invoices)
    print(f"\nAll done. {len(invoices)} invoices generated in: {INVOICE_DIR}")


if __name__ == "__main__":
    main()
