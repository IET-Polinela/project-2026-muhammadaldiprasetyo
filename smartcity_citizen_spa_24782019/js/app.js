let currentTab = 'my_reports';
let currentPage = 1;
let editingReportId = null;
let reportModalInstance = null;

function setupDashboard() {
    currentTab = 'my_reports';
    currentPage = 1;
    editingReportId = null;

    const btnNewReport = document.getElementById('btnOpenReportModal');
    const tabMyReports = document.getElementById('tabMyReports');
    const tabFeed = document.getElementById('tabFeed');
    const saveDraftButton = document.getElementById('saveDraftButton');
    const submitReportButton = document.getElementById('submitReportButton');

    const modalEl = document.getElementById('reportModal');
    if (modalEl) {
        reportModalInstance = new bootstrap.Modal(modalEl, { backdrop: 'static' });
    }

    btnNewReport?.addEventListener('click', openReportModal);
    tabMyReports?.addEventListener('click', () => switchDashboardTab('my_reports'));
    tabFeed?.addEventListener('click', () => switchDashboardTab('feed'));
    saveDraftButton?.addEventListener('click', () => submitReport('DRAFT'));
    submitReportButton?.addEventListener('click', () => submitReport('REPORTED'));

    loadDashboardData(currentTab, currentPage);
}

function switchDashboardTab(tab) {
    currentTab = tab;
    currentPage = 1;

    document.getElementById('tabMyReports')?.classList.toggle('active', tab === 'my_reports');
    document.getElementById('tabFeed')?.classList.toggle('active', tab === 'feed');
    document.getElementById('listTitle').textContent = tab === 'my_reports' ? 'Laporan Saya' : 'Feed Kota';
    document.getElementById('listSubtitle').textContent = tab === 'my_reports'
        ? 'Data laporan akan dimuat dari backend setiap halaman secara terpisah.'
        : 'Feed publik menampilkan laporan terbaru dari warga lain dengan nama anonim.';
    document.getElementById('currentTabBadge').textContent = tab;

    loadDashboardData(tab, 1);
}

async function loadDashboardData(tab = 'my_reports', page = 1) {
    currentTab = tab;
    currentPage = page;

    const listContainer = document.getElementById('listContainer');
    const paginationContainer = document.getElementById('paginationContainer');

    if (listContainer) {
        listContainer.innerHTML = `
            <div class="col-12 text-center py-5 text-muted">
                <div class="spinner-border text-success" role="status"></div>
                <div class="mt-3">Memuat data laporan...</div>
            </div>
        `;
    }

    try {
        const response = await requestAPI(`/api/report/?tab=${tab}&page=${page}`);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            const message = errorData.detail || 'Gagal memuat data laporan.';
            throw new Error(message);
        }

        const data = await response.json();
        renderList(data.results || []);
        renderPagination(data);
        await loadSummaryStats();
    } catch (error) {
        if (listContainer) {
            listContainer.innerHTML = `
                <div class="col-12 text-center py-5 text-danger">
                    <p class="mb-0">${error.message}</p>
                </div>
            `;
        }
        console.error('loadDashboardData:', error);
    }
}

function statusBadgeInfo(status) {
    switch (status) {
        case 'DRAFT':
            return { label: 'Draft', color: 'secondary', progress: 18 };
        case 'REPORTED':
            return { label: 'Reported', color: 'secondary', progress: 25 };
        case 'VERIFIED':
            return { label: 'Verified', color: 'primary', progress: 50 };
        case 'IN_PROGRESS':
            return { label: 'In Progress', color: 'warning', progress: 75 };
        case 'RESOLVED':
            return { label: 'Resolved', color: 'success', progress: 100 };
        default:
            return { label: status, color: 'dark', progress: 25 };
    }
}

function renderList(reports = []) {
    const listContainer = document.getElementById('listContainer');
    if (!listContainer) return;

    if (reports.length === 0) {
        listContainer.innerHTML = `
            <div class="col-12">
                <div class="alert alert-info mb-0">
                    Tidak ada laporan untuk ditampilkan pada tab saat ini.
                </div>
            </div>
        `;
        return;
    }

    listContainer.innerHTML = reports.map((report) => {
        const statusInfo = statusBadgeInfo(report.status);
        const draftActions = report.is_owner && report.status === 'DRAFT';

        return `
            <div class="col-12">
                <div class="card card-custom shadow-sm border-0">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-3 gap-3">
                            <div>
                                <h5 class="card-title mb-1">${report.title}</h5>
                                <p class="text-muted small mb-0">${report.category} • ${report.location}</p>
                            </div>
                            <span class="badge bg-${statusInfo.color} text-white py-2 px-3">${statusInfo.label}</span>
                        </div>
                        <p class="card-text text-secondary">${report.description}</p>
                        <div class="mb-3">
                            <div class="d-flex justify-content-between small mb-1">
                                <span>Progress laporan</span>
                                <strong>${statusInfo.label}</strong>
                            </div>
                            <div class="progress" style="height: 10px;">
                                <div class="progress-bar bg-${statusInfo.color}" role="progressbar" style="width: ${statusInfo.progress}%;" aria-valuenow="${statusInfo.progress}" aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                        </div>
                        <div class="d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center gap-3">
                            <div class="text-muted small">
                                <div>Pelapor: <span class="fw-semibold text-dark">${report.reporter}</span></div>
                                <div>Terakhir diubah: ${new Date(report.updated_at).toLocaleString('id-ID')}</div>
                            </div>
                            <div class="d-flex gap-2 flex-wrap">
                                ${draftActions ? `<button type="button" class="btn btn-sm btn-outline-secondary" onclick="editDraft(${report.id})">Edit Draft</button>` : ''}
                                ${draftActions ? `<button type="button" class="btn btn-sm btn-outline-success" onclick="submitDraft(${report.id})">Ajukan</button>` : ''}
                                ${draftActions ? `<button type="button" class="btn btn-sm btn-outline-danger" onclick="deleteDraft(${report.id})">Hapus</button>` : ''}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function renderPagination(data) {
    const paginationContainer = document.getElementById('paginationContainer');
    if (!paginationContainer) return;

    const totalItems = data.count || 0;
    const pageSize = 10;
    const pageCount = Math.ceil(totalItems / pageSize);

    if (pageCount <= 1) {
        paginationContainer.innerHTML = '';
        return;
    }

    const pages = Array.from({ length: pageCount }, (_, i) => i + 1);
    paginationContainer.innerHTML = `
        <ul class="pagination pagination-sm justify-content-center mb-0">
            ${pages.map((page) => `
                <li class="page-item ${page === currentPage ? 'active' : ''}">
                    <button type="button" class="page-link" ${page === currentPage ? 'disabled' : ''} onclick="loadDashboardData('${currentTab}', ${page})">${page}</button>
                </li>
            `).join('')}
        </ul>
    `;
}

async function loadSummaryStats() {
    const draftCountEl = document.getElementById('sidebarDraftCount');
    const reportedCountEl = document.getElementById('sidebarReportedCount');
    const verifiedCountEl = document.getElementById('sidebarVerifiedCount');
    const inProgressCountEl = document.getElementById('sidebarInProgressCount');
    const resolvedCountEl = document.getElementById('sidebarResolvedCount');

    try {
        const response = await requestAPI(`/api/report/?tab=my_reports&page_size=1000`);
        if (!response.ok) {
            return;
        }

        const data = await response.json();
        const reports = data.results || [];

        const draftCount = reports.filter((item) => item.status === 'DRAFT').length;
        const reportedCount = reports.filter((item) => item.status === 'REPORTED').length;
        const verifiedCount = reports.filter((item) => item.status === 'VERIFIED').length;
        const inProgressCount = reports.filter((item) => item.status === 'IN_PROGRESS').length;
        const resolvedCount = reports.filter((item) => item.status === 'RESOLVED').length;

        if (draftCountEl) draftCountEl.textContent = draftCount;
        if (reportedCountEl) reportedCountEl.textContent = reportedCount;
        if (verifiedCountEl) verifiedCountEl.textContent = verifiedCount;
        if (inProgressCountEl) inProgressCountEl.textContent = inProgressCount;
        if (resolvedCountEl) resolvedCountEl.textContent = resolvedCount;
    } catch (error) {
        console.error('loadSummaryStats:', error);
    }
}

function openReportModal() {
    const modalTitle = document.getElementById('reportModalLabel');
    const reportForm = document.getElementById('reportForm');
    if (!reportModalInstance || !reportForm || !modalTitle) return;

    editingReportId = null;
    reportForm.reset();
    modalTitle.textContent = 'Tambah Laporan Baru';
    reportModalInstance.show();
}

async function editDraft(id) {
    try {
        const response = await requestAPI(`/api/report/${id}/`);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Gagal mengambil data draft.');
        }

        const data = await response.json();
        editingReportId = id;

        document.getElementById('reportTitle').value = data.title || '';
        document.getElementById('reportCategory').value = data.category || '';
        document.getElementById('reportLocation').value = data.location || '';
        document.getElementById('reportDescription').value = data.description || '';
        document.getElementById('reportModalLabel').textContent = 'Edit Draft Laporan';

        if (reportModalInstance) {
            reportModalInstance.show();
        }
    } catch (error) {
        console.error('editDraft:', error);
        alert(error.message);
    }
}

async function submitReport(statusValue) {
    const title = document.getElementById('reportTitle')?.value.trim();
    const category = document.getElementById('reportCategory')?.value.trim();
    const location = document.getElementById('reportLocation')?.value.trim();
    const description = document.getElementById('reportDescription')?.value.trim();

    if (!title || !category || !location || !description) {
        alert('Silakan lengkapi semua kolom sebelum menyimpan laporan.');
        return;
    }

    const payload = {
        title,
        category,
        location,
        description,
        status: statusValue,
    };

    const endpoint = editingReportId ? `/api/report/${editingReportId}/` : '/api/report/';
    const method = editingReportId ? 'PUT' : 'POST';

    try {
        const response = await requestAPI(endpoint, method, payload);
        if (response.status === 200 || response.status === 201) {
            if (reportModalInstance) {
                reportModalInstance.hide();
            }
            document.getElementById('reportForm')?.reset();
            editingReportId = null;
            await loadDashboardData(currentTab, 1);
            alert('Laporan berhasil disimpan.');
            return;
        }

        const errorData = await response.json().catch(() => ({}));
        const errorText = errorData.detail || JSON.stringify(errorData);
        throw new Error(errorText);
    } catch (error) {
        console.error('submitReport:', error);
        alert(`Gagal menyimpan laporan: ${error.message}`);
    }
}

async function submitDraft(id) {
    if (!confirm('Apakah Anda yakin ingin mengajukan draft ini sekarang?')) return;

    try {
        const response = await requestAPI(`/api/report/${id}/`, 'PATCH', { status: 'REPORTED' });
        if (response.ok) {
            await loadDashboardData(currentTab, currentPage);
            alert('Draft berhasil diajukan ke status REPORTED.');
            return;
        }

        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Gagal mengajukan draft.');
    } catch (error) {
        console.error('submitDraft:', error);
        alert(error.message);
    }
}

async function deleteDraft(id) {
    if (!confirm('Hapus laporan draft ini? Tindakan ini tidak dapat dibatalkan.')) return;

    try {
        const response = await requestAPI(`/api/report/${id}/`, 'DELETE');
        if (response.ok || response.status === 204) {
            await loadDashboardData(currentTab, currentPage);
            alert('Draft berhasil dihapus.');
            return;
        }

        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Gagal menghapus draft.');
    } catch (error) {
        console.error('deleteDraft:', error);
        alert(error.message);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    if (typeof handleRouting === 'function') {
        handleRouting();
    }
});
