// 1. Definisi template HTML: Login dan Dashboard memakai tema hijau Agro City
const routes = {
    '#login': `
        <section class="login-shell">
            <div class="login-panel">
                <div class="row g-0">
                    <div class="col-lg-5 d-none d-lg-block">
                        <div class="login-brand-side h-100">
                            <div class="position-relative z-1">
                                <div class="login-brand-mark mb-4">
                                    <i class="bi bi-tree-fill"></i>
                                </div>
                                <p class="text-uppercase fw-bold small mb-3 opacity-75">Agro City Citizen Portal</p>
                                <h1 class="display-6 fw-bold lh-sm mb-4">Pantau dan ajukan laporan kota hijau dengan mudah.</h1>
                                <p class="mb-4 opacity-75">Masuk sebagai warga untuk menyimpan draft, mengajukan laporan, dan memantau progress laporan secara real-time.</p>
                                <div class="login-feature">
                                    <i class="bi bi-shield-check"></i>
                                    <span>Draft laporan privat hanya terlihat oleh pemilik akun.</span>
                                </div>
                                <div class="login-feature">
                                    <i class="bi bi-activity"></i>
                                    <span>Workflow laporan transparan dari Reported sampai Resolved.</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-7">
                        <div class="login-form-side">
                            <div class="login-icon mb-4">
                                <i class="bi bi-person-circle"></i>
                            </div>
                            <p class="text-uppercase fw-bold text-success small mb-2">Portal Warga</p>
                            <h2 class="fw-bold mb-2">Login Warga Agro City</h2>
                            <p class="text-muted mb-4">Gunakan akun citizen untuk masuk ke dashboard laporan warga.</p>
                            <form id="loginForm">
                                <div class="input-with-icon mb-3">
                                    <i class="bi bi-person-fill"></i>
                                    <input type="text" id="loginUsername" class="form-control" placeholder="Username" autocomplete="username" required>
                                </div>
                                <div class="input-with-icon mb-4">
                                    <i class="bi bi-key-fill"></i>
                                    <input type="password" id="loginPassword" class="form-control" placeholder="Password" autocomplete="current-password" required>
                                </div>
                                <button type="submit" class="btn btn-success w-100 fw-bold card-custom py-3">
                                    <i class="bi bi-box-arrow-in-right me-2"></i>Masuk ke Dashboard
                                </button>
                            </form>
                            <div class="mt-4 p-3 rounded-4 bg-light border border-success-subtle">
                                <div class="d-flex gap-3 align-items-start">
                                    <i class="bi bi-info-circle-fill text-success mt-1"></i>
                                    <p class="small text-muted mb-0">Setelah login, Anda dapat membuat draft laporan dan mengajukannya ke admin ketika sudah siap.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    `,
    '#dashboard': `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card card-custom border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <button id="btnOpenReportModal" class="btn btn-success btn-lg w-100 fw-bold mb-3 card-custom shadow-sm">
                        <i class="bi bi-plus-circle-fill me-2"></i>Tambah Laporan Baru
                    </button>
                    <div class="mb-4 p-3 rounded-4 bg-light border border-1 border-success">
                        <h6 class="fw-bold text-success mb-3">Rekap Status Laporan</h6>
                        <div class="d-flex justify-content-between mb-2">
                            <span class="small">Draft</span>
                            <strong id="sidebarDraftCount">0</strong>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span class="small">Reported</span>
                            <strong id="sidebarReportedCount">0</strong>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span class="small">Verified</span>
                            <strong id="sidebarVerifiedCount">0</strong>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span class="small">In Progress</span>
                            <strong id="sidebarInProgressCount">0</strong>
                        </div>
                        <div class="d-flex justify-content-between">
                            <span class="small">Resolved</span>
                            <strong id="sidebarResolvedCount">0</strong>
                        </div>
                    </div>
                    <div class="list-group list-group-flush small">
                        <button id="tabMyReports" class="list-group-item list-group-item-action active rounded mb-1 text-start">
                            <i class="bi bi-person-fill me-2"></i>Laporan Saya
                        </button>
                        <button id="tabFeed" class="list-group-item list-group-item-action rounded text-start">
                            <i class="bi bi-globe2 me-2"></i>Feed Kota
                        </button>
                    </div>
                </div>
            </aside>
            <section class="col-12 col-lg-9">
                <div class="card card-custom border-0 p-4 shadow-sm bg-white">
                    <div class="d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center mb-4">
                        <div>
                            <h5 class="fw-bold mb-1" id="listTitle">Laporan Saya</h5>
                            <p class="text-muted small mb-0" id="listSubtitle">Data laporan akan dimuat dari backend setiap halaman secara terpisah.</p>
                        </div>
                        <span class="badge bg-success py-2 px-3" id="currentTabBadge">my_reports</span>
                    </div>
                    <div id="listContainer" class="row g-3"></div>
                    <nav id="paginationContainer" class="mt-4"></nav>
                </div>
            </section>
        </div>

        <div class="modal fade" id="reportModal" tabindex="-1" aria-labelledby="reportModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <div>
                            <h5 class="modal-title fw-bold" id="reportModalLabel">Tambah Laporan Baru</h5>
                            <p class="text-muted small mb-0">Isi formulir berikut untuk membuat atau mengedit laporan tanpa reload.</p>
                        </div>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Tutup"></button>
                    </div>
                    <div class="modal-body">
                        <form id="reportForm">
                            <div class="mb-3">
                                <label for="reportTitle" class="form-label">Judul Laporan</label>
                                <input type="text" id="reportTitle" class="form-control" placeholder="Contoh: Jalan rusak di RT 05" required>
                            </div>
                            <div class="row g-3 mb-3">
                                <div class="col-md-6">
                                    <label for="reportCategory" class="form-label">Kategori</label>
                                    <input type="text" id="reportCategory" class="form-control" placeholder="Kategori laporan" required>
                                </div>
                                <div class="col-md-6">
                                    <label for="reportLocation" class="form-label">Lokasi</label>
                                    <input type="text" id="reportLocation" class="form-control" placeholder="Nama lokasi atau alamat" required>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="reportDescription" class="form-label">Deskripsi Lengkap</label>
                                <textarea id="reportDescription" class="form-control" rows="5" placeholder="Ceritakan kondisi masalah secara rinci" required></textarea>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Batal</button>
                        <button type="button" id="saveDraftButton" class="btn btn-outline-primary">Simpan Draft</button>
                        <button type="button" id="submitReportButton" class="btn btn-success">Ajukan</button>
                    </div>
                </div>
            </div>
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
        mainNavbar.className = "navbar navbar-expand-lg navbar-dark agro-navbar shadow-sm navbar-transition";
        navbarTitle.innerHTML = `<i class="bi bi-tree-fill me-2"></i> AGRO CITY Citizen`;
        navMenus.innerHTML = '';
        document.body.style.backgroundColor = "#f4f8f5";

        if (typeof setupLoginForm === 'function') {
            setupLoginForm();
        }
    } else if (hash === '#dashboard') {
        const token = localStorage.getItem('access_token');
        if (!token) {
            window.location.hash = '#login';
            return;
        }

        mainNavbar.className = "navbar navbar-expand-lg navbar-dark agro-navbar shadow-sm navbar-transition";
        navbarTitle.innerHTML = `<i class="bi bi-tree-fill me-2"></i> AGRO CITY`;
        document.body.style.backgroundColor = "#f4f6f3";

        const loggedUser = localStorage.getItem('logged_user') || 'Warga Agro City';
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

        if (typeof setupDashboard === 'function') {
            setupDashboard();
        }
    }
}

window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);
