from unittest.mock import MagicMock
from senza.aws import resolve_topic_arn
import boto.ec2
from senza.aws import get_security_group, resolve_security_groups

def test_resolve_security_groups(monkeypatch):
    ec2 = MagicMock()
    sg = boto.ec2.securitygroup.SecurityGroup(name='app-test', id='sg-test')
    ec2.get_all_security_groups.return_value = [sg]
    monkeypatch.setattr('boto.ec2.connect_to_region', MagicMock(return_value=ec2))

    security_groups = []
    security_groups.append({'Fn::GetAtt': ['RefSecGroup', 'GroupId']})
    security_groups.append('sg-007')
    security_groups.append('app-test')

    result = []
    result.append({'Fn::GetAtt': ['RefSecGroup', 'GroupId']})
    result.append('sg-007')
    result.append('sg-test')

    assert result == resolve_security_groups(security_groups, 'myregion')

def test_create(monkeypatch):
    sns = MagicMock()
    topic = {'TopicArn': 'arn:123:mytopic'}
    sns.get_all_topics.return_value = {'ListTopicsResponse': {'ListTopicsResult': {'Topics': [topic]}}}
    monkeypatch.setattr('boto.sns.connect_to_region', MagicMock(return_value=sns))

    assert 'arn:123:mytopic' == resolve_topic_arn('myregion', 'mytopic')
