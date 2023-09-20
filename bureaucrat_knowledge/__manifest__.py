{
    'name': "Bureaucrat Knowledge",

    'summary': """
        Bureaucrat Knowledge
    """,

    'author': "Center of Research and Development",
    'website': "https://crnd.pro",
    'version': '15.0.0.37.1',
    'category': 'Knowledge',

    'external_dependencies': {
        'python': [
            'html2text',
            'pdf2image',
        ],
        'bin': [
            'pdftoppm',
        ],
    },
    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'base_field_m2m_view',
        'generic_mixin',
        'generic_tag',
        'mail',
    ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/generic_tag_model.xml',
        'data/document_types_data.xml',
        'data/bureaucrat_knowledge_base_data.xml',
        'data/bureaucrat_knowledge_base_documents_data.xml',

        'views/bureaucrat_knowledge_category.xml',
        'views/bureaucrat_knowledge_document.xml',
        'views/bureaucrat_knowledge_document_history.xml',
        'views/bureaucrat_knowledge_document_type.xml',
        'views/bureaucrat_knowledge_menu.xml',

        'templates/category_content.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'bureaucrat_knowledge/static/src/scss/knowledge_base.scss',
        ],
    },
    'images': ['static/description/banner.png'],
    'demo': [
        'demo/res_groups.xml',
        'demo/bureaucrat_knowledge_demo.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
