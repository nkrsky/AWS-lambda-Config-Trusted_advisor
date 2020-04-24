from __future__ import print_function
import boto3
import traceback
from botocore.exceptions import ClientError
import os

sns = boto3.client('sns')
support_client = boto3.client('support', region_name='us-east-1')


def lambda_handler(event, context):
    try:

        ta_checks = support_client.describe_trusted_advisor_checks(language='en')
        checks_list = {ctgs: [] for ctgs in list(set([checks['category'] for checks in ta_checks['checks']]))}
        for checks in ta_checks['checks']:
            try:
                test = ['hjLMh88uM8', 'iqdCTZKCUp', '7qGXsKIUw']

                if (checks['id'] in test):
                    support_client.refresh_trusted_advisor_check(checkId=checks['id'])
                    print('Refreshing check: ' + checks['name'])
                    check_summary = \
                        support_client.describe_trusted_advisor_check_summaries(checkIds=[checks['id']])['summaries'][0]
                    # print ("check : {0}".format(check_summary))
                    checks_list[checks['category']].append([checks['name'], check_summary['status'],
                                                            str(check_summary['resourcesSummary'][
                                                                    'resourcesProcessed']),
                                                            str(check_summary['resourcesSummary']['resourcesFlagged']),
                                                            str(check_summary['resourcesSummary'][
                                                                    'resourcesSuppressed']),
                                                            str(check_summary['resourcesSummary']['resourcesIgnored'])])
                    print("check summary {}".format(check_summary))
                    # print(check_summary['resourcesSummary']['resourcesFlagged'])

                    if (check_summary['status'] != 'not_available' and checks['id'] == 'hjLMh88uM8' and
                            check_summary['resourcesSummary']['resourcesFlagged'] == 0):
                        Trigger_notification(check_summary, checks['name'], checks['id'])


                    elif (check_summary['status'] != 'not_available' and checks['id'] == 'iqdCTZKCUp' and
                          check_summary['resourcesSummary']['resourcesFlagged'] > 0):
                        Trigger_notification(check_summary, checks['name'], checks['id'])


                    elif (check_summary['status'] != 'not_available' and checks['id'] == '7qGXsKIUw' and
                          check_summary['resourcesSummary']['resourcesFlagged'] > 0):
                        Trigger_notification(check_summary, checks['name'], checks['id'])


            except ClientError:
                print('Cannot refresh check: ' + checks['name'])
                continue

    except:
        print('Failed! Debug further.')
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
