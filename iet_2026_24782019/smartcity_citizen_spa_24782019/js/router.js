// 1. Definisi template HTML: Login (Biru Default) vs Dashboard (Hijau Agro City)
const routes = {
    '#login': `
        <div class="row justify-content-center mt-5">
            <div class="col-md-4 card card-custom shadow-sm border-0 p-4">
                <div class="text-center mb-4">
                    <i class="bi bi-buildings-fill text-primary fs-1"></i>
                    <h4 class="fw-bold mt-2 text-dark">Login Warga</h4>
                    <p class="text-muted small">Silakan masuk menggunakan akun portal warga anda</p>
                </div>
                <form id="loginForm">
                    <div class="mb-3">
                        <input type="text" id="loginUsername" class="form-control" placeholder="Username" required>
                    </div>
                    <div class="mb-3">
                        <input type="password" id="loginPassword" class="form-control" placeholder="Password" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100 fw-bold card-custom">Masuk</button>
                </form>
            </div>
        </div>
    `,
    '#dashboard': `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card card-custom border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <button class="btn btn-success btn-lg w-100 fw-bold mb-3 card-custom shadow-sm">
                        <i class="bi bi-plus-circle-fill me-2"></i>Mulai Lapor
                    </button>
                    <div class="list-group list-group-flush small">
                        <a href="#dashboard" class="list-group-item list-group-item-action active rounded border-0 bg-success mb-1">
                            <i class="bi bi-grid-1x2-fill me-2"></i>Dashboard Utama
                        </a>
                    </div>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div class="card card-custom border-0 p-5 shadow-sm text-center text-muted border-dashed bg-white">
                    <i class="bi bi-patch-check-fill fs-1 text-success mb-3"></i>
                    <h5 class="fw-bold text-dark">Selamat Datang di Portal Citizen!</h5>
                    <p class="small text-secondary px-md-4">
                        Koneksi data API laporan agrikultur dan infrastruktur digital akan diimplementasikan penuh pada modul Lab 12 mendatang.
                    </p>
                </div>
            </section>

            <aside class="col-lg-3 d-none d-lg-block">
                <div class="card card-custom border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <h6 class="fw-bold text-success mb-3">
                        <i class="bi bi-info-circle-fill me-2"></i>Layanan Unggulan
                    </h6>
                    <div class="p-2 border-start border-success border-3 bg-light mb-2 rounded-end small">
                        <span class="fw-bold d-block">24/7 Monitoring</span>
                        <span class="text-muted">Pelaporan infrastruktur agrikultur real-time.</span>
                    </div>
                    <div class="p-2 border-start border-success border-3 bg-light mb-2 rounded-end small">
                        <span class="fw-bold d-block">Dukungan Akademik</span>
                        <span class="text-muted">Teknologi Rekayasa Internet POLINELA.</span>
                    </div>
                </div>
            </aside>
        </div>
    `
};

// 2. Fungsi Pengendali Navigasi Konten & Perubahan Warna Tema Tema
function handleRouting() {
    const hash = window.location.hash || '#login';
    const appContent = document.getElementById('app-content');
    const mainNavbar = document.getElementById('main-navbar');
    const navbarTitle = document.getElementById('navbar-title');
    const navMenus = document.getElementById('nav-menus');
    
    // Pasang HTML dasar ke halaman
    appContent.innerHTML = routes[hash] || routes['#login'];

    if (hash === '#login') {
        // KONDISI LOGIN: Kembalikan ke Biru Default Modul
        mainNavbar.className = "navbar navbar-expand-lg navbar-dark bg-primary shadow-sm navbar-transition";
        navbarTitle.innerHTML = `<i class="bi bi-buildings-fill me-2"></i> Smart City Portal`;
        navMenus.innerHTML = ''; 
        
        // Atur background body kembali ke abu-abu terang bawaan
        document.body.style.backgroundColor = "#f4f6f9";

        if (typeof setupLoginForm === 'function') {
            setupLoginForm();
        }
    } else if (hash === '#dashboard') {
        // Proteksi Halaman: Wajib lempar ke login jika tidak ada token JWT
        const token = localStorage.getItem('access_token');
        if (!token) {
            window.location.hash = '#login';
            return;
        }

        // KONDISI DASHBOARD: Ubah jadi Hijau Agro City
        mainNavbar.className = "navbar navbar-expand-lg navbar-dark bg-success shadow-sm navbar-transition";
        navbarTitle.innerHTML = `<i class="bi bi-tree-fill me-2"></i> AGRO CITY`;
        
        // Sesuaikan background body agar senada dengan web Agro City utama
        document.body.style.backgroundColor = "#f4f6f3";

        // Ambil data user login dari memori lokal
        const loggedUser = localStorage.getItem('logged_user') || 'Warga Agro City';

        // Tampilkan Identitas Akun di Kanan Navbar mirip screenshot web Agro City-mu
        navMenus.innerHTML = `
            <div class="d-flex align-items-center gap-3">
                <span class="badge bg-light text-success px-3 py-2 rounded-pill fw-bold shadow-sm d-flex align-items-center">
                    <i class="bi bi-person-circle me-2 fs-6"></i> ${loggedUser}
                </span>
                <button class="btn btn-outline-light btn-sm fw-bold px-3 py-1.5 rounded-pill shadow-sm" onclick="logout()">
                    <i class="bi bi-box-arrow-right me-1"></i> Keluar
                </button>
            </div>
        `;
    }
}

window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);