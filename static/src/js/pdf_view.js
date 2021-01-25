odoo.define('website.pdf_view', function (require) {
"use strict";

    var snippet_animation = require('website.content.snippets.animation');
    var snippet_registry = snippet_animation.registry;

    var document_view_pdf_widget = snippet_animation.Class.extend({
        selector: '#document_body_pdf',

        start: function () {
        },
        
    });

    snippet_registry.document_view_pdf_widget = document_view_pdf_widget;

    return {
        document_view_pdf_widget: document_view_pdf_widget,
    };
});
