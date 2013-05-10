# -*- coding: utf-8 -*-
"""
Timestamps should be Coordinated Universal Time (UTC).
"""
import json
from pprint import pprint

test_result = {
    'description': "Description of the test run. Reason for it's execution.",
    'environment': {
        'Hardware': [
            {
                'type': 'PC',
                # 'name':
                # 'version':
                # 'address':
            }
        ],
        'Software': [
            {
                'type': 'os',
                'name': 'Windows 7 Ultimate',
                'version': '6.7',
                'architecture': 64
            }
        ]
    },
    'sequences': [
        {
            'name': 'TestSequence...',
            'status': 'Failed',
            'log': [
                {
                    'timestamp': 'YYYY-MM-DD HH:MM:SS',
                    'severity': 0,
                    'message': "This is a log message."
                },
                {
                    'timestamp': 'YYYY-MM-DD HH:MM:SS',
                    'severity': 1,
                    'message': "This is a log message with an error."
                },
            ]
        },
        {
            'name': 'AnotherTestSequence',
            'status': 'Passed',
            'log': [
                {
                    'timestamp': 'YYYY-MM-DD HH:MM:SS',
                    'severity': 0,
                    'message': "This is a log message."
                },
                {
                    'timestamp': 'YYYY-MM-DD HH:MM:SS',
                    'severity': 1,
                    'message': "This is a log message with an error."
                },
            ]
        }
    ]
}

# pprint(test_result)

print json.dumps(test_result, indent=4)
