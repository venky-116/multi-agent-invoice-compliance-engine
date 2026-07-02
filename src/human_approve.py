import os
import sys
from dotenv import load_dotenv

# Add workspace to path just in case
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.graph import get_compiled_graph

def human_approve():
    load_dotenv()
    
    # 1. Argument validation
    if len(sys.argv) < 2:
        print("\n[USAGE] python src/human_approve.py <thread_id>")
        print("Example: python src/human_approve.py thread_INV-2025-0002")
        sys.exit(1)
        
    thread_id = sys.argv[1]
    config = {"configurable": {"thread_id": thread_id}}
    
    print("\n" + "=" * 60)
    print(f"RESUMING AUDIT THREAD: {thread_id}")
    print("=" * 60)
    
    with get_compiled_graph() as app:
        # Check current state first
        state_info = app.get_state(config)
        if not state_info.values:
            print(f"[ERROR] No audit state found for Thread ID: {thread_id}")
            print("Please run the audit first using src/run_audit.py.")
            sys.exit(1)
            
        if not state_info.next:
            print("[INFO] This audit thread has already completed.")
            print(f"Final Risk Score was: ${state_info.values.get('risk_score', 0.0):,.2f}")
            sys.exit(0)
            
        print(f"Current risk score: ${state_info.values.get('risk_score', 0.0):,.2f}")
        print(f"Paused at node: '{state_info.next[0]}'")
        print("Applying human approval override and resuming...")
        
        # Update state to set human_approved = True, simulating human verification
        app.update_state(config, {"human_approved": True}, as_node="human_verification")
        
        # Resume the graph execution from the interrupt point
        for event in app.stream(None, config):
            for node_name, state_update in event.items():
                print(f"\n>>> Executed Node: {node_name}")
                if state_update and isinstance(state_update, dict):
                    if "risk_score" in state_update:
                        print(f"  - Risk Score: ${state_update['risk_score']:,.2f}")
                    if "dispute_draft_path" in state_update:
                        print(f"  - Generated dispute letter at: {state_update['dispute_draft_path']}")
                    
        # Check completion state
        final_state = app.get_state(config)
        print("\n" + "=" * 60)
        print("AUDIT PROCESS COMPLETED AFTER HUMAN OVERRIDE")
        print(f"Final Audit Risk: ${final_state.values.get('risk_score', 0.0):,.2f}")
        print("Status: APPROVED (Manual Override)")
        print("=" * 60 + "\n")

if __name__ == "__main__":
    human_approve()
