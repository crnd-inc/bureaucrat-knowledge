Rename `document_type` field to `document_format`.
This is needed to introduce new document types as separate model.
For backward compatability there is `document_type` field
added as compute+inverse to automatically write values for document format
