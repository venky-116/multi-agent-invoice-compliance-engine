from typing import TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage

class AuditState(TypedDict):
    # Complete conversation/thought history
    messages: List[BaseMessage]
    
    # Path of the invoice PDF currently being audited
    invoice_path: str
    
    # Extracted data from the invoice PDF
    invoice_extracted_data: Dict[str, Any]
    
    # Validation errors encountered during invoice extraction
    extraction_errors: str
    
    # Count of extraction validation attempts
    extraction_attempts: int
    
    # Matching contract clauses retrieved from RAG
    contract_clauses_retrieved: List[str]
    
    # Matching ERP logs retrieved from SQL database
    erp_logs_retrieved: List[Dict[str, Any]]
    
    # Detailed discrepancies identified by the deterministic calculator
    audit_discrepancies: List[Dict[str, Any]]
    
    # Raw generated sandboxed audit python code
    audit_code: str
    
    # Errors/Traceback caught during sandbox python script run
    audit_code_errors: str
    
    # Count of sandbox run attempts
    audit_code_attempts: int
    
    # Sum of financial variances (price or quantity overcharges)
    risk_score: float
    
    # Iteration counter to prevent infinite routing loops
    current_iteration: int
    
    # Flag to indicate if a human has approved the invoice audit manually
    human_approved: bool
    
    # Path to the generated automated dispute letter (if any)
    dispute_draft_path: str
