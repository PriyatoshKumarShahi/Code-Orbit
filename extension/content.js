// Inject a floating Parakh button when text is selected
let floatingBtn = null;

document.addEventListener('mouseup', (e) => {
  const selectedText = window.getSelection().toString().trim();
  
  if (selectedText.length > 10) {
    if (!floatingBtn) {
      floatingBtn = document.createElement('button');
      floatingBtn.innerText = "🔍 Parakh Verify";
      floatingBtn.style.position = 'absolute';
      floatingBtn.style.zIndex = '999999';
      floatingBtn.style.background = '#FF00FF'; // Brutalism pink
      floatingBtn.style.color = '#000';
      floatingBtn.style.border = '2px solid #000';
      floatingBtn.style.boxShadow = '3px 3px 0px #000';
      floatingBtn.style.padding = '5px 10px';
      floatingBtn.style.fontWeight = 'bold';
      floatingBtn.style.cursor = 'pointer';
      floatingBtn.style.fontFamily = 'sans-serif';
      document.body.appendChild(floatingBtn);
      
      floatingBtn.addEventListener('click', () => {
        const textToVerify = window.getSelection().toString().trim();
        chrome.runtime.sendMessage({ action: "extract_text", text: textToVerify });
        floatingBtn.innerText = "Checked! Open Parakh ↗";
        setTimeout(() => {
          if (floatingBtn) {
            floatingBtn.remove();
            floatingBtn = null;
          }
        }, 1500);
      });
    }
    
    // Position the button near the mouse
    floatingBtn.style.top = `${e.pageY + 10}px`;
    floatingBtn.style.left = `${e.pageX + 10}px`;
  } else {
    if (floatingBtn) {
      floatingBtn.remove();
      floatingBtn = null;
    }
  }
});

// WhatsApp Web "Forward-Check" Overlay
if (window.location.hostname === 'web.whatsapp.com') {
  console.log("Parakh: WhatsApp Web detected. Initializing Forward-Check.");
  
  // A simple observer to find messages and append a check button
  setInterval(() => {
    // Look for message containers that don't have our button yet
    const messages = document.querySelectorAll('div[data-id]:not(.parakh-injected)');
    
    messages.forEach(msg => {
      // Find the text content inside the message
      const textSpan = msg.querySelector('span.selectable-text');
      if (textSpan && textSpan.innerText.length > 15) {
        msg.classList.add('parakh-injected');
        
        // Check if it looks forwarded (WhatsApp uses specific icons or "Forwarded" text)
        // We'll just add it to all incoming messages for the demo
        
        const btn = document.createElement('span');
        btn.innerHTML = '🔍 Verify';
        btn.style.background = '#00FFFF'; // Brutalism cyan
        btn.style.color = '#000';
        btn.style.border = '1px solid #000';
        btn.style.boxShadow = '1px 1px 0px #000';
        btn.style.fontSize = '10px';
        btn.style.fontWeight = 'bold';
        btn.style.padding = '2px 5px';
        btn.style.marginLeft = '5px';
        btn.style.cursor = 'pointer';
        btn.style.borderRadius = '3px';
        
        btn.onclick = (e) => {
          e.stopPropagation();
          chrome.runtime.sendMessage({ action: "extract_text", text: textSpan.innerText });
        };
        
        // Append next to the text
        textSpan.parentNode.appendChild(btn);
      }
    });
  }, 2000);
}
