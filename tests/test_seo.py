import json
import re
import unittest

from app import create_app


class SeoResponseTests(unittest.TestCase):
    landing_pages = {
        '/qr-business-cards-uk': 'QR code business cards that stay useful after printing',
        '/digital-business-card-uk': 'A digital business card without another monthly subscription',
        '/business-cards-for-tradespeople': 'Business cards built for the way tradespeople get referred',
    }

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('Debug')
        cls.client = cls.app.test_client()

    def test_homepage_uses_root_domain_as_canonical(self):
        response = self.client.get('/', base_url='https://www.cardbranch.co.uk')
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<link rel="canonical" href="https://cardbranch.co.uk/">', html
        )
        self.assertIn(
            '<meta property="og:url" content="https://cardbranch.co.uk/">', html
        )
        self.assertIn('<meta name="robots" content="index, follow">', html)

    def test_robots_advertises_root_domain_sitemap(self):
        response = self.client.get('/robots.txt')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/plain')
        self.assertIn(
            'Sitemap: https://cardbranch.co.uk/sitemap.xml',
            response.get_data(as_text=True),
        )
        self.assertNotIn('www.cardbranch.co.uk', response.get_data(as_text=True))

    def test_sitemap_only_contains_indexable_marketing_pages(self):
        response = self.client.get('/sitemap.xml')
        xml = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/xml')
        self.assertIn('<loc>https://cardbranch.co.uk/</loc>', xml)
        self.assertIn('<loc>https://cardbranch.co.uk/contact</loc>', xml)
        for path in self.landing_pages:
            self.assertIn(f'<loc>https://cardbranch.co.uk{path}</loc>', xml)
        self.assertNotIn('www.cardbranch.co.uk', xml)
        self.assertNotIn('/c/', xml)

    def test_landing_pages_are_unique_indexable_and_structured(self):
        titles = set()

        for path, heading in self.landing_pages.items():
            with self.subTest(path=path):
                response = self.client.get(path)
                html = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)
                self.assertIn(
                    f'<link rel="canonical" href="https://cardbranch.co.uk{path}">',
                    html,
                )
                self.assertIn('<meta name="robots" content="index, follow">', html)
                self.assertIn(heading, html)

                title = re.search(r'<title>(.*?)</title>', html, re.DOTALL).group(1)
                self.assertNotIn(title, titles)
                titles.add(title)

                structured = re.search(
                    r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
                    html,
                    re.DOTALL,
                ).group(1)
                payload = json.loads(structured)
                self.assertEqual(payload['@graph'][0]['url'], f'https://cardbranch.co.uk{path}')
                self.assertEqual(len(payload['@graph'][1]['mainEntity']), 4)

    def test_homepage_links_to_each_landing_page(self):
        html = self.client.get('/').get_data(as_text=True)

        for path in self.landing_pages:
            self.assertIn(f'href="{path}"', html)

    def test_auth_pages_are_not_indexable(self):
        for path in ('/login', '/register'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIn(
                    '<meta name="robots" content="noindex, nofollow">',
                    response.get_data(as_text=True),
                )


if __name__ == '__main__':
    unittest.main()
