from azure.storage.blob import ContainerClient
import rasterio
from io import BytesIO
import configparser


def read_isohypsen(container_client, blob_names, level, date):
    # find all blobs that start with date and end with '{}cm.cpg'.format(level) or '{}cm.dbf'.format(level) or '{}cm.shp'.format(level) or '{}cm.shx'.format(level)
    relevant_blob_names = [blob_name for blob_name in blob_names if blob_name.endswith('{}cm.zip'.format(level))]

    # check if the date exists
    blob_names_to_read = [
        blob_name for blob_name in relevant_blob_names if date in blob_name]
    if len(blob_names_to_read) == 0:
        raise ValueError('Date {} does not exist'.format(date))
    # read the blobs
    isohypsen = {}
    for blob_name in blob_names_to_read:
        blob_client = container_client.get_blob_client(blob_name)
        blob = blob_client.download_blob().readall()
        isohypsen[blob_name] = blob

    return isohypsen


def read_raster(container_client, blob_names, raster_type, date):
    relevant_blob_names = [blob_name for blob_name in blob_names if blob_name.endswith(
        '{}.tif'.format(raster_type))]
    # check if the date exists
    try:
        blob_name_to_read = [
            blob_name for blob_name in relevant_blob_names if date in blob_name][0]
    except IndexError:
        raise ValueError('Date {} does not exist'.format(date))
    blob_client = container_client.get_blob_client(blob_name_to_read)
    raster_blob = blob_client.download_blob().readall()

    with rasterio.open(BytesIO(raster_blob)) as src:
        raster = src.read(1)
        meta = src.meta

    return raster, meta


def main(sas_url):
    # raster_types are: NAP (relative to NAP), MV (relative to 'maaiveld'), CAT (categorical (very_dry->very_wet))]
    raster_type = 'CAT'
    date = '20230430'  # date in the format 'YYYYMMDD'

    # the sas_url is the url to the container, not the blob itself. List all blobs in the container
    container_client = ContainerClient.from_container_url(sas_url)
    blob_list = container_client.list_blobs()
    blob_names = [blob.name for blob in blob_list]

    raster, meta = read_raster(container_client, blob_names, raster_type, date)

    print(raster.shape)
    print(meta)

    level = 100  # level in cm (100 or 25)
    isohypsen = read_isohypsen(container_client, blob_names, level, date)
    print(len(isohypsen))


if __name__ == '__main__':
    SAS_token = ''  # TODO: fill in sas token here
    sas_url = r'https://stdeepgrondwaterdev001.blob.core.windows.net/external/?{}'.format(
        SAS_token)
    main(sas_url)
