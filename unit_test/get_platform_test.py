# ruff: noqa: ARG001
import contextlib
from pathlib import Path
from typing import Dict

import pytest
import setuptools._distutils.util

from cibuildwheel.windows import PythonConfiguration, setup_setuptools_cross_compile


@contextlib.contextmanager
def patched_environment(monkeypatch: pytest.MonkeyPatch, environment: Dict[str, str]):
    with monkeypatch.context() as mp:
        mp.setattr("os.name", "nt")
        for envvar, val in environment.items():
            mp.setenv(name=envvar, value=val)
        yield


def test_x86(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    arch = "32"
    environment: Dict[str, str] = {}

    configuration = PythonConfiguration("irrelevant", arch, "irrelevant", None)

    setup_setuptools_cross_compile(tmp_path, configuration, tmp_path, environment)
    with patched_environment(monkeypatch, environment):
        target_platform = setuptools._distutils.util.get_platform()

    assert environment["VSCMD_ARG_TGT_ARCH"] == "x86"
    assert target_platform == "win32"


def test_x64(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    arch = "64"
    environment: Dict[str, str] = {}

    configuration = PythonConfiguration("irrelevant", arch, "irrelevant", None)

    setup_setuptools_cross_compile(tmp_path, configuration, tmp_path, environment)
    with patched_environment(monkeypatch, environment):
        target_platform = setuptools._distutils.util.get_platform()

    assert environment["VSCMD_ARG_TGT_ARCH"] == "x64"
    assert target_platform == "win-amd64"


def test_arm(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    arch = "ARM64"
    environment: Dict[str, str] = {}

    configuration = PythonConfiguration("irrelevant", arch, "irrelevant", None)

    setup_setuptools_cross_compile(tmp_path, configuration, tmp_path, environment)
    with patched_environment(monkeypatch, environment):
        target_platform = setuptools._distutils.util.get_platform()

    assert environment["VSCMD_ARG_TGT_ARCH"] == "arm64"
    assert target_platform == "win-arm64"


def test_env_set(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    arch = "32"
    environment = {"VSCMD_ARG_TGT_ARCH": "arm64"}

    configuration = PythonConfiguration("irrelevant", arch, "irrelevant", None)

    setup_setuptools_cross_compile(tmp_path, configuration, tmp_path, environment)
    with patched_environment(monkeypatch, environment):
        target_platform = setuptools._distutils.util.get_platform()

    assert environment["VSCMD_ARG_TGT_ARCH"] == "arm64"
    assert target_platform == "win-arm64"


def test_env_blank(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    arch = "32"
    environment = {"VSCMD_ARG_TGT_ARCH": ""}

    configuration = PythonConfiguration("irrelevant", arch, "irrelevant", None)

    setup_setuptools_cross_compile(tmp_path, configuration, tmp_path, environment)
    with patched_environment(monkeypatch, environment):
        target_platform = setuptools._distutils.util.get_platform()

    assert environment["VSCMD_ARG_TGT_ARCH"] == "x86"
    assert target_platform == "win32"
