{
    'name': "Bureaucrat Knowledge",

    'summary': """
        Bureaucrat Knowledge
    """,

    'author': "Center of Research and Development",
    'website': "https://crnd.pro",
    'version': '11.0.0.4.0',
    'category': 'Knowledge',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'generic_mixin',
        'generic_tag',
        'mail',
    ],

    # always loaded
    'data': [
        'data/generic_tag_model.xml',
        'data/bureaucrat_knowledge_base_data.xml',
        'data/bureaucrat_knowledge_base_documents_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/bureaucrat_knowledge_category.xml',
        'views/bureaucrat_knowledge_document.xml',
        'views/bureaucrat_knowledge_menu.xml',
        'views/bureaucrat_knowledge_document_history.xml',

        'templates/templates.xml',
        'templates/category_content.xml',
    ],
    'images': [],
    'demo': [],

    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
