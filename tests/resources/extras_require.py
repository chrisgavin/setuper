#!/usr/bin/env python3
import setuptools

def main():
	setuptools.setup(
		name="testpackage",
		version="1.0.0",
		description="A test Python module.",
		packages=["testpackage"],
		install_requires=[
			"jinja2",
			"requests",
		],
		extras_require={
			"dev": [
				"Pillow",
			],
			"something-else": [
				"matplotlib",
			],
		},
	)

if __name__ == "__main__":
	main()
