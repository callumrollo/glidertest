import pooch
import xarray as xr

server = "https://erddap.observations.voiceoftheocean.org/examples/glidertest"
data_source_og = pooch.create(
    path=pooch.os_cache("glidertest"),
    base_url=server,
    registry={
        "sea055_20220104T1536_delayed.nc": "sha256:7f72f8a0398c3d339687d7b7dcf0311036997f6855ed80cae5bbf877e09975a6",
        "sea045_20230604T1253_delayed.nc": "sha256:9d71b5fb580842e8296b447041cd5b544c8b4336df40a8f3c2e09279f436f502",
        "sg015_20050213T230253_delayed.nc": "sha256:ca64e33e9f317e1fc3442e74485a9bf5bb1b4a81b5728e9978847b436e0586ab",
        "sg014_20040924T182454_delayed.nc": "sha256:c9fca08ce676573224c04512f4d5bfe251d0419478ee433dfefa03aa70e2eb9a",
        "sg014_20040924T182454_delayed_subset.nc": "sha256:0e97a4107364d27364d076ed8007f08c891b2015b439cf524a44612de0a1a2ea",
        'sea055_20240628T0856_delayed.nc': 'sha256:5df052d2ac1403d123e585483ac9f1869c9acda714f6ae2c443bac27daa96280',
        'sea055_20241009T1345_delayed.nc': 'sha256:cd411c326b2734efd73a02b97e43c019dccbe1825447542b1d7cbfa4130639e4',
        'sea069_20230726T0628_delayed.nc': 'sha256:774cf779b5632bef1c2269eae916797ab73290e61fe36bf9085bed699d53562e',
        'sea077_20230316T1019_delayed.nc': 'sha256:cc14ec6e8826b66a8bb4d4b1f0aecf13d4a00856f55141872fd0d1a7798aec29',
        'sea067_20221113T0853_delayed.nc': 'sha256:87f78226f89cfbd602aa1e05f92b907dde5b1cccc0adbe56399ff5faf8b7937e',
        'sea063_20230811T1657_delayed.nc': 'sha256:407a7d990b47009d6d1887919259a0af8ff285bc6a12c80d32a5eeec39d93140',
        'sea045_20230530T0832_delayed.nc': 'sha256:f6193cc9cca4d557faa1bbf1b3e381d056d91c2637af3627c1a062cd978aca82',
        'sea077_20220906T0748_delayed.nc': 'sha256:54c56e23c2e8c9d5460aa4fd9eab6e8ac365af27f0634354df12ea2e0ebd7379'
    },
)


def load_sample_dataset(dataset_name="sea045_20230604T1253_delayed.nc"):
    """Download sample datasets for use with glidertest

    Parameters
    ----------
    dataset_name: str, optional
        Default is "sea045_20230530T0832_delayed.nc".

    Raises
    ------
    ValueError: 
        If the requests dataset is not known, raises a value error

    Returns
    -------
    xarray.Dataset: 
        Requested sample dataset
    """
    if dataset_name in data_source_og.registry.keys():
        file_path = data_source_og.fetch(dataset_name)
        return xr.open_dataset(file_path)
    else:
        msg = f"Requested sample dataset {dataset_name} not known. Specify one of the following available datasets: {list(data_source_og.registry.keys())}"
        raise KeyError(msg)
