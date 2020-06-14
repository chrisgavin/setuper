import pathlib
import tempfile
import subprocess

import virtualenv

import setuper

def _get_installed_packages(virtualenv_path):
	installed_packages = subprocess.check_output([str(virtualenv_path / "bin" / "python"), "-m", "pip", "list"]).decode("utf-8")
	installed_packages = installed_packages.split("\n")[2:]
	installed_packages = [package.split(" ")[0].strip() for package in installed_packages]
	installed_packages = {package for package in installed_packages if package}
	return installed_packages

def _test_with_test_file(test_file_name, expected_packages=set(), unexpected_packages=set(), **kwargs):
	setup_path = pathlib.Path(__file__).parent / "resources" / test_file_name
	with tempfile.TemporaryDirectory("setuper_tests") as test_virtualenv:
		virtualenv_path = pathlib.Path(test_virtualenv)
		virtualenv.cli_run([str(virtualenv_path)])
		initial_packages = _get_installed_packages(virtualenv_path)
		setuper.run(setup_path, pip=[str(virtualenv_path / "bin" / "python"), "-m", "pip"], **kwargs)
		final_packages = _get_installed_packages(virtualenv_path)
		packages = final_packages.difference(initial_packages)
		if expected_packages:
			assert expected_packages.issubset(packages)
		if unexpected_packages:
			assert not unexpected_packages.issubset(packages)

def test_setup():
	_test_with_test_file("setup.py", expected_packages={"Jinja2", "requests"})

def test_extras_require():
	_test_with_test_file("extras_require.py", expected_packages={"Jinja2", "requests", "Pillow"}, unexpected_packages={"matplotlib"}, extras=["dev"])
