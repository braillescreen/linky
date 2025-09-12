# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# for previously unpublished addons, please follow the community guidelines at:
	# https://bitbucket.org/nvdaaddonteam/todo/raw/master/guideLines.txt
	# add-on Name, internal for nvda
	"addon_name": "linky",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on to be shown on installation and add-on information.
	"addon_summary": _("Linky"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description": _("""Opens the last spoken link with a hotkey (Ctrl+NVDA+L)."""),
	# version
	"addon_version": "2025.09.1",
	# Author(s)
	"addon_author": "BrailleScreen",
	# URL for the add-on documentation support
	"addon_url": "https://github.com/braillescreen/linky",
	# Documentation file name
	"addon_docFileName": "readme.html",
	# Minimum NVDA version supported (e.g. "2018.3.0", minor version is optional)
	"addon_minimumNVDAVersion": "2023.1.0",
	# Last NVDA version supported/tested (e.g. "2018.4.0", ideally more recent than minimum version)
	"addon_lastTestedNVDAVersion": "2025.2.0",
	# Add-on update channel (default is None, denoting stable releases, and for development releases, use "dev", do not change unless you know what you are doing)
	"addon_updateChannel": None,
}


import os.path

# Define the python files that are the sources of this add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = [os.path.join("addon", "globalPlugins", "*.py")]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the add-on.
# Paths are relative to the add-on directory, not to the directory containing SConstruct
excludedFiles = [
	"*.pyc",
	"*.egg-info",
	"__pycache__"
]