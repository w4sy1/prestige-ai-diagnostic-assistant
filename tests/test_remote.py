import io
import json
import unittest
from unittest.mock import patch
from remote import analyze,payload


class RemoteTests(unittest.TestCase):
    def test_sensitive_source_text_not_sent(self):
        body=payload({'packet_loss':4,'source_alerts':[{'detected':'private-path-secret'}]},'test-model')
        self.assertNotIn('private-path-secret',json.dumps(body))
        self.assertFalse(body['store'])

    def test_request_and_response_without_real_api(self):
        captured=[]
        def fake(request,timeout):
            captured.append(request)
            return io.BytesIO(json.dumps({'output':[{'type':'message','content':[{'type':'output_text','text':'Sprawdź bramę.'}]}]}).encode())
        with patch.dict('os.environ',{'OPENAI_API_KEY':'fixture-not-a-real-key'}):
            result=analyze({'packet_loss':12},'test-model',fake)
        self.assertTrue(result['data_leaves_device'])
        self.assertEqual(result['analysis'],'Sprawdź bramę.')
        self.assertNotIn('fixture-not-a-real-key',json.dumps(result))
        self.assertEqual(captured[0].full_url,'https://api.openai.com/v1/responses')

    def test_missing_key_no_request(self):
        with patch.dict('os.environ',{},clear=True),self.assertRaises(ValueError):analyze({},'test-model')
