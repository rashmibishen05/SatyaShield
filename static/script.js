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
        const data = await response.json();
        
        resultArea.innerText = data.result;
        
        const lowers = data.result.toLowerCase();
        if (lowers.includes('✅') || lowers.includes('authentic') || lowers.includes('true') || lowers.includes('normal') || lowers.includes('safe')) {
            resultArea.classList.add('success');
        } else if (lowers.includes('🚨') || lowers.includes('fake') || lowers.includes('false') || lowers.includes('manipulated') || lowers.includes('scam') || lowers.includes('suspicious')) {
            resultArea.classList.add('danger');
        } else if (lowers.includes('⚠️') || lowers.includes('caution') || lowers.includes('unverified') || lowers.includes('warning')) {
            resultArea.classList.add('warning');
        }
    } catch (error) {
        console.error(error);
        resultArea.innerText = 'Error processing request.';
        resultArea.classList.add('danger');
    } finally {
        loader.style.display = 'none';
        button.disabled = false;
    }
}
