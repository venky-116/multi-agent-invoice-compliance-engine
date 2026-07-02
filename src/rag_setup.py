import os
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Map contract filenames to vendor metadata
VENDOR_MAP = {
    "Apex_Construction_MSA.txt": {"vendor_id": "V001", "vendor_name": "Apex Construction LLC"},
    "TechBuild_Materials_MSA.txt": {"vendor_id": "V002", "vendor_name": "TechBuild Materials Inc"},
    "GlobalCivil_Partners_MSA.txt": {"vendor_id": "V003", "vendor_name": "GlobalCivil Partners Ltd"},
    "PrimeStar_Services_MSA.txt": {"vendor_id": "V004", "vendor_name": "PrimeStar Services Corp"},
    "Northern_Logistics_MSA.txt": {"vendor_id": "V005", "vendor_name": "Northern Logistics Co"},
    "SouthWest_Build_Group_MSA.txt": {"vendor_id": "V006", "vendor_name": "SouthWest Build Group"},
    "Hybrid_Engineering_SOW.txt": {"vendor_id": "MULTI", "vendor_name": "Multiple Vendors"},
    "Electrical_Subcontract_Agreement.txt": {"vendor_id": "V002", "vendor_name": "TechBuild Materials Inc"},
}

CONTRACTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/contracts"))
CHROMA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/chroma_db"))

def setup_rag():
    print("Initializing Chroma RAG setup...")
    
    # 1. Clean existing chroma directory
    if os.path.exists(CHROMA_DIR):
        print(f"Cleaning existing Chroma database at {CHROMA_DIR}...")
        shutil.rmtree(CHROMA_DIR)
        
    os.makedirs(CHROMA_DIR, exist_ok=True)
    
    # 2. Initialize Embeddings
    print("Loading HuggingFace embeddings model (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 3. Read and process documents
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    for filename in os.listdir(CONTRACTS_DIR):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(CONTRACTS_DIR, filename)
        
        if filename in VENDOR_MAP:
            meta = VENDOR_MAP[filename]
        else:
            clean_name = filename.replace(".txt", "")
            vendor_name = clean_name.split('_')[0]
            meta = {
                "vendor_id": "CUAD_" + vendor_name[:10].upper(),
                "vendor_name": vendor_name.replace("INC", " Inc").replace("CO", " Co").title()
            }
            
        print(f"Reading contract: {filename} for Vendor {meta['vendor_id']} ({meta['vendor_name']})")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Create langchain document
        doc = Document(
            page_content=content,
            metadata={
                "source": filename,
                "vendor_id": meta["vendor_id"],
                "vendor_name": meta["vendor_name"]
            }
        )
        
        # Split document
        chunks = text_splitter.split_documents([doc])
        print(f"  Split into {len(chunks)} chunks ({meta['vendor_id']}).")
        documents.extend(chunks)
        
    # 4. Save to Chroma DB
    print(f"Saving {len(documents)} document chunks to Chroma DB at {CHROMA_DIR}...")
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    print("Chroma DB populated and persisted successfully!")
    
    # 5. Simple verification
    print("\nRunning quick retrieval verification...")
    # Search for V001 (Apex) pricing
    results = vector_store.similarity_search(
        "Concrete Foundation Work",
        k=2,
        filter={"vendor_id": "V001"}
    )
    
    print(f"Found {len(results)} chunks matching V001 filter:")
    for i, res in enumerate(results):
        print(f"\nResult {i+1} (Source: {res.metadata['source']}):")
        print("-" * 50)
        # Print a snippet of page_content
        print(res.page_content[:250] + "...")
        print("-" * 50)

if __name__ == "__main__":
    setup_rag()
