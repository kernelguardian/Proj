// content.js
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
	if (request.action === 'sendHTML') {
		const htmlContent = document.documentElement.outerHTML;
		sendResponse({ html: htmlContent });
	}
});
