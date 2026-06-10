const BASE_URL = 'http://103.151.63.71:8002'; 

async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    const url = `${BASE_URL}${endpoint}`;
    const headers = { 'Content-Type': 'application/json' };

    const token = localStorage.getItem('access_token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = { method: method, headers: headers };

    if (bodyData && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        config.body = JSON.stringify(bodyData);
    }

    try {
        const response = await fetch(url, config);
        if (response.status === 401 && window.location.hash !== '#login') {
            logout();
        }
        return response;
    } catch (error) {
        console.error('Terjadi kesalahan Fetch API:', error);
        alert('Gagal terhubung dengan server backend Django!');
        throw error;
    }
}
