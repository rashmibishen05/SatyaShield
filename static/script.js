async function apiCall(endpoint, body, isJson = true, button, resultId) {
    const loader = button.querySelector('.loader');
    const resultArea = document.getElementById(resultId);
    
    loader.style.display = 'inline-block';
    button.disabled = true;
    resultArea.classList.remove('success', 'danger', 'warning');
    resultArea.innerText = 'Analyzing...';

    try {
        const options = {
            method: 'POST',
            body: isJson ? JSON.stringify(body) : body
        };
        if (isJson) {
            options.headers = { 'Content-Type': 'application/json' };
        }

        const response = await fetch(endpoint, options);

        if (!response.ok) {
            const errData = await response.json().catch(() => ({ result: `Server error: ${response.status}` }));
            resultArea.innerText = errData.result || `Server error: ${response.status}`;
            resultArea.classList.add('danger');
            return;
        }

        const data = await response.json();
        const resultText = data.result || 'No result returned.';
        resultArea.innerText = resultText;

        const lower = resultText.toLowerCase();

        // --- PRIORITY 1: EMOJI-BASED COLORING (Exact Match) ---
        if (resultText.includes('🚨') || resultText.includes('❌')) {
            resultArea.classList.add('danger');
        } else if (resultText.includes('⚠️') || resultText.includes('🔍')) {
            resultArea.classList.add('warning');
        } else if (resultText.includes('✅')) {
            resultArea.classList.add('success');
        } 
        // --- PRIORITY 2: KEYWORD-BASED FALLBACK ---
        else {
            const isDanger =
                lower.includes('fake') ||
                lower.includes('false') ||
                lower.includes('manipulated') ||
                lower.includes('scam') ||
                lower.includes('high risk') ||
                lower.includes('phishing') ||
                lower.includes('malicious') ||
                lower.includes('deepfake');

            const isWarning =
                lower.includes('suspicious') ||
                lower.includes('caution') ||
                lower.includes('unverified') ||
                lower.includes('warning') ||
                lower.includes('pending');

            const isSuccess =
                lower.includes('authentic') ||
                lower.includes('trusted') ||
                lower.includes('true') ||
                lower.includes('normal') ||
                lower.includes('safe') ||
                lower.includes('no obvious manipulation');

            if (isDanger) {
                resultArea.classList.add('danger');
            } else if (isWarning) {
                resultArea.classList.add('warning');
            } else if (isSuccess) {
                resultArea.classList.add('success');
            }
        }

    } catch (error) {
        console.error('Fetch error:', error);
        resultArea.innerText = 'Network error: Could not connect to the server.';
        resultArea.classList.add('danger');
    } finally {
        loader.style.display = 'none';
        button.disabled = false;
    }
}
