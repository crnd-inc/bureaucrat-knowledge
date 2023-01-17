# flake8: noqa: E501
{
    'name': "Bureaucrat Knowledge Website",

    'summary': """
        Bureaucrat Knowledge Website
    """,

    'author': "Center of Research and Development",
    'website': "https://crnd.pro",

    'version': '16.0.0.14.0',

    'category': 'Knowledge',

    # any module necessary for this one to work correctly
    'depends': [
        'website',
        'bureaucrat_knowledge',
        'web_tour',
    ],

    # always loaded
    'data': [
        'data/website_data.xml',
        'templates/templates.xml',
        'views/bureaucrat_knowledge_category.xml',
        'views/bureaucrat_knowledge_document.xml',
    ],
    'images': ['static/description/banner.png'],
    'assets': {
        'web.assets_frontend': [
            'bureaucrat_knowledge_website/static/src/scss/knowledge_base_website.scss',
        ],
        'web.assets_tests': [
            'bureaucrat_knowledge_website/static/src/js/tours/search.js',
        ],
    },

    'demo': [
        'demo/demo_res_users.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
