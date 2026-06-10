function setupLoginForm() {
    const form = document.getElementById('loginForm');
    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); 

        const usernameInput = document.getElementById('loginUsername').value;
        const passwordInput = document.getElementById('loginPassword').value;

        const payload = { username: usernameInput, password: passwordInput };

        try {
            const response = await requestAPI('/api/token/', 'POST', payload);
            if (response.status === 200) {
                const data = await response.json();
                
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                localStorage.setItem('logged_user', usernameInput); 
                
                alert('Login Berhasil!');
                window.location.hash = '#dashboard'; 
            } else {
                const errData = await response.json();
                alert(`Login Gagal: ${errData.detail || 'Username atau password salah!'}`);
            }
        } catch (error) {
            console.error('Proses autentikasi bermasalah:', error);
        }
    });
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('logged_user');
    alert('Anda telah keluar dari sistem.');
    window.location.hash = '#login';
}

function setupRegisterForm() {

    const form =
        document.getElementById(
            'registerForm'
        );

    if (!form) return;

    form.addEventListener(
        'submit',
        async function (event) {

            event.preventDefault();

            const payload = {
                username:
                    document.getElementById(
                        'registerUsername'
                    ).value,

                email:
                    document.getElementById(
                        'registerEmail'
                    ).value,

                password:
                    document.getElementById(
                        'registerPassword'
                    ).value
            };

            try {

                const response =
                    await registerCitizen(
                        payload
                    );

                if (
                    response.status === 201
                ) {

                    alert(
                        'Registrasi berhasil. Silakan login.'
                    );

                    window.location.hash =
                        '#login';

                } else {

                    const data =
                        await response.json();

                    alert(
                        JSON.stringify(
                            data
                        )
                    );

                }

            } catch (error) {

                console.error(error);

            }

        }
    );

}