from setuptools import setup


setup(
	author="zakx",
	author_email="sg@unkreativ.org",
	classifiers=[
		"Development Status :: 4 - Beta",
		"Environment :: Console",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Natural Language :: English",
		"Operating System :: POSIX",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Topic :: Printing",
	],
	description=" A Python script that reads PNG files and prints them on a Brother P2430PC",
	entry_points={
		'console_scripts': [
			"printpng=printpng:main",
		],
	},
	install_requires=[
		"Pillow >= 2.2.1",
	],
	keywords=[
		"label",
		"print",
		"ptouch",
	],
	license="GPLv3",
	name="png2ptouch",
    py_modules=['printpng'],
	url="https://github.com/zakx/png2ptouch",
	version="1.2",
)
