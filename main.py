import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import boto3
import StringIO

debug = False


def main():
    # Main function used for debugging
    global debug
    event = context = {}
    debug = True
    lambda_handler(event, context)


def lambda_handler(event, context):
    global config

    # Load the configuration (s3_bucket, s3_key, sheet_id)
    with open('config.json') as data_file:
        config = json.load(data_file)

    # Connect to Google Sheets and open the sheet
    # Ensure the sheet is shared with the service
    # account email address (user@project.iam.gserviceaccount.com)
    scopes = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scopes=scopes)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key(config['sheet_id']).worksheet(config['worksheet_name'])

    # Get the values
    gval = sheet.range("A1:B" + str(sheet.row_count))
    data = {}

    # Get every key => value for A => B (If A is not blank)
    for i in range(sheet.row_count):
        if i % 2 == 0 and gval[i].value != '':
            data[gval[i].value] = str(gval[i + 1].value)

    # Encode into JSON
    jsonstr = json.dumps(data)

    # Print or upload to S3
    if debug:
        print jsonstr
    else:
        return upload_to_s3(jsonstr)

    return


def upload_to_s3(data):
    try:
        s3 = boto3.client('s3')
        s3r = boto3.resource('s3')

        # Upload
        s3r.Bucket(config['s3_bucket']).Object(config['s3_key']).put(Body=data)
        s3.put_object_acl(ACL='public-read', Bucket=config['s3_bucket'], Key=config['s3_key'])
        print "File uploaded to {}, key {}.".format(config['s3_bucket'], config['s3_key'])

        return 0

    except Exception as e:
        raise Exception(e)
        return -1


if __name__ == '__main__':
    main()