import json
import oss2
import requests
import functools
from retrying import retry
import os

packagerepositoryRequestHeaders = {
    'Authorization': os.getenv('Authorization')
}
@retry(stop_max_attempt_number=5, wait_random_min=200, wait_random_max=2000)
def downloadOSSFile(bucket, OSSKey, localPath, keepFileName=True):
    if bucket.object_exists(OSSKey):
        imgName = OSSKey.split('/')[-1]
        print(' Downloading oss file: {}'.format(OSSKey))
        if keepFileName:
            targetPath = os.path.normpath(os.path.join(localPath, imgName)).replace(os.sep, '/')
        else:
            targetPath = localPath
        bucket.get_object_to_file(OSSKey, targetPath)


@retry(stop_max_attempt_number=5, wait_random_min=200, wait_random_max=2000)
def upload_file_2_oss(bucket, oss_key, local_file_path):
    bucket.put_object_from_file(oss_key, local_file_path)


@functools.lru_cache(maxsize=6)
def getBucketConfigure(bucketStr):
    url = os.getenv('GET_BUCKET_URL') + bucketStr
    try:
        result = requests.get(url, headers=packagerepositoryRequestHeaders)
        contentJson = json.loads(result.content.decode('utf8'))
        # print("code=" + str(contentJson['code']))
    except Exception as e:
        print(e)
        return None

    if contentJson['state'] != 200:
        return None

    return contentJson['payload']


@functools.lru_cache(maxsize=6)
def getBucketByPackagerepository(bucketStr):
    bucketConfig = getBucketConfigure(bucketStr)
    if bucketConfig is None:
        return None
    bucket = get_bucket_instance_v2(bucketStr, bucketConfig['accessKey'], bucketConfig['accessSecret'],
                                    bucketConfig['endPoint'])
    return bucket


def get_bucket_instance_v2(bucketID, access_key_id, access_key_secret, endpoint):
    return oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucketID, enable_crc=False)


def get_ossKey_of_whole_dir(bucket, oss_dir):
    res = []
    for obj in oss2.ObjectIterator(bucket, prefix=oss_dir):
        res.append(obj.key)
    return res


def copy_obj_between_ossKeys(dest_bucket, src_bucket_name, src_object_name, dest_object_name):
    dest_bucket.copy_object(src_bucket_name, src_object_name, dest_object_name)