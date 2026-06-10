from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .models import Report


class NavbarRenderingTests(SimpleTestCase):
    def test_home_page_renders_visible_navbar(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<nav class="navbar navbar-expand-lg')
        self.assertContains(response, "visibility: visible !important;")
        self.assertContains(response, reverse("report_list"))
        self.assertContains(response, reverse("dashboard"))

    def test_authenticated_navbar_has_consistent_icon_and_logout_button(self):
        user = SimpleNamespace(
            is_authenticated=True,
            is_admin=True,
            username="aldi",
        )

        html = render_to_string("base.html", {"user": user})

        self.assertIn("bi-person-circle", html)
        self.assertNotIn(">account_circle<", html)
        self.assertIn(f'action="{reverse("logout")}"', html)
        self.assertIn('method="post"', html)
        self.assertIn("bi-box-arrow-right", html)
        self.assertIn("<span>Logout</span>", html)

    def test_main_templates_use_green_theme_without_legacy_blue(self):
        templates = [
            "base.html",
            "main_app/home.html",
            "main_app/report_list.html",
            "dashboard/index.html",
            "usermanagement_24782019/login.html",
            "usermanagement_24782019/register.html",
        ]
        html = "".join(render_to_string(template) for template in templates)

        self.assertIn("--agro-green: #006948", html)
        for legacy_blue in (
            "#007bff",
            "#0056b3",
            "#0d6efd",
            "#17a2b8",
            "#dbeafe",
            "#1e3a8a",
            "#dae2fd",
            "#e2e7ff",
            "#eaedff",
        ):
            self.assertNotIn(legacy_blue, html.lower())

    def test_about_and_contact_pages_render_modern_sections(self):
        about_response = self.client.get(reverse("about"))
        contact_response = self.client.get(reverse("contact"))

        self.assertEqual(about_response.status_code, 200)
        self.assertContains(about_response, "Membangun solusi digital")
        self.assertContains(about_response, "Fokus pengembangan")
        self.assertContains(about_response, "Muhammad Aldi Prasetyo")

        self.assertEqual(contact_response.status_code, 200)
        self.assertContains(contact_response, "Mari terhubung")
        self.assertContains(contact_response, "24782019@student.polinela.ac.id")
        self.assertContains(contact_response, 'rel="noopener noreferrer"', count=2)


class ReportAuthorizationTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin = user_model.objects.create_user(
            username="admin",
            password="test-pass-123",
            is_admin=True,
        )
        self.citizen = user_model.objects.create_user(
            username="citizen",
            password="test-pass-123",
            is_admin=False,
        )
        self.other_citizen = user_model.objects.create_user(
            username="other",
            password="test-pass-123",
            is_admin=False,
        )

        self.draft = self.create_report(
            "Draft Privat Aldi",
            self.citizen,
            Report.Status.DRAFT,
        )
        self.reported = self.create_report(
            "Laporan Menunggu Verifikasi",
            self.citizen,
            Report.Status.REPORTED,
        )
        self.verified = self.create_report(
            "Laporan Terverifikasi",
            self.other_citizen,
            Report.Status.VERIFIED,
        )
        self.in_progress = self.create_report(
            "Laporan Lama Diproses",
            self.other_citizen,
            Report.Status.IN_PROGRESS,
        )
        self.resolved = self.create_report(
            "Laporan Sudah Selesai",
            self.other_citizen,
            Report.Status.RESOLVED,
        )

    @staticmethod
    def report_payload(title="Laporan Diperbarui"):
        return {
            "title": title,
            "category": "Infrastruktur",
            "description": "Deskripsi laporan untuk pengujian otorisasi.",
            "location": "Politeknik Negeri Lampung",
        }

    def create_report(self, title, reporter, status):
        return Report.objects.create(
            reporter=reporter,
            status=status,
            **self.report_payload(title),
        )

    def test_admin_sees_public_workflow_reports_without_drafts(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("report_list"))

        self.assertContains(response, self.reported.title)
        self.assertContains(response, self.verified.title)
        self.assertContains(response, self.in_progress.title)
        self.assertContains(response, self.resolved.title)
        self.assertNotContains(response, self.draft.title)

    def test_draft_is_only_visible_to_its_citizen_owner(self):
        self.client.force_login(self.citizen)
        owner_list = self.client.get(reverse("report_list"))
        owner_detail = self.client.get(
            reverse("report_detail", args=[self.draft.pk])
        )

        self.assertContains(owner_list, self.draft.title)
        self.assertEqual(owner_detail.status_code, 200)

        self.client.force_login(self.other_citizen)
        other_list = self.client.get(reverse("report_list"))
        other_detail = self.client.get(
            reverse("report_detail", args=[self.draft.pk])
        )

        self.assertNotContains(other_list, self.draft.title)
        self.assertEqual(other_detail.status_code, 404)

        self.client.force_login(self.admin)
        admin_detail = self.client.get(
            reverse("report_detail", args=[self.draft.pk])
        )
        self.assertEqual(admin_detail.status_code, 404)

    def test_citizen_can_edit_delete_and_submit_only_own_draft(self):
        self.client.force_login(self.citizen)
        update_url = reverse("update_report", args=[self.draft.pk])

        response = self.client.post(
            update_url,
            {**self.report_payload("Draft Milik Sendiri"), "action": "draft"},
        )
        self.assertRedirects(response, reverse("report_list"))
        self.draft.refresh_from_db()
        self.assertEqual(self.draft.title, "Draft Milik Sendiri")
        self.assertEqual(self.draft.status, Report.Status.DRAFT)

        response = self.client.post(
            reverse("submit_report", args=[self.draft.pk])
        )
        self.assertRedirects(response, reverse("report_list"))
        self.draft.refresh_from_db()
        self.assertEqual(self.draft.status, Report.Status.REPORTED)

        locked_update = self.client.post(
            update_url,
            {**self.report_payload("Tidak Boleh Berubah"), "action": "draft"},
        )
        locked_delete = self.client.post(
            reverse("delete_report", args=[self.draft.pk])
        )

        self.assertEqual(locked_update.status_code, 404)
        self.assertEqual(locked_delete.status_code, 404)
        self.draft.refresh_from_db()
        self.assertEqual(self.draft.title, "Draft Milik Sendiri")

    def test_citizen_creates_private_draft_and_admin_cannot_create(self):
        self.client.force_login(self.citizen)
        response = self.client.post(
            reverse("add_report"),
            {**self.report_payload("Draft Baru Citizen"), "action": "draft"},
        )

        self.assertRedirects(response, reverse("report_list"))
        created_report = Report.objects.get(title="Draft Baru Citizen")
        self.assertEqual(created_report.reporter, self.citizen)
        self.assertEqual(created_report.status, Report.Status.DRAFT)

        self.client.force_login(self.admin)
        admin_response = self.client.post(
            reverse("add_report"),
            {**self.report_payload("Laporan Buatan Admin"), "action": "draft"},
        )

        self.assertRedirects(admin_response, reverse("report_list"))
        self.assertFalse(
            Report.objects.filter(title="Laporan Buatan Admin").exists()
        )

    def test_live_search_does_not_leak_private_drafts(self):
        search_url = reverse("report_search_api")

        self.client.force_login(self.other_citizen)
        other_response = self.client.get(search_url, {"q": "Draft Privat"})
        self.assertNotContains(other_response, self.draft.title)

        self.client.force_login(self.admin)
        admin_response = self.client.get(search_url, {"q": "Draft Privat"})
        self.assertNotContains(admin_response, self.draft.title)

        self.client.force_login(self.citizen)
        owner_response = self.client.get(search_url, {"q": "Draft Privat"})
        self.assertContains(owner_response, self.draft.title)

    def test_other_citizen_cannot_modify_someone_elses_draft(self):
        self.client.force_login(self.other_citizen)

        update_response = self.client.post(
            reverse("update_report", args=[self.draft.pk]),
            {**self.report_payload(), "action": "draft"},
        )
        delete_response = self.client.post(
            reverse("delete_report", args=[self.draft.pk])
        )
        submit_response = self.client.post(
            reverse("submit_report", args=[self.draft.pk])
        )

        self.assertEqual(update_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)
        self.assertEqual(submit_response.status_code, 404)

    def test_admin_can_advance_workflow_in_order_and_cannot_edit_or_delete(self):
        self.client.force_login(self.admin)

        verify_response = self.client.post(
            reverse("update_status", args=[self.reported.pk]),
            {"status": Report.Status.VERIFIED},
        )
        self.assertRedirects(verify_response, reverse("report_list"))
        self.reported.refresh_from_db()
        self.assertEqual(self.reported.status, Report.Status.VERIFIED)

        progress_response = self.client.post(
            reverse("update_status", args=[self.reported.pk]),
            {"status": Report.Status.IN_PROGRESS},
        )
        self.assertRedirects(progress_response, reverse("report_list"))
        self.reported.refresh_from_db()
        self.assertEqual(self.reported.status, Report.Status.IN_PROGRESS)

        resolve_response = self.client.post(
            reverse("update_status", args=[self.reported.pk]),
            {"status": Report.Status.RESOLVED},
        )
        self.assertRedirects(resolve_response, reverse("report_list"))
        self.reported.refresh_from_db()
        self.assertEqual(self.reported.status, Report.Status.RESOLVED)

        edit_response = self.client.post(
            reverse("update_report", args=[self.reported.pk]),
            {**self.report_payload("Admin Edit"), "action": "draft"},
        )
        delete_response = self.client.post(
            reverse("delete_report", args=[self.reported.pk])
        )
        invalid_skip = self.client.post(
            reverse("update_status", args=[self.verified.pk]),
            {"status": Report.Status.RESOLVED},
        )
        invalid_after_resolved = self.client.post(
            reverse("update_status", args=[self.reported.pk]),
            {"status": Report.Status.VERIFIED},
        )

        self.assertEqual(edit_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)
        self.assertRedirects(invalid_skip, reverse("report_list"))
        self.assertRedirects(invalid_after_resolved, reverse("report_list"))
        self.verified.refresh_from_db()
        self.reported.refresh_from_db()
        self.assertEqual(self.verified.status, Report.Status.VERIFIED)
        self.assertEqual(self.reported.status, Report.Status.RESOLVED)

    def test_api_enforces_draft_privacy_and_status_transitions(self):
        self.client.force_login(self.other_citizen)
        hidden_draft = self.client.get(f"/api/report/{self.draft.pk}/")
        self.assertEqual(hidden_draft.status_code, 404)

        self.client.force_login(self.citizen)
        submit_response = self.client.patch(
            f"/api/report/{self.draft.pk}/",
            data='{"status": "REPORTED"}',
            content_type="application/json",
        )
        self.assertEqual(submit_response.status_code, 200)

        locked_edit = self.client.patch(
            f"/api/report/{self.draft.pk}/",
            data='{"title": "Tidak Boleh Diubah"}',
            content_type="application/json",
        )
        self.assertEqual(locked_edit.status_code, 403)

        self.client.force_login(self.admin)
        verify_response = self.client.patch(
            f"/api/report/{self.draft.pk}/",
            data='{"status": "VERIFIED"}',
            content_type="application/json",
        )
        delete_response = self.client.delete(
            f"/api/report/{self.draft.pk}/"
        )

        self.assertEqual(verify_response.status_code, 200)
        progress_response = self.client.patch(
            f"/api/report/{self.draft.pk}/",
            data='{"status": "IN_PROGRESS"}',
            content_type="application/json",
        )
        resolve_response = self.client.patch(
            f"/api/report/{self.draft.pk}/",
            data='{"status": "RESOLVED"}',
            content_type="application/json",
        )
        self.assertEqual(delete_response.status_code, 403)
        self.assertEqual(progress_response.status_code, 200)
        self.assertEqual(resolve_response.status_code, 200)
