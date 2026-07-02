"""
TASK 1.3: Synthetic Contract Generation (MSA / SOW style documents)
Generates 8 realistic Master Services Agreement text files that mirror
the CUAD dataset structure, including pricing tiers, penalty clauses,
expiry dates, and service thresholds — the key fields our RAG system
will search against invoice line items.
"""
import os

TARGET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/contracts"))

CONTRACTS = [
    {
        "filename": "Apex_Construction_MSA.txt",
        "vendor": "Apex Construction LLC",
        "vendor_id": "V001",
        "content": """MASTER SERVICES AGREEMENT
Between: GlobalCorp Enterprises Inc. ("Client")
And: Apex Construction LLC ("Vendor")
Vendor ID: V001
Effective Date: January 1, 2025
Expiration Date: December 31, 2027

1. SCOPE OF SERVICES
Vendor shall provide construction and civil engineering services as detailed
in each Statement of Work (SOW) issued under this Agreement.

2. PRICING AND TARIFFS
The following unit rates are agreed and binding for the term of this Agreement:
  - Concrete Foundation Work:    $185.00 per cubic yard
  - Steel Frame Assembly:        $1,200.00 per ton
  - Site Clearing & Grading:     $800.00 per acre
  - Project Management Fee:      $150.00 per hour

Any invoice submitted at rates exceeding the above schedule shall be deemed
non-compliant and subject to a 15% penalty deduction on the overbilled amount.

3. SERVICE THRESHOLDS
Vendor guarantees a minimum monthly delivery capacity of:
  - Concrete work: 200 cubic yards per month
  - Steel assembly: 50 tons per month
Failure to meet these thresholds grants Client the right to source alternative
contractors at Vendor's cost differential.

4. PAYMENT TERMS
Client shall pay undisputed invoices within Net-30 days of receipt.
Disputed amounts shall be resolved within 14 days of written notice.

5. PENALTY CLAUSES
  - Late delivery penalty: 2% of invoice value per week of delay.
  - Non-compliance penalty: $5,000 per materially non-conforming invoice.
  - Overbilling recovery: Client may deduct overbilled amounts from future payments.

6. TERMINATION
Either party may terminate this Agreement with 60 days written notice.
Termination for cause may occur immediately upon material breach.

7. GOVERNING LAW
This Agreement shall be governed by the laws of the State of Texas.
""",
    },
    {
        "filename": "TechBuild_Materials_MSA.txt",
        "vendor": "TechBuild Materials Inc",
        "vendor_id": "V002",
        "content": """MASTER SERVICES AGREEMENT
Between: GlobalCorp Enterprises Inc. ("Client")
And: TechBuild Materials Inc ("Vendor")
Vendor ID: V002
Effective Date: March 1, 2025
Expiration Date: February 28, 2027

1. SCOPE OF SERVICES
Vendor shall supply electrical, HVAC, and building materials as specified in
individual Purchase Orders issued by Client.

2. PRICING AND TARIFFS
Fixed unit rates agreed for the contract period:
  - Electrical Wiring (Phase 1): $320.00 per unit
  - HVAC Installation:           $2,500.00 per unit
  - Plumbing Rough-In:           $1,100.00 per unit
  - Safety Inspection Services:  $400.00 per unit

Rates are fixed for 12 months and subject to CPI adjustment not exceeding 3%
thereafter with 60 days advance written notice to Client.

3. VOLUME DISCOUNTS
  - Orders exceeding 20 HVAC units per quarter: 5% discount
  - Orders exceeding 50 electrical units per quarter: 3% discount

4. PAYMENT TERMS
Net-45 from invoice date. Early payment discount of 1.5% if paid within 15 days.

5. WARRANTY AND LIABILITY
Vendor warrants all installed equipment for a period of 24 months.
Liability for defective materials is capped at the value of the specific order.

6. DISPUTE RESOLUTION
All disputes shall be resolved through binding arbitration in Chicago, Illinois.
""",
    },
    {
        "filename": "GlobalCivil_Partners_MSA.txt",
        "vendor": "GlobalCivil Partners Ltd",
        "vendor_id": "V003",
        "content": """MASTER SERVICES AGREEMENT
Between: GlobalCorp Enterprises Inc. ("Client")
And: GlobalCivil Partners Ltd ("Vendor")
Vendor ID: V003
Effective Date: June 1, 2025
Expiration Date: May 31, 2028

1. SCOPE OF SERVICES
Vendor provides civil engineering, project management, and site preparation
services for large-scale infrastructure projects.

2. PRICING AND TARIFFS
  - Project Management Fee:   $150.00 per hour (capped at 160 hours/month)
  - Site Clearing & Grading:  $800.00 per acre
  - Safety Inspection:        $400.00 per unit inspection

Hourly rate is inclusive of travel within a 50-mile radius of project site.
Travel exceeding 50 miles billed at $0.70/mile in addition to hourly rate.

3. DELIVERABLES AND MILESTONES
  - Monthly progress reports due by the 5th of each month
  - Final milestone sign-off required before invoice submission

4. PAYMENT TERMS
Net-30. Invoices submitted without milestone sign-off documentation will be
held pending receipt of required supporting materials.

5. PRICING ADJUSTMENTS
Client may request competitive re-bid after 18 months if market rates for
equivalent services decline more than 10% per independent survey.

6. CONFIDENTIALITY
Vendor shall maintain strict confidentiality of all project specifications
and Client business data for a period of 5 years post-contract.
""",
    },
    {
        "filename": "PrimeStar_Services_MSA.txt",
        "vendor": "PrimeStar Services Corp",
        "vendor_id": "V004",
        "content": """MASTER SERVICES AGREEMENT
Between: GlobalCorp Enterprises Inc. ("Client")
And: PrimeStar Services Corp ("Vendor")
Vendor ID: V004
Effective Date: April 15, 2025
Expiration Date: April 14, 2026

1. SCOPE OF SERVICES
PrimeStar provides logistics coordination, safety inspection, and
workforce management services on Client construction sites.

2. PRICING SCHEDULE
  - Safety Inspection Services: $400.00 per inspection unit
  - Workforce Coordination:     $150.00 per hour
  - Logistics Management:       $800.00 per day

The above rates represent maximum allowable billing rates. Vendor may
bill below these rates but must not exceed them under any circumstance.

3. COMPLIANCE REQUIREMENTS
All personnel must hold valid OSHA-30 certifications. Vendor will provide
certification records upon Client request within 2 business days.

4. INSURANCE REQUIREMENTS
Vendor shall maintain:
  - General Liability: minimum $2,000,000 per occurrence
  - Workers Compensation as required by law
  - Professional Liability: minimum $1,000,000

5. PAYMENT TERMS
Net-30 from verified invoice receipt. Client has right to audit invoices
and request supporting documentation for any line item within 60 days.

6. TERMINATION FOR CONVENIENCE
Client may terminate with 30 days notice. Vendor entitled to payment for
work completed as of termination date only.
""",
    },
    {
        "filename": "Northern_Logistics_MSA.txt",
        "vendor": "Northern Logistics Co",
        "vendor_id": "V005",
        "content": """MASTER SERVICES AGREEMENT
Between: GlobalCorp Enterprises Inc. ("Client")
And: Northern Logistics Co ("Vendor")
Vendor ID: V005
Effective Date: February 1, 2025
Expiration Date: January 31, 2027

1. SCOPE OF SERVICES
Northern Logistics provides freight transport, materials staging, and
delivery coordination for all Client construction site requirements.

2. RATE SCHEDULE
  - Local freight (within 50 miles): $200.00 per delivery
  - Long-haul freight (50-300 miles): $0.75 per ton-mile
  - Emergency delivery surcharge: 35% above standard rate
  - Staging and warehousing: $1.50 per pallet per day

3. SERVICE LEVEL AGREEMENT
  - Standard delivery: 3-5 business days
  - Priority delivery: 24-48 hours (surcharge applies)
  - On-time delivery target: 95% or above on rolling 90-day basis

Failure to meet SLA targets for two consecutive months gives Client
the right to renegotiate rates downward by up to 10%.

4. CLAIMS AND LIABILITY
Vendor is liable for lost or damaged cargo up to invoice value.
Claims must be filed within 5 business days of delivery.

5. FUEL SURCHARGE
A fuel surcharge of up to 8% may be applied when diesel index exceeds
$4.00/gallon. Surcharge must be itemized separately on each invoice.
""",
    },
    {
        "filename": "SouthWest_Build_Group_MSA.txt",
        "vendor": "SouthWest Build Group",
        "vendor_id": "V006",
        "content": """MASTER SERVICES AGREEMENT
Between: GlobalCorp Enterprises Inc. ("Client")
And: SouthWest Build Group ("Vendor")
Vendor ID: V006
Effective Date: July 1, 2025
Expiration Date: June 30, 2028

1. SCOPE OF SERVICES
SouthWest Build Group provides comprehensive commercial construction
services including foundation, framing, MEP, and finishing work.

2. PRICING SCHEDULE (BINDING RATES)
  - Concrete Foundation Work:    $185.00 per cubic yard
  - Steel Frame Assembly:        $1,200.00 per ton
  - Electrical Wiring (Phase 1): $320.00 per unit
  - HVAC Installation:           $2,500.00 per unit
  - Plumbing Rough-In:           $1,100.00 per unit
  - Project Management Fee:      $150.00 per hour

The foregoing rates are firm and not subject to escalation during
the initial 24-month period. Renegotiation may occur at month 25.

3. QUALITY STANDARDS
All work must conform to IBC 2021 standards. Third-party inspection
reports must accompany milestone billing submissions.

4. PAYMENT TERMS
Progress billing permitted at 20% project completion intervals.
Final 10% withheld pending punch-list completion and sign-off.
Net-30 on all approved progress invoices.

5. LIQUIDATED DAMAGES
Delays attributable to Vendor beyond agreed milestone schedule:
  $2,500 per calendar day for the first 14 days of delay.
  $5,000 per calendar day thereafter.

6. CHANGE ORDER PROCESS
No additional cost without written Change Order executed by both parties
prior to commencement of changed scope of work.

7. DISPUTE RESOLUTION
Mediation first, then binding arbitration in Phoenix, Arizona.
""",
    },
    {
        "filename": "Hybrid_Engineering_SOW.txt",
        "vendor": "Multiple Vendors",
        "vendor_id": "MULTI",
        "content": """STATEMENT OF WORK (SOW) - Q3 2025 CONSTRUCTION PROGRAM
Issued under Master Services Agreements on file.
Client: GlobalCorp Enterprises Inc.
Program Reference: GCORP-Q3-2025-BUILD

1. PROGRAM OVERVIEW
This SOW governs all vendor activity during the Q3 2025 Construction
Program for the Dallas Campus Expansion Project.

2. SCOPE BREAKDOWN
Phase A: Site Preparation
  - Site Clearing & Grading (all acres): $800.00/acre — Vendor: V001, V003
  - Safety Pre-inspection:               $400.00/unit — Vendor: V004

Phase B: Foundation & Structure
  - Concrete Foundation:  $185.00/cubic yard — Vendor: V001, V006
  - Steel Frame Assembly: $1,200.00/ton — Vendor: V001

Phase C: MEP Installation
  - Electrical Wiring:    $320.00/unit — Vendor: V002
  - HVAC Installation:    $2,500.00/unit — Vendor: V002
  - Plumbing Rough-In:    $1,100.00/unit — Vendor: V002, V006

Phase D: Project Oversight
  - Project Management:   $150.00/hour (max 160 hrs/month) — Vendor: V003

3. COMPLIANCE NOTE
Any invoice submitted under this SOW must reference this program number.
Rates must match the applicable MSA schedule. Any variance triggers
automatic audit review per GlobalCorp Procurement Policy 4.3.2.
""",
    },
    {
        "filename": "Electrical_Subcontract_Agreement.txt",
        "vendor": "TechBuild Materials Inc",
        "vendor_id": "V002",
        "content": """SUBCONTRACT AGREEMENT FOR ELECTRICAL SERVICES
Prime Contract No.: GC-ELEC-2025-001
Subcontractor: TechBuild Materials Inc (V002)
Prime Contractor: GlobalCorp Enterprises Inc.
Project: Dallas Campus Expansion — Electrical Package
Date: May 1, 2025

1. SUBCONTRACT SCOPE
Subcontractor shall furnish all labor, materials, and equipment necessary
to complete electrical installation as per Drawings E-001 through E-045.

2. CONTRACT SUM
  - Phase 1 Electrical Wiring: $320.00 per unit (as per MSA dated March 1, 2025)
  - Phase 2 Electrical Panels: $480.00 per unit (per attached schedule)
  - Testing & Commissioning:   $200.00 per unit

Total estimated contract value: $850,000.00 (subject to final unit counts).

3. SCHEDULE
  - Notice to Proceed: May 15, 2025
  - Substantial Completion: September 30, 2025
  - Final Completion: October 31, 2025

4. BILLING REQUIREMENTS
Monthly applications for payment shall include:
  a) Signed Schedule of Values (AIA G702/G703)
  b) Conditional lien waiver for current period
  c) Unconditional lien waiver for prior paid amounts

5. RETAINAGE
10% retainage withheld from each payment application until
Substantial Completion is certified by Client's engineer.

6. CHANGE ORDER RATES
For changes within scope of work:
  - Journeyman Electrician: $95.00/hour
  - Foreman:                $115.00/hour
  - Materials: cost + 15% markup

7. INDEMNIFICATION
Subcontractor shall indemnify and hold harmless Prime Contractor and Owner
against all claims arising from Subcontractor's operations.
""",
    },
]


def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    for contract in CONTRACTS:
        path = os.path.join(TARGET_DIR, contract["filename"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(contract["content"])
        size = len(contract["content"])
        print(f"  Saved: {contract['filename']}  ({size:,} chars)")
    print(f"\nDone. {len(CONTRACTS)} contracts saved to: {TARGET_DIR}")


if __name__ == "__main__":
    main()
