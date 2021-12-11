"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import os
import mimetypes

config = pulumi.Config()
# siteDir = New Variable made by:
# pulumi config set this-project:siteDir www
site_dir = config.require("siteDir") 

bucket = aws.s3.Bucket("pulumi-bucket",
    website={
        "index_document": "index.html"
    })

for file in os.listdir(site_dir):
    filepath = os.path.join(site_dir, file)
    mime_type = mimetypes.guess_type(filepath)
    obj = aws.s3.BucketObject(file,
        bucket=bucket.bucket,
        source=pulumi.FileAsset(filepath),
        acl="public-read",
        content_type=mime_type[0] # mime_type is a dictionary; mime type is of key[1]
        )

# Export=Output the name of the bucket
# (bash) pulumi stack output bucket_name -> bucket name 
pulumi.export('bucket_name', bucket.bucket)
pulumi.export('bucket_endpoint', pulumi.Output.concat("http://", bucket.website_endpoint))