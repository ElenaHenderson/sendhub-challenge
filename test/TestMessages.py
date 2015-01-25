import unittest
import requests
import json

VALID_MESSAGE = 'SendHub Rocks'
VALID_RECIPIENT = '+19255701616'
INVALID_RECIPIENT_DIGITS_1 = '+1925570161'
INVALID_RECIPIENT_DIGITS_2 = '+192557016'
INVALID_RECIPIENT_COUNTRY = '+59255701616'
INVALID_RECIPIENT_NOT_US = '+19005701616'
INVALID_RECIPIENT_TOO_LONG = '+192557016164444443333333'
INVALID_RECIPIENT_NOT_A_NUMBER = 'BBBBBBBBF'
INVALID_RECIPIENT_INVALID_COUNTRY_CODE = '925570161644444F'


class TestSuite(unittest.TestCase):

    def test_valid_recipients(self):
        message = 'SendHub Rocks'
        recipients = self.generate_valid_recipients(5001)
        self.route_messages(message, recipients)

    def test_error_messages(self):
        self.assertEquals(json.loads(self.route_messages(None, [VALID_RECIPIENT]).content)['errorMessage'],
                          'MESSAGE_PARAMETER_CAN_NOT_BE_NONE')

        self.assertEquals(json.loads(self.route_messages(VALID_MESSAGE, None).content)['errorMessage'],
                          'RECIPIENTS_PARAMETER_CAN_NOT_BE_NONE')

        self.assertEquals(json.loads(self.route_messages(VALID_MESSAGE, []).content)['errorMessage'],
                          'RECIPIENTS_PARAMETER_SHOULD_HAVE_AT_LEAST_ONE_ITEM')

        self.assertEquals(json.loads(self.route_messages(VALID_MESSAGE, 'not list').content)['errorMessage'],
                          'RECIPIENTS_PARAMETER_SHOULD_BE_LIST')

        self.assertEquals(json.loads(self.route_messages(VALID_MESSAGE, [VALID_RECIPIENT, VALID_RECIPIENT]).content)['errorMessage'],
                          'RECIPIENTS_MUST_BE_UNIQUE')

        # self.assertEquals(json.loads(self.route_messages(VALID_MESSAGE, self.generate_valid_recipients(5001)).content)['errorMessage'],
        #                   '5000_RECIPIENTS_LIMIT_IS_EXCEEDED')

        self.route_messages(VALID_MESSAGE, [INVALID_RECIPIENT_DIGITS_1,
                                            INVALID_RECIPIENT_DIGITS_2,
                                            INVALID_RECIPIENT_COUNTRY,
                                            INVALID_RECIPIENT_NOT_US,
                                            INVALID_RECIPIENT_TOO_LONG,
                                            INVALID_RECIPIENT_NOT_A_NUMBER,
                                            INVALID_RECIPIENT_INVALID_COUNTRY_CODE])

    def generate_valid_recipients(self, count):
        return ["+1617123{0:04d}".format(i) for i in range(count)]

    def route_messages(self, message, recipients):
        url = 'https://damp-coast-8375.herokuapp.com/messages'
        data = {'message': message, 'recipients': recipients}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=json.dumps(data), headers=headers)
        if message is not None and recipients is not None:
            print 'curl -v -H \"Content-Type: application/json\" -X POST -d \'{\"message\": \"' + message + \
                  '\", \"recipients\": ' + str(recipients).replace('\'', '\"') + '}\'  https://damp-coast-8375.herokuapp.com/messages'
        return response
