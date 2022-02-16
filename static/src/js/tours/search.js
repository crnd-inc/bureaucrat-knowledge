odoo.define('bureaucrat_knowledge_website.search', function (require) {
    'use strict';

    var tour = require('web_tour.tour');

    tour.register('bureaucrat_knowledge_website_search', {
        test: true,
        url: '/',
    }, [
        {
            content: 'Navigate to knowledge base page',
            trigger: "a[href='/knowledge']",
        },

        {
            content: "Fill search text 'Generic' in searchbar",
            trigger: "#wsd-knowledge-search input",
            run: "text Generic Assignment HR",
        },
        {
            content: "Click on 'search' button",
            trigger: "#wsd-knowledge-search-after button[type='submit']",
        },
        {
            content: "Wait for loading",
            trigger: "#wrapwrap",
        },
        {
            content: "Check that specific article was found",
            trigger: "a:containsExact('Generic Assignment HR')",
        },
        {
            content: 'Waiting for result',
            trigger: "#genenric-assignment-hr",
        },
        {
            content: "Navigate back to root of knowledge base",
            trigger: ".breadcrumb-item a[href='/knowledge/']",
        },
        {
            content: "Try to search for unexisting article",
            trigger: "#wsd-knowledge-search input",
            run: "text There are no documents must be found",
        },
        {
            content: "Click on 'search' button",
            trigger: "#wsd-knowledge-search-after button[type='submit']",
        },
        {
            content: "Check that nothing finded",
            trigger: "h3:containsExact('There are no matching documents.')",
        },
    ]);
    return {};
});
