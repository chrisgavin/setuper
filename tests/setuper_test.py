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

def test_test():
	setup_path = pathlib.Path(__file__).parent / "resources" / "setup.py"
	with tempfile.TemporaryDirectory("setuper_tests") as test_virtualenv:
		virtualenv.create_environment(test_virtualenv)
		virtualenv_path = pathlib.Path(test_virtualenv)
		initial_packages = _get_installed_packages(virtualenv_path)
		setuper.run(setup_path, pip=[str(virtualenv_path / "bin" / "python"), "-m", "pip"])
		final_packages = _get_installed_packages(virtualenv_path)
		packages = final_packages.difference(initial_packages)
		assert {"Jinja2", "requests"}.issubset(packages)
