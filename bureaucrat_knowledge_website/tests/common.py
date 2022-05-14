from odoo.tests import HttpCase


class TestPhantomTour(HttpCase):
    def _test_phantom_tour(self, start_url, tour_name, **kw):
        """ Wrapper to run web tours
        """
        tour_service = "odoo.__DEBUG__.services['web_tour.tour']"
        js_run_tour = tour_service + ".run('%s')"
        js_tours_tour = tour_service + ".tours.%s.ready"
        self.browser_js(
            url_path=start_url,
            code=js_run_tour % tour_name,
            ready=js_tours_tour % tour_name,
            **kw)
