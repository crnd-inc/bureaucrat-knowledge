odoo.define('bureaucrat_knowledge_website.search', function (require) {
    'use strict';

    var tour = require('web_tour.tour');

    tour.register('bureaucrat_knowledge_website_search', {
        test: true,
        url: '/knowledge',
    }, [
        {
            content: "Search",
            trigger: "form#wsd-knowledge-search input[name='search']",
            run: "text Generic",
        },
        {
            content: "Click on 'search' button",
            trigger: ".btn.btn-outline-secondary",
        },
    ]);
    return {};
});
