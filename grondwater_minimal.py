from azure.storage.blob import ContainerClient
import rasterio
from io import BytesIO


def read_raster(container_client, blob_names, raster_type, date):
    relevant_blob_names = [blob_name for blob_name in blob_names if blob_name.endswith('{}.tif'.format(raster_type))]
    # check if the date exists
    try:
        blob_name_to_read = [blob_name for blob_name in relevant_blob_names if date in blob_name][0]
    except IndexError:
        raise ValueError('Date {} does not exist'.format(date))
    blob_client = container_client.get_blob_client(blob_name_to_read)
    raster_blob = blob_client.download_blob().readall()
    
    with rasterio.open(BytesIO(raster_blob)) as src:
        raster = src.read(1)
        meta = src.meta
    
    return raster, meta


def main(sas_url, raster_type, date):
    # the sas_url is the url to the container, not the blob itself. List all blobs in the container
    container_client = ContainerClient.from_container_url(sas_url)
    blob_list = container_client.list_blobs()
    blob_names = [blob.name for blob in blob_list]

    raster, meta = read_raster(container_client, blob_names, raster_type, date)

    print(raster.shape)
    print(meta)


if __name__ == '__main__':
    SAS_token = ''  # TODO: fill in sas token here
    sas_url = r'https://stdeepgrondwaterdev001.blob.core.windows.net/external/?{}'.format(SAS_token)

    raster_type = 'CAT'  # raster_types are: NAP (relative to NAP), MV (relative to 'maaiveld'), CAT (categorical (very_dry->very_wet))]
    date = '20230416'  # date in the format 'YYYYMMDD'
    
    main(sas_url, raster_type, date)