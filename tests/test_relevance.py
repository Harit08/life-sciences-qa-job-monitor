import unittest
from matching import assess, us_eligible, target_title


class RelevanceTests(unittest.TestCase):
    def test_entry_and_senior_specialists_are_included(self):
        for title, description in (
            ("Quality Assurance Specialist I", "Biopharmaceutical GMP batch records. 0–2 years of experience."),
            ("Senior Quality Assurance Specialist", "Medical devices, CAPA. 8+ years of experience."),
            ("Sr. QA Specialist", "Biotech quality systems. 10 years of experience."),
            ("Specialist II, Quality Assurance", "Cell therapy manufacturing and batch release."),
            ("QA, Shop Floor Specialist II", "GMP biologics manufacturing oversight."),
            ("Senior Quality Systems Specialist", "ISO 13485, document control and audit support."),
            ("Quality Assurance Associate", "Pharmaceutical batch review."),
        ):
            with self.subTest(title=title):
                self.assertTrue(assess(title, description)[0])

    def test_unrelated_and_management_roles_are_excluded(self):
        for title, description in (
            ("Data Engineer", "GMP pharmaceutical data and Python"),
            ("Software QA Specialist", "Medical devices software testing"),
            ("QA Automation Specialist", "Biotech Selenium and Cypress tests"),
            ("Quality Assurance Manager", "GMP pharma"),
            ("Quality Assurance Intern", "GMP biotech"),
            ("Food Quality Assurance Specialist", "GMP food manufacturing"),
            ("QA Specialist", "Test web apps using Selenium, AWS and GCP. Medical insurance."),
            ("Marketing Specialist", "We sell pharmaceutical products"),
        ):
            with self.subTest(title=title):
                self.assertFalse(assess(title, description)[0])

    def test_title_prescreen_does_not_require_description(self):
        self.assertTrue(target_title("Specialist, Quality Assurance"))
        self.assertFalse(target_title("Software QA Specialist"))

    def test_pharma_client_boilerplate_does_not_make_call_center_qa_relevant(self):
        description = ("We provide software services to pharmaceutical brands. "
                       "Maintain call center quality standards. Evaluate recorded calls "
                       "and monitor customer service performance. 1 year of experience.")
        self.assertFalse(assess("Quality Assurance Specialist - Remote", description)[0])

    def test_missing_years_do_not_exclude(self):
        accepted, _, reasons = assess("QA Specialist", "GMP batch release and CAPA.")
        self.assertTrue(accepted)
        self.assertIn("experience not specified", reasons)

    def test_sponsorship_text_is_not_filtered(self):
        for text in ("H-1B sponsorship is available.", "We cannot provide visa sponsorship.",
                     "Must have US work authorization.", ""):
            with self.subTest(text=text):
                self.assertTrue(assess("Quality Assurance Specialist", "GMP biotech. " + text)[0])

    def test_years_do_not_change_relevance_priority(self):
        junior = assess("Quality Assurance Specialist", "GMP. 1 year of experience.")
        senior = assess("Quality Assurance Specialist", "GMP. 8 years of experience.")
        self.assertTrue(junior[0] and senior[0])
        self.assertEqual(junior[1], senior[1])
        self.assertIn("experience: entry level", junior[2])
        self.assertIn("experience: senior specialist", senior[2])

    def test_us_locations_and_work_styles(self):
        for location, country in (
            ("On-site, Boston, MA", None), ("Hybrid, Newark, NJ", None),
            ("Remote, United States", None), ("Remote", "US"),
            ("Remote worldwide", None), ("South Dakota", None), ("Boise, ID", None),
        ):
            with self.subTest(location=location):
                self.assertTrue(us_eligible(location, country))
        for location, country in (
            ("Toronto, Canada", "CA"), ("Remote, Canada", None),
            ("Remote", None), ("North America", None), ("London", "GB"),
        ):
            with self.subTest(location=location):
                self.assertFalse(us_eligible(location, country))


if __name__ == "__main__":
    unittest.main()
