// API base URL
const API_BASE = window.location.origin;

// DOM elements
const startForm = document.getElementById('startForm');
const verifyForm = document.getElementById('verifyForm');
const startResponse = document.getElementById('startResponse');
const verifyResponse = document.getElementById('verifyResponse');
const apiStatus = document.getElementById('apiStatus');

// Check API status on page load
checkApiStatus();

// Event listeners
startForm.addEventListener('submit', handleStartVerification);
verifyForm.addEventListener('submit', handleVerifyCode);

async function checkApiStatus() {
    try {
        const response = await fetch(`${API_BASE}/docs`);
        if (response.ok) {
            apiStatus.innerHTML = '<span style="color: green;">✓ API is running</span>';
        } else {
            apiStatus.innerHTML = '<span style="color: red;">✗ API is not responding</span>';
        }
    } catch (error) {
        apiStatus.innerHTML = '<span style="color: red;">✗ Cannot connect to API</span>';
        console.error('API status check failed:', error);
    }
}

async function handleStartVerification(event) {
    event.preventDefault();

    const formData = new FormData(startForm);
    const data = {
        phone_number: formData.get('phone_number'),
        payload: formData.get('payload') || null
    };

    startResponse.innerHTML = '<div style="color: blue;">Sending verification request...</div>';

    try {
        const response = await fetch(`${API_BASE}/api/v1/verification/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            startResponse.innerHTML = `
                <div style="color: green;">
                    <strong>✓ Success!</strong><br>
                    Status: ${result.status}<br>
                    Request ID: ${result.request_id || 'N/A'}
                </div>
            `;
        } else {
            startResponse.innerHTML = `
                <div style="color: red;">
                    <strong>✗ Error:</strong><br>
                    ${result.detail || 'Unknown error'}
                </div>
            `;
        }
    } catch (error) {
        startResponse.innerHTML = `
            <div style="color: red;">
                <strong>✗ Network Error:</strong><br>
                ${error.message}
            </div>
        `;
        console.error('Start verification failed:', error);
    }
}

async function handleVerifyCode(event) {
    event.preventDefault();

    const formData = new FormData(verifyForm);
    const data = {
        phone_number: formData.get('phone_number'),
        code: formData.get('code')
    };

    verifyResponse.innerHTML = '<div style="color: blue;">Verifying code...</div>';

    try {
        const response = await fetch(`${API_BASE}/api/v1/verification/verify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            if (result.status === 'verified') {
                verifyResponse.innerHTML = `
                    <div style="color: green;">
                        <strong>✓ Phone Verified!</strong><br>
                        ${result.message}
                    </div>
                `;
            } else {
                verifyResponse.innerHTML = `
                    <div style="color: orange;">
                        <strong>⚠ Verification Failed</strong><br>
                        ${result.message}
                    </div>
                `;
            }
        } else {
            verifyResponse.innerHTML = `
                <div style="color: red;">
                    <strong>✗ Error:</strong><br>
                    ${result.detail || 'Unknown error'}
                </div>
            `;
        }
    } catch (error) {
        verifyResponse.innerHTML = `
            <div style="color: red;">
                <strong>✗ Network Error:</strong><br>
                ${error.message}
            </div>
        `;
        console.error('Verify code failed:', error);
    }
}
