# ruff: noqa: ARG001
from pathlib import Path
from typing import Dict

import pytest
import setuptools._distutils.util  # type: ignore[import-untyped]

from cibuildwheel.windows import PythonConfiguration, setup_setuptools_cross_compile


def test_x86(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    arch = "32"
    configuration = PythonConfiguration("irrelevant", arch, "irrelevant", None)
    generated_environment: Dict[str, str] = {}

    setup_setuptools_cross_compile(tmp_path, configuration, tmp_path, generated_environment)
    with monkeypatch.context() as mp:
        mp.setattr("os.name", "nt")
        for envvar, val in generated_environment.items():
            mp.setenv(name=envvar, value=val)
        target_platform = setuptools._distutils.util.get_platform()

    assert generated_environment["VSCMD_ARG_TGT_ARCH"] == "x86"
    assert target_platform == "win32"


def test_x64(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    arch = "64"
    configuration = PythonConfiguration("irrelevant", arch, "irrelevant", None)
    generated_environment: Dict[str, str] = {}

    setup_setuptools_cross_compile(tmp_path, configuration, tmp_path, generated_environment)
    with monkeypatch.context() as mp:
        mp.setattr("os.name", "nt")
        for envvar, val in generated_environment.items():
            mp.setenv(name=envvar, value=val)
        target_platform = setuptools._distutils.util.get_platform()

    assert generated_environment["VSCMD_ARG_TGT_ARCH"] == "x64"
    assert target_platform == "win-amd64"


def test_arm(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    arch = "ARM64"
    configuration = PythonConfiguration("irrelevant", arch, "irrelevant", None)
    generated_environment: Dict[str, str] = {}

    setup_setuptools_cross_compile(tmp_path, configuration, tmp_path, generated_environment)
    with monkeypatch.context() as mp:
        mp.setattr("os.name", "nt")
        for envvar, val in generated_environment.items():
            mp.setenv(name=envvar, value=val)
        target_platform = setuptools._distutils.util.get_platform()
    assert generated_environment["VSCMD_ARG_TGT_ARCH"] == "arm64"
    assert target_platform == "win-arm64"


def test_env_set(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    arch = "32"
    configuration = PythonConfiguration("irrelevant", arch, "irrelevant", None)
    generated_environment: Dict[str, str] = {"VSCMD_ARG_TGT_ARCH": "arm64"}

    setup_setuptools_cross_compile(tmp_path, configuration, tmp_path, generated_environment)
    with monkeypatch.context() as mp:
        mp.setattr("os.name", "nt")
        for envvar, val in generated_environment.items():
            mp.setenv(name=envvar, value=val)
        target_platform = setuptools._distutils.util.get_platform()

    assert generated_environment["VSCMD_ARG_TGT_ARCH"] == "arm64"
    assert target_platform == "win-arm64"


def test_env_blank(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    arch = "32"
    configuration = PythonConfiguration("irrelevant", arch, "irrelevant", None)
    generated_environment: Dict[str, str] = {"VSCMD_ARG_TGT_ARCH": ""}

    setup_setuptools_cross_compile(tmp_path, configuration, tmp_path, generated_environment)
    with monkeypatch.context() as mp:
        mp.setattr("os.name", "nt")
        for envvar, val in generated_environment.items():
            mp.setenv(name=envvar, value=val)
        target_platform = setuptools._distutils.util.get_platform()

    assert generated_environment["VSCMD_ARG_TGT_ARCH"] == "x86"
    assert target_platform == "win32"
