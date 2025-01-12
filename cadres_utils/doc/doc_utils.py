import io


def save_document_2_stream(document):
    doc_io = io.BytesIO()
    document.save(doc_io)
    doc_io.seek(0)

    return doc_io
