import config
import main.api
import mock
import unittest


class TestApiModuleMethods(unittest.TestCase):
    """Unit tests for api module methods."""

    def setUp(self):
        pass

    @mock.patch("requests.get")
    def test_ok_response(self, requests_get_mock):
        response_mock = mock.Mock()
        response_mock.status_code = 200
        response_json_mock = mock.Mock()
        response_mock.json.return_value = response_json_mock
        requests_get_mock.return_value = response_mock
        expected_headers = {
            "Authorization": config.API_TOKEN,
            "Content-type": "application/json",
        }

        # Test with default param.
        resp = main.api.get_listed_loans()
        requests_get_mock.assert_called_with(
            config.API_URL + config.API_LOANS_URI,
            headers=expected_headers,
            params={"showAll": True},
        )
        response_mock.json.assert_called_with()
        self.assertEqual(resp, response_json_mock)

        # Test with explicit param.
        resp = main.api.get_listed_loans(show_all=False)
        requests_get_mock.assert_called_with(
            config.API_URL + config.API_LOANS_URI,
            headers=expected_headers,
            params={"showAll": False},
        )
        response_mock.json.assert_called_with()
        self.assertEqual(resp, response_json_mock)

    @mock.patch("logging.getLogger")
    @mock.patch("requests.get")
    def test_error_response(self, requests_get_mock, logging_get_mock):
        response_mock = mock.Mock()
        response_mock.status_code = 403
        response_mock.text = "{'error': 'Unauthorized'}"
        requests_get_mock.return_value = response_mock
        logger_mock = mock.Mock()
        logging_get_mock.return_value = logger_mock

        resp = main.api.get_listed_loans()
        self.assertTrue(requests_get_mock.called)
        self.assertFalse(response_mock.json.called)
        logger_mock.error.assert_called_with(response_mock.text)
        self.assertTrue(resp == None)


if __name__ == "__main__":
    unittest.main()
