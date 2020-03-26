import re
import wget
import boto3
# from smart_open import open
import urllib.request
import sys
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# exception list
amiListUrl = "https://raw.githubusercontent.com/"
urllib.request.urlretrieve(amiListUrl, 'download.txt')
temp_upload_location = "upload.txt"
upload_location = sys.argv[1]

def main():
    try:
        with open(temp_upload_location, "w") as upload:
            with open('download.txt', 'r') as f:
                for line in f:
                    if 'ami-' in line:
                            for ami in re.findall('\w*ami-\w*', line):
                                upload.write("%s\n" % (ami))
    except:
        print("unable to get the latest ami list")
        raise SystemExit

    s3 = boto3.resource('s3')
    #try:
    print("uploading to: ", upload_location)
    s3.Bucket(upload_location).upload_file(temp_upload_location,'ami-exception-list.txt')
    print("ami list uploaded successful")
    # except:
    #     print("unable to upload to s3")
    #     raise SystemExit


main()

