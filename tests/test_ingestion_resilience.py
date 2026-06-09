from io import StringIO

import pandas as pd

from src.ingestion import update_elo
from src.ingestion import update_teams


def _elo_tsv_row() -> str:
    values = [
        "1",
        "1",
        "ES",
        "2157",
        "1",
        "2189",
        "7",
        "1946",
        "19",
        "1805",
        "0",
        "-15",
        "0",
        "-15",
        "0",
        "0",
        "+3",
        "+137",
        "+4",
        "+125",
        "+4",
        "+166",
        "782",
        "341",
        "302",
        "139",
        "462",
        "138",
        "182",
        "1595",
        "699",
    ]

    return "\t".join(values)


def test_download_elo_rankings_accepts_valid_tsv(monkeypatch):
    original_read_csv = pd.read_csv

    def fake_read_csv(source, *args, **kwargs):
        if source == update_elo.ELO_TSV_URL:
            return original_read_csv(StringIO(_elo_tsv_row()), *args, **kwargs)

        return original_read_csv(source, *args, **kwargs)

    monkeypatch.setattr(update_elo.pd, "read_csv", fake_read_csv)

    df = update_elo.download_elo_rankings()

    assert df.attrs["from_cache"] is False
    assert df.loc[0, "country_code"] == "ES"
    assert "extracted_at" in df.columns
    assert df.loc[0, "source"] == update_elo.ELO_TSV_URL


def test_download_elo_rankings_rejects_html_and_loads_cache(
    monkeypatch,
    tmp_path,
    capsys,
    caplog,
):
    cached_path = tmp_path / "elo_rankings.csv"
    cached = pd.DataFrame(
        {
            "rank": [1],
            "team": [1],
            "country_code": ["AR"],
            "rating": [2114],
        }
    )
    cached.to_csv(cached_path, index=False)
    original_read_csv = pd.read_csv

    def fake_read_csv(source, *args, **kwargs):
        if source == update_elo.ELO_TSV_URL:
            return original_read_csv(
                StringIO("<!DOCTYPE html><html><head></head></html>"),
                *args,
                **kwargs,
            )

        return original_read_csv(source, *args, **kwargs)

    monkeypatch.setattr(update_elo, "RAW_OUTPUT_PATH", cached_path)
    monkeypatch.setattr(update_elo.pd, "read_csv", fake_read_csv)

    caplog.set_level("WARNING")
    df = update_elo.download_elo_rankings()
    output = capsys.readouterr().out

    assert df.attrs["from_cache"] is True
    assert df.loc[0, "country_code"] == "AR"
    assert "Remote Elo source unavailable." in caplog.text
    assert "WARNING - Remote Elo source unavailable." in output
    assert "Using local cached elo_rankings.csv" in output


def test_elo_main_does_not_overwrite_cache_when_remote_is_html(
    monkeypatch,
    tmp_path,
):
    cached_path = tmp_path / "elo_rankings.csv"
    cached_text = "rank,team,country_code,rating\n1,1,BR,1991\n"
    cached_path.write_text(cached_text, encoding="utf-8")
    original_read_csv = pd.read_csv

    def fake_read_csv(source, *args, **kwargs):
        if source == update_elo.ELO_TSV_URL:
            return original_read_csv(
                StringIO("<html><head>Unavailable</head></html>"),
                *args,
                **kwargs,
            )

        return original_read_csv(source, *args, **kwargs)

    monkeypatch.setattr(update_elo, "RAW_OUTPUT_PATH", cached_path)
    monkeypatch.setattr(update_elo.pd, "read_csv", fake_read_csv)

    update_elo.main()

    assert cached_path.read_text(encoding="utf-8") == cached_text


def test_download_teams_lookup_accepts_valid_tsv(monkeypatch):
    original_read_csv = pd.read_csv

    def fake_read_csv(source, *args, **kwargs):
        if source == update_teams.TEAMS_TSV_URL:
            return original_read_csv(
                StringIO("ES\tSpain\nAR\tArgentina\n"),
                *args,
                **kwargs,
            )

        return original_read_csv(source, *args, **kwargs)

    monkeypatch.setattr(update_teams.pd, "read_csv", fake_read_csv)

    df = update_teams.download_teams_lookup()

    assert df.attrs["from_cache"] is False
    assert df.loc[0, "country_code"] == "ES"
    assert df.loc[0, "team_name"] == "Spain"
    assert "extracted_at" in df.columns


def test_download_teams_lookup_rejects_html_and_loads_cache(
    monkeypatch,
    tmp_path,
    capsys,
    caplog,
):
    cached_path = tmp_path / "teams_lookup.csv"
    cached_path.write_text(
        "country_code,team_name\nFR,France\n",
        encoding="utf-8",
    )
    original_read_csv = pd.read_csv

    def fake_read_csv(source, *args, **kwargs):
        if source == update_teams.TEAMS_TSV_URL:
            return original_read_csv(
                StringIO("<html><head>Unavailable</head></html>"),
                *args,
                **kwargs,
            )

        return original_read_csv(source, *args, **kwargs)

    monkeypatch.setattr(update_teams, "RAW_OUTPUT_PATH", cached_path)
    monkeypatch.setattr(update_teams.pd, "read_csv", fake_read_csv)

    caplog.set_level("WARNING")
    df = update_teams.download_teams_lookup()
    output = capsys.readouterr().out

    assert df.attrs["from_cache"] is True
    assert df.loc[0, "country_code"] == "FR"
    assert df.loc[0, "team_name"] == "France"
    assert "Remote teams source unavailable." in caplog.text
    assert "WARNING - Remote teams source unavailable." in output
    assert "Using local cached teams_lookup.csv" in output


def test_teams_main_does_not_overwrite_cache_when_remote_is_html(
    monkeypatch,
    tmp_path,
):
    cached_path = tmp_path / "teams_lookup.csv"
    cached_text = "country_code,team_name\nBR,Brazil\n"
    cached_path.write_text(cached_text, encoding="utf-8")
    original_read_csv = pd.read_csv

    def fake_read_csv(source, *args, **kwargs):
        if source == update_teams.TEAMS_TSV_URL:
            return original_read_csv(
                StringIO("<!DOCTYPE html><html></html>"),
                *args,
                **kwargs,
            )

        return original_read_csv(source, *args, **kwargs)

    monkeypatch.setattr(update_teams, "RAW_OUTPUT_PATH", cached_path)
    monkeypatch.setattr(update_teams.pd, "read_csv", fake_read_csv)

    update_teams.main()

    assert cached_path.read_text(encoding="utf-8") == cached_text
