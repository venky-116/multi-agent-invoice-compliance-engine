import os
import sys
from dotenv import load_dotenv

# Add workspace to path just in case
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.graph import get_compiled_graph

def run_audit():
    load_dotenv()
    
    # 1. API Key validation
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "YOUR_GROQ_API_KEY":
        print("\n[WARNING] GROQ_API_KEY is not configured in your .env file!")
        print("The system will execute in Local Offline Fallback Mode using rule-based parsers.")
        print("To run with Llama 3.3 reasoning, edit d:/langGraph/.env and set your key.\n")
        
    # 2. Argument validation
    if len(sys.argv) < 2:
        print("\n[USAGE] python src/run_audit.py <path_to_invoice_pdf>")
        print("Example: python src/run_audit.py data/invoices/INV-2025-0001.pdf")
        sys.exit(1)
        
    invoice_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(invoice_path):
        print(f"\n[ERROR] Invoice PDF file not found at: {invoice_path}")
        sys.exit(1)
        
    print("\n" + "=" * 60)
    print("STARTING INVOICE AUDIT COMPLIANCE RUN")
    print(f"Target Invoice: {invoice_path}")
    print("=" * 60)
    
    # Define stable thread ID from invoice filename
    base = os.path.basename(invoice_path)
    invoice_name = os.path.splitext(base)[0]
    thread_id = f"thread_{invoice_name}"
    config = {"configurable": {"thread_id": thread_id}}
    
    # Build initial empty state
    initial_state = {
        "messages": [],
        "invoice_path": invoice_path,
        "invoice_extracted_data": {},
        "extraction_errors": "",
        "extraction_attempts": 0,
        "contract_clauses_retrieved": [],
        "erp_logs_retrieved": [],
        "audit_discrepancies": [],
        "audit_code": "",
        "audit_code_errors": "",
        "audit_code_attempts": 0,
        "risk_score": 0.0,
        "current_iteration": 0,
        "human_approved": False,
        "dispute_draft_path": ""
    }
    
    # Compile and execute within Sqlite checkpointer scope
    with get_compiled_graph() as app:
        print(f"Initial setup complete. Thread ID: {thread_id}")
        
        # Stream states
        current_state = initial_state
        for event in app.stream(initial_state, config):
            for node_name, state_update in event.items():
                print(f"\n>>> Executed Node: {node_name}")
                
                # Report key changes
                if state_update and isinstance(state_update, dict):
                    if "invoice_extracted_data" in state_update:
                        ext = state_update["invoice_extracted_data"]
                        print(f"  - Extracted Invoice #: {ext.get('invoice_number')} | Vendor: {ext.get('vendor_id')} ({ext.get('vendor_name')})")
                        print(f"  - Items Extracted: {len(ext.get('line_items', []))} items")
                        
                    if "contract_clauses_retrieved" in state_update:
                        print(f"  - Retrieved {len(state_update['contract_clauses_retrieved'])} matching legal contract clauses.")
                        
                    if "erp_logs_retrieved" in state_update:
                        print(f"  - Loaded {len(state_update['erp_logs_retrieved'])} delivery log events from ERP SQL database.")
                        
                    if "audit_discrepancies" in state_update:
                        print(f"  - Audit calculation completed. Discrepancies: {len(state_update['audit_discrepancies'])}")
                        
                    if "risk_score" in state_update:
                        print(f"  - Risk Score Calculated: ${state_update['risk_score']:,.2f}")
                        
                    if "dispute_draft_path" in state_update:
                        print(f"  - Automated dispute draft saved at: {state_update['dispute_draft_path']}")
                    
        # Check current graph state
        final_state = app.get_state(config)
        
        if final_state.next:
            # Graph is paused at an interrupt (Human-in-the-Loop)
            print("\n" + "!" * 60)
            print("WARNING: AUDIT PROCESS INTERRUPTED & PAUSED (HITL)")
            print(f"The discrepancy value (${final_state.values.get('risk_score', 0.0):,.2f}) exceeds the $5,000.00 compliance limit.")
            print(f"State saved to SQLite checkpointer. The graph is paused at: '{final_state.next[0]}'")
            print("\nHow to resolve/approve:")
            print(f"  Run the approval script with this thread id:")
            print(f"  .venv/Scripts/python.exe src/human_approve.py {thread_id}")
            print("!" * 60 + "\n")
        else:
            # Run finished to completion
            print("\n" + "=" * 60)
            print("AUDIT PROCESS COMPLETED")
            risk = final_state.values.get("risk_score", 0.0)
            print(f"Final Audit Risk: ${risk:,.2f}")
            if risk == 0:
                print("Status: COMPLIANT (Passed)")
            elif risk <= 5000:
                print("Status: NON-COMPLIANT (Dispute Drafted)")
                print(f"Letter Path: {final_state.values.get('dispute_draft_path')}")
            else:
                print("Status: COMPLETED WITH MANUAL HUMAN OVERRIDE / APPROVAL")
            print("=" * 60 + "\n")

if __name__ == "__main__":
    run_audit()
