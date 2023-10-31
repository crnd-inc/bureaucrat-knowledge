{
    'name': "Bureaucrat Knowledge Related Documents",

    'summary': """
        Bureaucrat Knowledge Related Documents
    """,

    'author': "Center of Research and Development",
    'website': "https://crnd.pro",
    'version': '12.0.0.4.0',
    'category': 'Knowledge',

    # any module necessary for this one to work correctly
    'depends': [
        'bureaucrat_knowledge',
    ],

    # always loaded
    'data': [
        'views/bureaucrat_knowledge_document.xml',

        'wizard/related_documents_change_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'demo': [],

    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
