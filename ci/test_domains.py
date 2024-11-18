import numpy as np
import pytest
import pandas as pd


km_map = {
    0.11: 12,
    0.1: 12,
    0.22: 25,
    0.44: 50,
}

numeric_cols = [
    "ll_lon",
    "ll_lat",
    "nlon",
    "nlat",
    "dlon",
    "dlat",
    "ur_lon",
    "ur_lat",
    "pollon",
    "pollat",
]

# df = pd.read_csv("CORDEX-CMIP6_rotated_grids.csv", index_col="domain_id")


@pytest.fixture
def table():
    return pd.read_csv("CORDEX-CMIP6_rotated_grids.csv", index_col="domain_id")


def _scale(ll_lon, ll_lat, nlon, nlat, dl, dlnew):
    factor = dl / dlnew
    shift = 0.5 * (dlnew - dl)
    ll_lon_scaled = ll_lon + shift
    ll_lat_scaled = ll_lat + shift
    nlon_scaled = int(nlon * factor)
    nlat_scaled = int(nlat * factor)
    return tuple(
        map(
            lambda x: np.round(x, 7),
            (ll_lon_scaled, ll_lat_scaled, nlon_scaled, nlat_scaled),
        )
    )


def scale(dm, dl):
    return _scale(dm.ll_lon, dm.ll_lat, dm.nlon, dm.nlat, dm.dlon, dl)


def scale_domain(table, domain_id, dl):
    """scale a domain to a new resolution"""
    dm = table.loc[domain_id].copy()
    dm["ll_lon"], dm["ll_lat"], dm["nlon"], dm["nlat"] = _scale(
        dm.ll_lon, dm.ll_lat, dm.nlon, dm.nlat, dm.dlon, dl
    )
    dm["dlon"] = dl
    dm["dlat"] = dl
    dm["ur_lon"] = dm.ll_lon + (dm.nlon - 1) * dl
    dm["ur_lat"] = dm.ll_lat + (dm.nlat - 1) * dl
    dm["CORDEX_domain"] = f"{domain_id.split('-')[0]}-{int(dm.dlon*100)}"
    dm.name = f"{domain_id.split('-')[0]}-{km_map[dl]}"
    return dm


def boundaries(ll_lon, ll_lat, nlon, nlat, dl):
    """compute boundaries of a domain"""
    bounds = (
        ll_lon - 0.5 * dl,
        ll_lat - 0.5 * dl,
        ll_lon + (nlon - 0.5) * dl,
        ll_lat + (nlat - 0.5) * dl,
    )
    return tuple(map(lambda x: np.round(x, 7), bounds))


def check_boundary(table):
    bounds = [
        boundaries(dm.ll_lon, dm.ll_lat, dm.nlon, dm.nlat, dm.dlon)
        for domain_id, dm in table.iterrows()
    ]
    all_the_same = all(b == bounds[0] for b in bounds)
    return all_the_same
    # assert all(bounds[i][2] == bounds[i+1][0] for i in range(len(bounds)-1))


def check_scale(table):
    """find first domain in a region and check if scaling is consistent"""
    scale0 = table.iloc[0]
    for domain_id, dm in table.iterrows():
        scaled = scale_domain(table, scale0.name, dm.dlon)
        print(f"Testing {scale0.name} vs {dm.name}")
        pd.testing.assert_series_equal(
            scaled[numeric_cols], table.loc[scaled.name][numeric_cols]
        )


def check_boundaries(df):
    return {region: check_boundary(table) for region, table in df.groupby("region")}


def test_boundaries(table):
    checks = check_boundaries(table)
    print("Checking boundaries")
    for region, check in checks.items():
        print(f"Region {region}: {check}")
        # some exceptios here for CORDEX CORE SEA-25
        if region not in [7]:
            assert check


def test_scales(table):
    print("Checking correct scaling")
    for region, table in table.groupby("region"):
        if region not in [7]:
            check_scale(table)


def test_east_north(table):
    """check if east and north boundaries are consistent"""
    for domain_id, dm in table.iterrows():
        print(f"Testing east north: {domain_id}")
        assert dm.ur_lon == np.round(dm.ll_lon + (dm.nlon - 1) * dm.dlon, 7)
        assert dm.ur_lat == np.round(dm.ll_lat + (dm.nlat - 1) * dm.dlat, 7)
