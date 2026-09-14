import unittest
from normalization import normalize
from providers import LocalProvider


class ReportTests(unittest.TestCase):
    def test_adb_temperature_and_unknown(self):
        report={'data':{'results':{'battery':{'status':'OK','data':{'temperature_c':46}},'storage':{'status':'UNAVAILABLE'}}}}
        result=LocalProvider().analyze(normalize(report))
        self.assertEqual({alert['code'] for alert in result['alerts']},{'BATTERY_TEMPERATURE','INCOMPLETE_EVIDENCE'})
        self.assertFalse(result['data_leaves_device'])

    def test_source_alerts_deduplicated(self):
        alert={'risk':'ŚREDNIE','detected':'Fixture','what_to_check':'Sprawdź źródło'}
        metrics=normalize({'alerts':[alert,alert]})
        self.assertEqual(len(metrics['source_alerts']),1)
        self.assertEqual(LocalProvider().analyze(metrics)['risk_score'],15)

    def test_windows_disk_health_and_jitter(self):
        result=LocalProvider().analyze(normalize({'data':[{'HealthStatus':'Warning'},{'jitter_ms':150}]}))
        self.assertEqual({alert['code'] for alert in result['alerts']},{'STORAGE_HEALTH','NETWORK_JITTER'})
