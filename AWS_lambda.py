from __future__ import print_function
import boto3
import traceback
from botocore.exceptions import ClientError
import os

sns = boto3.client('sns')
support_client = boto3.client('support', region_name='us-east-1')


def lambda_handler(event, context):
    try:
        TrustedAdvisoryChecks = support_client.describe_trusted_advisor_checks(language='en')
        ResourceList = {accountTags: [] for accountTags in list(set([token['category'] for token in TrustedAdvisoryChecks['checks']]))}
        for token in TrustedAdvisoryChecks['checks']:
            try:
                test = ['hjLMh88uM8', 'iqdCTZKCUp','Z4AUBRNSmz']

                # hjLMh88uM8 ->Idle Load Balancers
                # iqdCTZKCUp ->Load Balancer Optimization
                # 7qGXsKIUw ->ELB Connection Draining
                # Z4AUBRNSmz ->Unassociated Elastic IP Addresses

                if (token['id'] in test):
                    support_client.refresh_trusted_advisor_check(checkId=token['id'])
                    print('Refreshing check: ' + token['name'])
                    Results = \
                        support_client.describe_trusted_advisor_check_summaries(checkIds=[token['id']])['summaries'][0]
                    # print ("check : {0}".format(Results))
                    ResourceList[token['category']].append([token['name'], Results['status'],
                                                            str(Results['resourcesSummary'][
                                                                    'resourcesProcessed']),
                                                            str(Results['resourcesSummary']['resourcesFlagged']),
                                                            str(Results['resourcesSummary'][
                                                                    'resourcesSuppressed']),
                                                            str(Results['resourcesSummary']['resourcesIgnored'])])
                    print("check summary {}".format(Results))
                    # print(Results['resourcesSummary']['resourcesFlagged'])

                    if (Results['status'] != 'not_available' and token['id'] == 'hjLMh88uM8' and
                            Results['resourcesSummary']['resourcesFlagged'] > 0):
                        Trigger_notification(Results, token['name'], token['id'])


                    elif (Results['status'] != 'not_available' and token['id'] == 'iqdCTZKCUp' and
                          Results['resourcesSummary']['resourcesFlagged'] > 0):
                        Trigger_notification(Results, token['name'], token['id'])


                    elif (Results['status'] != 'not_available' and token['id'] == 'Z4AUBRNSmz' and
                          Results['resourcesSummary']['resourcesFlagged'] > 0):
                        Trigger_notification(Results, token['name'], token['id'])


            except ClientError:
                print('Failed to refresh check: ' + token['name'])
                continue

    except:
        print('Operation not succeeded')
        traceback.print_exc()


def Trigger_notification(detailed_check, check_name, checks_id):
    result = support_client.describe_trusted_advisor_check_result(checkId=checks_id, language='en')
    flagResources = result['result']['flaggedResources']
    response = sns.publish(
        TopicArn=os.environ['TOPIC_ARN'],
        Subject=check_name,
        Message=str(flagResources)
    )
    print("Notification send")


if __name__ == '__main__':
    lambda_handler('event', 'handler')
