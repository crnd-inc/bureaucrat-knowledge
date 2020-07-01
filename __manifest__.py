{
    'name': "Bureaucrat Knowledge Website",

    'summary': """
        Bureaucrat Knowledge Website
    """,

    'author': "Center of Research and Development",
    'website': "https://crnd.pro",
    'version': '11.0.0.1.0',
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
    ],
    'images': [],
    'demo': [],

    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
