import unittest
from unittest.mock import patch
import monitor


class SmartRecruitersTests(unittest.TestCase):
    def detail(self):
        return {
            "id": "qa1", "name": "Senior Quality Assurance Specialist",
            "location": {"city": "Boston", "region": "Massachusetts", "country": "us"},
            "applyUrl": "https://jobs.smartrecruiters.com/Example/qa1-specialist",
            "releasedDate": "2026-11-24T10:00:00Z",
            "jobAd": {"sections": {
                "jobDescription": {"text": "<p>GMP batch records and pharmaceutical quality.</p>"},
                "qualifications": {"text": "<p>8 years of experience</p>"},
            }},
        }

    def test_detail_job_description_and_dedup_across_queries(self):
        listing = {"content": [{"id": "qa1", "name": "Senior Quality Assurance Specialist"}]}
        with patch.object(monitor, "get", side_effect=[listing, self.detail(), listing]) as mocked:
            jobs = list(monitor.fetch({"ats": "smartrecruiters", "slug": "Example", "company": "Example"}))
        self.assertEqual(len(jobs), 1)
        self.assertIn("batch records", jobs[0]["description"])
        self.assertTrue(monitor.eligible(jobs[0]))
        self.assertEqual(mocked.call_count, 3)
        self.assertEqual(mocked.call_args_list[0].args[1]["country"], "us")
        self.assertEqual(mocked.call_args_list[0].args[1]["q"], "quality")

    def test_qa_jobs_beyond_first_200_are_fetched(self):
        other = {"content": [{"id": str(i), "name": "Scientist"} for i in range(100)]}
        listing = {"content": [{"id": "qa1", "name": "Senior Quality Assurance Specialist"}]}
        with patch.dict(monitor.PROFILE, {"smartrecruiters_queries": ["quality"]}):
            with patch.object(monitor, "get", side_effect=[other, other, listing, self.detail()]) as mocked:
                jobs = list(monitor.fetch({"ats": "smartrecruiters", "slug": "Example", "company": "Example"}))
        self.assertEqual(len(jobs), 1)
        self.assertEqual(mocked.call_args_list[2].args[1]["offset"], 200)


if __name__ == "__main__":
    unittest.main()
