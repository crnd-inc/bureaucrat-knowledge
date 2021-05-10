{
    'name': "Bureaucrat Knowledge Website",

    'summary': """
        Bureaucrat Knowledge Website
    """,

    'author': "Center of Research and Development",
    'website': "https://crnd.pro",
    'version': '12.0.0.5.0',
    'category': 'Knowledge',

    # any module necessary for this one to work correctly
    'depends': [
        'website',
        'bureaucrat_knowledge',
    ],

    # always loaded
    'data': [
        'data/website_data.xml',
        'templates/templates.xml',
        'views/bureaucrat_knowledge_category.xml',
        'views/bureaucrat_knowledge_document.xml',
    ],
    'images': [],
    'demo': [],

    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
