// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "extract_text") {
    // Save to storage so the popup can read it
    chrome.storage.local.set({ textToVerify: request.text }, () => {
      // Notify the user to click the extension icon since popups cannot be opened programmatically
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icon.png', // Assuming icon.png exists or use a default one
        title: 'Parakh: Text Captured',
        message: 'Click the Parakh extension icon in your toolbar to see the truth report!'
      });
    });
    sendResponse({ status: "received" });
  }
});
