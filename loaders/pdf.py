from .common import process_file
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import PyMuPDFLoader


def process_pdf(vector_store, file, stats_db):
    return process_file(vector_store, file, PyMuPDFLoader, ".pdf", stats_db=stats_db)
