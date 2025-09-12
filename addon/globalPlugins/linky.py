import globalPluginHandler
import ui
import speech
import webbrowser
import re
from collections import deque
import scriptHandler

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""Global plugin that opens the last spoken link."""

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self._speechHistory = deque(maxlen=500)
		self._originalSpeak = speech.speech.speak
		speech.speech.speak = self._customSpeak

	def terminate(self):
		"""Clean up when the plugin is terminated."""
		speech.speech.speak = self._originalSpeak
		super(GlobalPlugin, self).terminate()

	def _customSpeak(self, speechSequence, *args, **kwargs):
		"""Custom speak function that captures speech and calls original."""
		if speechSequence:
			text = self._getTextFromSpeechSequence(speechSequence)
			if text and text.strip():
				self._speechHistory.appendleft(text.strip())
		
		return self._originalSpeak(speechSequence, *args, **kwargs)

	def _getTextFromSpeechSequence(self, speechSequence):
		"""Extract text from a speech sequence."""
		text = ""
		for item in speechSequence:
			if isinstance(item, str):
				text += item
			elif hasattr(item, 'text'):
				text += item.text
		return text

	_URL_PATTERN = r'https?://[^\s]+|www\.[^\s]+\.[a-zA-Z]{2,}'

	def _isUrl(self, text):
		"""Check if text contains a URL."""
		return re.search(self._URL_PATTERN, text) is not None

	def _extractUrl(self, text):
		"""Extract the first URL from text."""
		match = re.search(self._URL_PATTERN, text)
		if match:
			url = match.group()
			if url.startswith("www."):
				url = "https://" + url
			return url
		return None

	@scriptHandler.script(
		description="Open the last spoken link",
		category="Linky",
		gesture="kb:control+NVDA+l"
	)
	def script_openLastLink(self, gesture):
		"""Open the last spoken link."""
		if not self._speechHistory:
			ui.message("No speech history available")
			return

		for text in self._speechHistory:
			if self._isUrl(text):
				url = self._extractUrl(text)
				if url:
					try:
						webbrowser.open(url)
						ui.message(f"Opening {url}")
						return
					except Exception as e:
						ui.message(f"Error opening link: {str(e)}")
						return

		ui.message("No link found in recent speech")