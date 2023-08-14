// background.js
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
	if (request.action === 'sendHTML') {
		// Forward the message to content script
		chrome.tabs.sendMessage(sender.tab.id, request, sendResponse);
		return true;
	}
});
