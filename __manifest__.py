{
    'name': "Bureaucrat Knowledge",

    'summary': """
        Bureaucrat Knowledge
    """,

    'author': "Center of Research and Development",
    'website': "https://crnd.pro",
    'version': '11.0.0.1.0',
    'category': 'Bureaucrat',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'generic_mixin',
    ],

    # always loaded
    'data': [
        'security/security.xml',
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
