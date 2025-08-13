# Copyright (c) 2025, Navtech and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data()

    # Donut chart using total revenue per airline
    chart = {
        "data": {
            "labels": [row["airline"] for row in data],
            "datasets": [
                {
                    "name": "Total Revenue",
                    "values": [row["total_revenue"] for row in data]
                }
            ]
        },
        "type": "donut"
    }

    # Summary row with total revenue
    summary = [
        {
            "label": _("Total Revenue"),
            "value": sum(row["total_revenue"] for row in data),
            "indicator": "Green"
        }
    ]

    return columns, data, None, chart, summary

def get_columns():
    return [
        {
            "label": _("Airline"),
            "fieldname": "airline",
            "fieldtype": "Link",
            "width": 200
        },
        {
            "label": _("Total Revenue"),
            "fieldname": "total_revenue",
            "fieldtype": "Currency",
            "width": 150
        }
    ]

def get_data():
    return frappe.db.sql("""
        SELECT
            al.name AS airline,
            SUM(at.total_amount) AS total_revenue
        FROM `tabAirplane Ticket` at
        INNER JOIN `tabAirplane Flight` af ON at.flight = af.name
        INNER JOIN `tabAirplane` a ON af.airplane = a.name
        INNER JOIN `tabAirline` al ON a.airline = al.name
        WHERE at.docstatus = 1
        GROUP BY al.name
        ORDER BY total_revenue DESC
    """, as_dict=True)

