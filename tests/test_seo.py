import unittest

from app import create_app


class SeoResponseTests(unittest.TestCase):
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
        self.assertNotIn('www.cardbranch.co.uk', xml)
        self.assertNotIn('/c/', xml)

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
