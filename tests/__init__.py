from . import (
    test_bureaucrat_knowledge,
    test_knowledge_category_read,
    test_knowledge_document_read,
    test_knowledge_category_write,
    test_knowledge_document_write,
    test_knowledge_category_unlink,
    test_knowledge_document_unlink,
    test_knowledge_document_history_read,
    test_knowledge_document_history_edit,

    # TODO: Add tests for creation
    # Apply following logic:
    # If document or category has parent, then user have not to be added to
    # owners or editors
    # If user creates top-level document or category, then he have to become
    # owner of created doc or category.
)
