{
    'name': "Bureaucrat Knowledge",

    'summary': """
        Bureaucrat Knowledge
    """,

    'author': "Center of Research and Development",
    'website': "https://crnd.pro",
    'version': '12.0.0.1.1',
    'category': 'Knowledge',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'generic_mixin',
        'generic_tag',
    ],

    # always loaded
    'data': [
        'data/generic_tag_model.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/bureaucrat_knowledge_category.xml',
        'views/bureaucrat_knowledge_document.xml',
        'views/bureaucrat_knowledge_menu.xml',
    ],
    'images': [],
    'demo': [],

    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
