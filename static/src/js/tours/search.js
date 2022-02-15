odoo.define('bureaucrat_knowledge_website.search', function (require) {
    'use strict';

    var tour = require('web_tour.tour');

    tour.register('bureaucrat_knowledge_website_search', {
        test: true,
        url: '/',
    }, [
        {
            content: 'Navigate to knowledge base page',
            trigger: "#top_menu > li:nth-child(3) > a > span",
        },

        {
            content: "Fill search text 'Generic' in searchbar",
            trigger: "form#wsd-knowledge-search input[name='search']",
            run: "text Generic",
        },
        {
            content: "Click on 'search' button",
            trigger: ".btn.btn-outline-secondary",
        },
        {
            content: "Check that specific article was found",
            trigger: ".child_doc" +
                " [data-oe-model='bureaucrat.knowledge.document']",
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
            trigger: "form#wsd-knowledge-search input[name='search']",
            run: "text There are no documents must be found",
        },
        {
            content: "Click on 'search' button",
            trigger: ".btn.btn-outline-secondary",
        },
    ]);
    return {};
});
