import os
from contextlib import contextmanager
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import Dict, Any

from src.state import AuditState
from src.agent_nodes import (
    invoice_extractor_node,
    contract_retriever_node,
    erp_validator_node,
    deterministic_audit_node,
    dispute_drafter_node,
    invoice_extractor_node
)
from src.agent_nodes import supervisor_node

# Placeholder node for human verification
def human_verification_node(state: AuditState) -> Dict[str, Any]:
    print("\n--- [NODE] HUMAN VERIFICATION (RESUMED) ---")
    print("Execution resumed by human approval.")
    return {"human_approved": True}

# Node for handling escalation failure (infinite loop protection)
def escalation_failure_node(state: AuditState) -> Dict[str, Any]:
    print("\n--- [NODE] ESCALATION FAILURE ---")
    print(f"CRITICAL: Audit for invoice {state.get('invoice_path')} exceeded max iteration threshold without completion.")
    print("Halting audit and saving error log.")
    return {}

# Routing function based on Supervisor decision
def route_decision(state: AuditState) -> str:
    messages = state.get("messages", [])
    if not messages:
        print("Warning: No messages found in state, routing to supervisor.")
        return "supervisor"
        
    last_message = messages[-1]
    decision = last_message.content.strip().upper()
    
    if decision == "EXTRACT":
        return "invoice_extractor"
    elif decision == "RETRIEVE":
        return "contract_retriever"
    elif decision == "VALIDATE":
        return "erp_validator"
    elif decision == "AUDIT":
        return "deterministic_audit"
    elif decision == "DISPUTE":
        return "dispute_drafter"
    elif decision == "HUMAN_VERIFY":
        return "human_verification"
    elif decision == "ESCALATE":
        return "escalation_failure"
    elif decision == "END":
        return END
    else:
        print(f"Warning: Unknown decision '{decision}', routing to END.")
        return END

def build_workflow() -> StateGraph:
    # 1. Initialize StateGraph
    workflow = StateGraph(AuditState)
    
    # 2. Register Nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("invoice_extractor", invoice_extractor_node)
    workflow.add_node("contract_retriever", contract_retriever_node)
    workflow.add_node("erp_validator", erp_validator_node)
    workflow.add_node("deterministic_audit", deterministic_audit_node)
    workflow.add_node("dispute_drafter", dispute_drafter_node)
    workflow.add_node("human_verification", human_verification_node)
    workflow.add_node("escalation_failure", escalation_failure_node)
    
    # 3. Configure Entry Point and Edges
    workflow.set_entry_point("supervisor")
    
    # Workers route back to the supervisor
    workflow.add_edge("invoice_extractor", "supervisor")
    workflow.add_edge("contract_retriever", "supervisor")
    workflow.add_edge("erp_validator", "supervisor")
    workflow.add_edge("deterministic_audit", "supervisor")
    workflow.add_edge("dispute_drafter", "supervisor")
    workflow.add_edge("human_verification", "supervisor")
    workflow.add_edge("escalation_failure", END)
    
    # Define conditional edges from Supervisor
    workflow.add_conditional_edges(
        "supervisor",
        route_decision,
        {
            "invoice_extractor": "invoice_extractor",
            "contract_retriever": "contract_retriever",
            "erp_validator": "erp_validator",
            "deterministic_audit": "deterministic_audit",
            "dispute_drafter": "dispute_drafter",
            "human_verification": "human_verification",
            "escalation_failure": "escalation_failure",
            END: END
        }
    )
    
    return workflow

@contextmanager
def get_compiled_graph(db_path: str = "data/audit_checkpoint.db"):
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    workflow = build_workflow()
    
    # SQLite connection for state serialization persistence
    with SqliteSaver.from_conn_string(db_path) as checkpointer:
        # Enforce interrupt before human verification node
        app = workflow.compile(
            checkpointer=checkpointer,
            interrupt_before=["human_verification"]
        )
        yield app
