import unittest
from datetime import datetime, timezone
from tempfile import TemporaryDirectory
from pathlib import Path
import monitor

class MonitorTests(unittest.TestCase):
    def test_dates(self):
        self.assertEqual(monitor.dateparse('2026-10-28T10:00:00Z').tzinfo,timezone.utc)
        self.assertIsNone(monitor.dateparse('invalid'))
    def test_locations(self):
        self.assertTrue(monitor.STATES.search('Remote, United States'))
        self.assertTrue(monitor.STATE_CODES.search('Atlanta, GA'))
        self.assertFalse(bool(monitor.STATES.search('Toronto, Canada')))
    def test_roles(self):
        self.assertTrue(monitor.ROLE.search('Quality Assurance Specialist'))
        self.assertTrue(monitor.ROLE.search('Senior QA Specialist'))
        self.assertTrue(monitor.EXCLUDE.search('Software QA Specialist'))
        self.assertFalse(monitor.EXCLUDE.search('Senior Quality Assurance Specialist'))
    def test_state_schema(self):
        with TemporaryDirectory() as temp:
            old=monitor.DB
            try:
                monitor.DB=str(Path(temp)/'jobs.sqlite3')
                db=monitor.connect()
                self.assertEqual(db.execute("SELECT count(*) FROM metadata").fetchone()[0],0)
                db.close()
            finally:
                monitor.DB=old

if __name__=='__main__': unittest.main()
