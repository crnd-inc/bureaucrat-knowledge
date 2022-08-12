- Added complex (computed) field 'code' to document
This field have to consist of three parts: category_code, document_type_code, 
  document_number

- Added field to document 'document_number'. 
As default values for already existing documents (or for new documents)
  we use sequence defined on document type. 
  Added generator for 'document_number'
