import os
from pathlib import Path
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError


# from boto3 import client
class S3Client:
    def __init__(
        self,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_session_token=None,
        region_name=None,
        botocore_session=None,
        profile_name=None,
    ):
        sess = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name,
            botocore_session=botocore_session,
            profile_name=profile_name,
        )
        self.client = sess.client("s3")

    def list_bucket(self):
        response = self.client.list_buckets()
        return [bucket["Name"] for bucket in response["Buckets"]]

    def list_objects(self, bucket, prefix):
        res = self.client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
        )
        return [r["Key"] for r in res["Contents"]]

    def upload_file(self, bucket, src, dest):
        try:
            response = self.client.upload_file(src, bucket, dest)
        except ClientError as e:
            print(e)
            return False
        return True

    def download_file(self, bucket, src, dest, replace=False):
        if os.path.exists(dest) and not replace:
            raise ValueError(f"File: '{dest}' already, set `replace=True` if you want to replace it.")
        with open(dest, "wb") as f:
            self.client.download_fileobj(bucket, src, f)
        return dest

    def download_from_uri(self, uri: str, replace=False) -> str:
        """_summary_

        Args:
            uri (str): s3 uri for the file.
            replace (bool, optional): if file already exist in file system, set True will replace the file, False will raise ValueError.

        Returns:
            str: the download filename.
        """
        parse = urlparse(uri)
        scheme, netloc = parse.scheme, parse.netloc
        assert scheme == "s3", f"Incorrect scheme: {scheme}"
        assert netloc, f"Netloc (bucket name) is empty from given uri {uri}"
        target_filename = Path(parse.path).parts[-1]
        dest = self.download_file(bucket=netloc, src=parse.path.lstrip("/"), dest=target_filename, replace=replace)
        return dest

    def upload_to_s3_destination(self, filename: str, dest_uri: str) -> str:
        """Upload file to a s3 URI.

        Args:
            filename (str): file you want to upload
            dest_uri (str): the target s3 uri you upload to (the file uri, not folder uri you want to upload to.)

        Returns:
            str: dest uri.
        """
        parse = urlparse(dest_uri)
        scheme, netloc = parse.scheme, parse.netloc
        assert scheme == "s3", f"Incorrect scheme: {scheme}"
        assert netloc, f"Netloc (bucket name) is empty from given uri {dest_uri}"

        self.upload_file(bucket=netloc, src=filename, dest=parse.path.strip("/"))
        return dest_uri
