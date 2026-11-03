import unittest
from copy import deepcopy
from unittest.mock import Mock, patch

import requests
from bs4 import BeautifulSoup

from app import DEFAULT_METADATA, LINKS, app


class LinkMetadataTests(unittest.TestCase):
    def setUp(self):
        self.original_links = deepcopy(LINKS)
        self.client = app.test_client()
        self.request_patch = patch("app.requests.get")
        self.get = self.request_patch.start()
        self.response = Mock()
        self.response.content = b"""
            <meta property="og:title" content=" Example &amp; title ">
            <meta property="og:description" content="A useful description">
            <meta property="og:image" content="https://example.com/image.jpg">
        """
        self.get.return_value = self.response

    def tearDown(self):
        self.request_patch.stop()
        LINKS[:] = self.original_links

    def add_link(self):
        return self.client.post(
            "/add", data={"name": "Example", "url": "https://example.com/"}
        )

    def test_add_fetches_stores_and_displays_open_graph_metadata(self):
        response = self.add_link()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/")
        self.get.assert_called_once_with("https://example.com/", timeout=10)
        self.response.raise_for_status.assert_called_once()
        self.assertEqual(LINKS[-1]["title"], "Example & title")
        self.assertEqual(LINKS[-1]["description"], "A useful description")
        self.assertEqual(LINKS[-1]["image_url"], "https://example.com/image.jpg")
        page = BeautifulSoup(self.client.get("/").data, "html.parser")
        card = page.select("li")[-1]
        self.assertEqual(card.img["src"], "https://example.com/image.jpg")
        self.assertEqual(card.h2.get_text(), "Example & title")
        self.assertEqual(card.p.get_text(), "A useful description")
        self.assertEqual(card.select("a")[-1]["href"], "https://example.com/")
        self.assertEqual(card.select("a")[-1].get_text(), "https://example.com/")
        self.get.assert_called_once()

    def test_cards_without_metadata_keep_static_fallbacks(self):
        page = BeautifulSoup(self.client.get("/").data, "html.parser")
        for card in page.select("li"):
            self.assertIsNone(card.img)
            self.assertEqual(
                [heading.get_text() for heading in card.select("dt")],
                ["Title", "Description", "Image URL"],
            )
            self.assertEqual(
                [value.get_text() for value in card.select("dd")],
                ["Not Available"] * 3,
            )
            self.assertTrue(card.select_one('a[aria-label^="Edit "]'))
            self.assertTrue(card.select_one('form[method="post"]'))

    def test_partial_metadata_shows_available_values_and_static_fallbacks(self):
        for field, value in [
            ("title", "Only a title"),
            ("description", "Only a description"),
            ("image_url", "https://example.com/only-image.jpg"),
        ]:
            with self.subTest(field=field):
                LINKS[:] = [{"name": "Example", "url": "https://example.com/", **DEFAULT_METADATA, field: value}]
                card = BeautifulSoup(self.client.get("/").data, "html.parser").li
                self.assertEqual(card.h2.get_text(), value if field == "title" else "Not Available")
                self.assertEqual(card.p.get_text(), value if field == "description" else "Not Available")
                if field == "image_url":
                    self.assertEqual(card.img["src"], value)
                else:
                    self.assertIsNone(card.img)
                    self.assertIn("Image URL: Not Available", card.get_text())

    def test_missing_empty_and_contentless_tags_use_fallback(self):
        for html in [
            b"<title>Not an Open Graph title</title>",
            b'<meta property="og:title" content="   ">',
            b'<meta property="og:description">',
        ]:
            with self.subTest(html=html):
                self.response.content = html
                self.assertEqual(self.add_link().status_code, 302)
                for field, fallback in DEFAULT_METADATA.items():
                    self.assertEqual(LINKS[-1][field], fallback)

    def test_one_missing_tag_does_not_discard_other_values(self):
        self.response.content = b'<meta property="og:title" content="Present">'
        self.add_link()
        self.assertEqual(LINKS[-1]["title"], "Present")
        self.assertEqual(LINKS[-1]["description"], "Not Available")
        self.assertEqual(LINKS[-1]["image_url"], "Not Available")

    def test_request_failures_still_store_link_with_fallbacks(self):
        for error in [requests.Timeout(), requests.ConnectionError(), requests.HTTPError()]:
            with self.subTest(error=type(error).__name__):
                self.get.side_effect = error
                self.assertEqual(self.add_link().status_code, 302)
                for field, fallback in DEFAULT_METADATA.items():
                    self.assertEqual(LINKS[-1][field], fallback)
        self.get.side_effect = None
        self.response.raise_for_status.side_effect = requests.HTTPError()
        self.assertEqual(self.add_link().status_code, 302)
        self.assertEqual(LINKS[-1]["title"], "Not Available")

    def test_metadata_is_escaped_in_cards(self):
        self.response.content = b'<meta property="og:title" content="&lt;script&gt;alert(1)&lt;/script&gt;">'
        self.add_link()
        page = self.client.get("/").data
        self.assertIn(b"&lt;script&gt;alert(1)&lt;/script&gt;", page)
        self.assertNotIn(b"<script>", page)

    def test_edit_preserves_metadata_for_rename_and_refreshes_changed_url(self):
        self.add_link()
        index = len(LINKS) - 1
        self.get.reset_mock()
        page = BeautifulSoup(self.client.get(f"/edit/{index}").data, "html.parser")
        self.assertEqual(page.select_one('[name="name"]')["value"], "Example")
        response = self.client.post(
            f"/edit/{index}",
            data={"name": "Renamed", "url": "https://example.com/"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LINKS[index]["name"], "Renamed")
        self.assertEqual(LINKS[index]["title"], "Example & title")
        self.get.assert_not_called()
        self.response.content = b'<meta property="og:title" content="New page">'
        response = self.client.post(
            f"/edit/{index}",
            data={"name": "Renamed", "url": "https://example.org/"},
        )
        self.assertEqual(response.headers["Location"], "/")
        self.get.assert_called_once_with("https://example.org/", timeout=10)
        self.assertEqual(LINKS[index]["title"], "New page")
        self.assertEqual(LINKS[index]["image_url"], "Not Available")

    def test_delete_removes_metadata_and_homepage_renders_examples(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.get.assert_not_called()
        self.add_link()
        index = len(LINKS) - 1
        response = self.client.post(f"/delete/{index}")
        self.assertEqual(response.headers["Location"], "/")
        self.assertEqual(LINKS, self.original_links)

    def test_invalid_forms_do_not_fetch_or_store(self):
        for data in [{"name": "", "url": "https://example.com/"}, {"name": "Missing URL"}]:
            with self.subTest(data=data):
                self.assertEqual(self.client.post("/add", data=data).status_code, 400)
        self.get.assert_not_called()
        self.assertEqual(LINKS, self.original_links)


if __name__ == "__main__":
    unittest.main()
