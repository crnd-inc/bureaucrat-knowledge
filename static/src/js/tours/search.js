odoo.define('bureaucrat_knowledge_website.search', function (require) {
    'use strict';

    var tour = require('web_tour.tour');

    tour.register('bureaucrat_knowledge_website_search', {
        test: true,
        url: '/knowledge',
    }, [
        {
            content: "Search for 'generic'",
            trigger: "#wsd-knowledge-search" +
                "input[name='search']",
            run:     "generic",
        },
        {
            content: "Click on 'search' button",
            trigger: "#wsd-knowledge-search-after" +
                "button[type='submit']",
        },
    ]);
    return {};
});
