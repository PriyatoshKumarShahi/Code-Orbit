let currentText = "";
let currentLang = "english"; // 'english' or 'hindi'

// Load initial state
chrome.storage.local.get(['textToVerify'], (result) => {
  if (result.textToVerify) {
    currentText = result.textToVerify;
    verifyContent(currentText);
  }
});

// Listen for updates from background.js/content.js
chrome.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === 'local' && changes.textToVerify) {
    currentText = changes.textToVerify.newValue;
    verifyContent(currentText);
  }
});

// Setup language toggle
document.getElementById('lang-btn').addEventListener('click', () => {
  if (!currentText) return;
  currentLang = currentLang === "english" ? "hindi" : "english";
  verifyContent(currentText);
});

async function verifyContent(text) {
  const cleanedText = normalizeClaimText(text);
  if (!cleanedText) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('error').innerText = "No readable text found. Please select a longer claim.";
    document.getElementById('error').style.display = 'block';
    return;
  }

  document.getElementById('empty-state').style.display = 'none';
  document.getElementById('results-container').style.display = 'none';
  document.getElementById('error').style.display = 'none';
  document.getElementById('loading').style.display = 'block';
  document.body.classList.remove('high-alert');
  
  // Show a preview of the text
  document.getElementById('preview-text').innerText = cleanedText.length > 100 ? cleanedText.substring(0, 100) + '...' : cleanedText;

  try {
    const response = await fetch('http://localhost:8000/api/v1/verify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        // Send raw selected claim text only; prompt hints should not contaminate verification input.
        text: cleanedText,
        mode: 'text',
        explain_tone: 'simple'
      })
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const data = await response.json();
    displayResults(data);

  } catch (err) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('error').innerText = "Backend is offline or unreachable. Is SachAI running?";
    document.getElementById('error').style.display = 'block';
  }
}

function normalizeClaimText(text) {
  return String(text || "")
    .replace(/[\u200B-\u200D\uFEFF]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function displayResults(data) {
  document.getElementById('loading').style.display = 'none';
  document.getElementById('results-container').style.display = 'block';

  // 1. Truth Meter
  const badge = document.getElementById('verdict-badge');
  badge.innerText = data.short_verdict || data.verdict;
  
  let color = '#ff9900';
  let meterColor = '#ff9900';
  const verdictColor = data?.visual_meter?.verdict_color;
  if (verdictColor === 'red') { color = 'var(--danger-red)'; meterColor = 'var(--danger-red)'; }
  else if (verdictColor === 'green') { color = 'var(--success-green)'; meterColor = 'var(--success-green)'; }
  
  badge.style.background = color;
  badge.style.color = (color === 'var(--danger-red)') ? '#fff' : '#000';

  document.getElementById('explanation').innerText = buildBotStyleSummary(data);
  
  const riskFill = document.getElementById('risk-meter');
  // fake_probability is 0.0 to 1.0
  const probability = Number(data.fake_probability ?? 0.5);
  riskFill.style.width = `${Math.max(0, Math.min(100, probability * 100))}%`;
  riskFill.style.background = meterColor;

  // 2. Societal Impact
  const consq = data.consequences || "Potential harm may happen if this is forwarded without verification.";
  const socImp = data.social_impact || "Unverified claims can reduce trust and create panic.";
  document.getElementById('consequences').innerText = consq;
  document.getElementById('social-impact').innerText = socImp;

  // Riot/Panic Warning logic
  const alertKeywords = ["violence", "riot", "panic", "harm", "hinsa", "dange", "marpeet", "death"];
  const combinedImpact = (consq + " " + socImp).toLowerCase();
  const isHighAlert = alertKeywords.some(kw => combinedImpact.includes(kw));

  if (isHighAlert || probability > 0.85) {
    document.body.classList.add('high-alert');
    document.getElementById('impact-card').style.boxShadow = '4px 4px 0px #fff';
  } else {
    document.getElementById('impact-card').style.boxShadow = '4px 4px 0px var(--accent-cyan)';
  }

  // 3. Family Tree
  const familyCard = document.getElementById('family-card');
  const familyList = document.getElementById('family-tree-list');
  familyList.innerHTML = '';
  
  if (data.family_tree && data.family_tree.length > 0) {
    familyCard.style.display = 'block';
    data.family_tree.forEach(node => {
      const div = document.createElement('div');
      div.className = 'tree-node';
      div.innerHTML = `<span class="tree-year">${node.year || 'Past'}</span><div class="tree-title">${node.title}</div>`;
      familyList.appendChild(div);
    });
  } else {
    familyCard.style.display = 'none';
  }

  // 4. Chain of Trust (Mocked in backend)
  document.getElementById('flag-count').innerText = data.community_flags || 0;
}

function buildBotStyleSummary(data) {
  const verdict = data.verdict || "Needs More Evidence";
  const fakeProb = Number(data.fake_probability ?? 0.5);
  const credibility = Number(data.credibility_score ?? 0);
  const explanation = data.explanation || "No explanation available.";

  let advice = "We need more evidence to be sure. Please wait before forwarding this to family or friends.";
  if (verdict.includes("Fake") || verdict.includes("Suspicious")) {
    advice = "Please do NOT forward this message. Spread the truth, not rumors.";
  } else if (verdict.includes("Real")) {
    advice = "This appears verified, but still be cautious before forwarding.";
  }

  return [
    `Verdict: ${verdict}`,
    `Fake News Risk: ${Math.round(fakeProb * 100)}/100`,
    `Credibility Score: ${Math.round(credibility)}/100`,
    "",
    explanation,
    "",
    `Advice: ${advice}`,
  ].join("\n");
}
