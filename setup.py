from setuptools import setup


PACKAGE = "cc_counter"
VERSION = "0.65"

setup(
    name=PACKAGE,
    version=VERSION,
    description="counts the cyclomatic complexity of the file",
    author="Kelvin Fann",
    packages=["cc_counter"],
    entry_points={
        'reviewboard.extensions':
            '%s = cc_counter.extension:CCCounter' % PACKAGE,
    },
	package_data={
		'cc_counter': [
			'templates/cc_counter/*.html',
		],
	}
)
