#!/usr/bin/env python3
"""Simple build script for the Linky NVDA add-on using uv."""

import os
import os.path
import zipfile
import importlib
import sys
import codecs
import subprocess
import fnmatch

buildVars = importlib.import_module("buildVars")
addonInfo = buildVars.addon_info

addonPath = os.path.join("addon")
manifestPath = os.path.join(addonPath, "manifest.ini")
version = addonInfo.get("addon_version", "unknown")
addon_name = addonInfo.get("addon_name", "unknown")
excludedFiles = buildVars.excludedFiles if hasattr(buildVars, 'excludedFiles') else []

def createManifest():
	"""Create the manifest.ini file."""
	templatePath = "manifest.ini.tpl"
	
	if not os.path.exists(templatePath):
		manifestContent = f"""name = {addon_name}
summary = {addonInfo.get("addon_summary", "")}
version = {version}
author = {addonInfo.get("addon_author", "unknown")}
description = {addonInfo.get("addon_description", "")}
"""
	else:
		with codecs.open(templatePath, "r", "utf-8") as f:
			manifestContent = f.read()
		
		for key, value in addonInfo.items():
			if value is None:
				value = ""
			manifestContent = manifestContent.replace("{%s}" % key, str(value))
	
	with codecs.open(manifestPath, "w", "utf-8") as f:
		f.write(manifestContent)

def generateDocs():
	"""Generate HTML documentation from readme.md."""
	docPath = os.path.join(addonPath, "doc", "en", "readme.html")
	
	try:
		result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
		if result.returncode != 0:
			print("Warning: pandoc not found, skipping HTML generation")
			return
	except FileNotFoundError:
		print("Warning: pandoc not found, skipping HTML generation")
		return
	
	os.makedirs(os.path.dirname(docPath), exist_ok=True)
	
	try:
		subprocess.run([
			'pandoc', 'readme.md', 
			'-o', docPath,
			'--standalone',
			'--metadata', 'title=Linky NVDA Add-on'
		], check=True)
	except subprocess.CalledProcessError:
		print("Warning: Failed to generate HTML documentation")

def packageAddon():
	"""Package the add-on into a .nvda-addon file."""
	addonFile = f"{addon_name}-{version}.nvda-addon"
	
	def should_exclude(path, filename):
		"""Check if a file or directory should be excluded."""
		for pattern in excludedFiles:
			if fnmatch.fnmatch(filename, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
				return True
		return False
	
	with zipfile.ZipFile(addonFile, 'w', zipfile.ZIP_DEFLATED) as addonZip:
		for root, dirs, files in os.walk(addonPath):
			# Remove excluded directories from the dirs list to prevent os.walk from entering them
			dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), d)]
			
			for file in files:
				if should_exclude(os.path.join(root, file), file):
					continue
				filePath = os.path.join(root, file)
				arcName = os.path.relpath(filePath, addonPath)
				addonZip.write(filePath, arcName)
	
	print(f"Created {addonFile}")

def main():
	"""Build the add-on using uv."""
	try:
		print("Creating manifest...")
		createManifest()
		
		print("Generating documentation...")
		generateDocs()
		
		print("Packaging add-on...")
		packageAddon()
		
		print("Build completed successfully!")
		return 0
	except Exception as e:
		print(f"Build failed with error: {e}")
		return 1

if __name__ == "__main__":
	sys.exit(main())