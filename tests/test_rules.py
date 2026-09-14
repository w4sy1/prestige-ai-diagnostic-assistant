import unittest
from normalization import normalize
from providers import LocalProvider

class RuleTests(unittest.TestCase):
    def test_example(self):
        report=LocalProvider().analyze(normalize({'disk_free_percent':4,'packet_loss':8,'defender_enabled':True,'critical_errors':3}))
        self.assertEqual(len(report['alerts']),3);self.assertFalse(report['data_leaves_device'])
    def test_windows(self):self.assertEqual(normalize({'results':[{'data':[{'FreePercent':4},{'FreePercent':20}]}]})['disk_free_percent'],4)
    def test_bad_percent(self):
        with self.assertRaises(ValueError):normalize({'packet_loss':120})
    def test_bool_string(self):
        with self.assertRaises(ValueError):normalize({'defender_enabled':'false'})
    def test_empty(self):self.assertEqual(LocalProvider().analyze(normalize({}))['metrics'],{})
