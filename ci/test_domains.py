import numpy as np
import pytest
import pandas as pd


km_map = {
    0.11: 12,
    0.22: 25,
    0.44: 50,
}


df = pd.read_csv("CORDEX-CMIP6_rotated_grids.csv", index_col="domain_id")


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
    dm = table.loc[domain_id].copy()
    dm["ll_lon"], dm["ll_lat"], dm["nlon"], dm["nlat"] = _scale(
        dm.ll_lon, dm.ll_lat, dm.nlon, dm.nlat, dm.dlon, dl
    )
    dm["dlon"] = dl
    dm["dlat"] = dl
    dm["ur_lon"] = dm.ll_lon + (dm.nlon - 1) * dl
    dm["ur_lat"] = dm.ll_lat + (dm.nlat - 1) * dl
    dm["CORDEX_domain"] = f"{domain_id.split("-")[0]}-{int(dm.dlon*100)}"
    dm.name = f"{domain_id.split("-")[0]}-{km_map[dl]}"
    return dm


def boundaries(ll_lon, ll_lat, nlon, nlat, dl):
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
    scale0 = table.iloc[0]
    for domain_id, dm in table.iterrows():
        scaled = scale_domain(table, scale0.name, dm.dlon)
        print(f"Testing {scale0.name} vs {dm.name}")
        pd.testing.assert_series_equal(scaled, table.loc[scaled.name])
        print("Testing")


def check_boundaries(df):
    return {region: check_boundary(table) for region, table in df.groupby("region")}


def check_scales(table):
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
    for region, table in df.groupby("region"):
        if region not in [7]:
            check_scale(table)
