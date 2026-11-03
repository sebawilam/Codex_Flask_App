import unittest
from unittest.mock import Mock, patch

from bs4 import BeautifulSoup

from app import app


class ErrorHandlerTests(unittest.TestCase):
    def setUp(self):
        self.config_patch = patch.dict(
            app.config, TESTING=True, DEBUG=False, PROPAGATE_EXCEPTIONS=False
        )
        self.config_patch.start()
        self.addCleanup(self.config_patch.stop)
        self.client = app.test_client()

    def assert_error_page(self, response, status, title):
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.mimetype, "text/html")
        page = BeautifulSoup(response.data, "html.parser")
        self.assertEqual(page.h1.get_text(), title)
        self.assertEqual(page.select_one('a[href="/"]').get_text(), "Back to My Links")
        self.assertEqual(
            page.select_one('link[rel="stylesheet"]')["href"], "/static/style.css"
        )

    def test_unknown_url_renders_custom_404(self):
        self.assert_error_page(
            self.client.get("/missing-page"), 404, "404 — Page Not Found"
        )

    def test_missing_link_renders_custom_404(self):
        for method, path in [("get", "/edit/999999"), ("post", "/delete/999999")]:
            with self.subTest(path=path):
                self.assert_error_page(
                    getattr(self.client, method)(path), 404, "404 — Page Not Found"
                )

    def test_unhandled_exception_renders_custom_500(self):
        broken_view = Mock(side_effect=RuntimeError("Internal diagnostic detail"))
        with patch.dict(app.view_functions, index=broken_view):
            with self.assertLogs(app.logger, level="ERROR") as logs:
                response = self.client.get("/")
        self.assert_error_page(response, 500, "500 — Internal Server Error")
        self.assertNotIn(b"Internal diagnostic detail", response.data)
        self.assertTrue(any("Internal diagnostic detail" in line for line in logs.output))

    def test_successful_pages_and_other_errors_keep_their_status(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/about").status_code, 200)
        with self.client.get("/static/style.css") as response:
            self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/add").status_code, 405)
        self.assertEqual(self.client.post("/add", data={}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
