document.addEventListener('DOMContentLoaded', function () {
	document.getElementById('sendButton').addEventListener('click', function () {
		console.log('helloworld');
		sendHTMLToAPI();
		highlightRandomElement();
		chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
			const activeTab = tabs[0];
			chrome.scripting.executeScript({
				target: { tabId: activeTab.id },
				function: highlightRandomElement,
			});
		});
	});

	function highlightRandomElement() {
		chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
			chrome.scripting.executeScript({
				target: { tabId: tabs[0].id },
				function: injectHighlightCode,
			});
		});
	}

	function injectHighlightCode() {
		const elements = document.querySelectorAll('*');
		const randomIndex = Math.floor(Math.random() * elements.length);
		const randomElement = elements[randomIndex];
		randomElement.style.border = '2px solid yellow';
	}
});

function sendHTMLToAPI() {
	chrome.runtime.sendMessage({ action: 'sendHTML' }, function (response) {
		if (chrome.runtime.lastError) {
			console.error('Error sending message: ', chrome.runtime.lastError);
			return;
		}

		// Assuming you have an API endpoint to send the HTML content
		fetch('https://httpbin.org/post', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ html: response.html }),
		})
			.then((response) => response.json())
			.then((data) => {
				console.log('API Response:', data);
			})
			.catch((error) => {
				console.error('API Error:', error);
			});
	});
}

// document.addEventListener('DOMContentLoaded', function () {
// 	const sendButton = document.getElementById('sendButton');
// 	sendButton.addEventListener('click', highlightRandomElement);

// });
