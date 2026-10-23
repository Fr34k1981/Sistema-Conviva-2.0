import unittest
from unittest.mock import patch

from src.access_control import _is_production, can_delete, classify_email


class ClassifyEmailTests(unittest.TestCase):
    def test_staff_email_is_case_insensitive(self):
        context = classify_email("STAFF@example.com", ["staff@example.com"], {})

        self.assertEqual(context.role, "staff")
        self.assertEqual(context.email, "staff@example.com")

    def test_parent_is_limited_to_mapped_student(self):
        context = classify_email("parent@example.com", [], {"parent@example.com": "RA-123"})

        self.assertEqual(context.role, "parent")
        self.assertEqual(context.student_ra, "RA-123")

    def test_manager_email_has_separate_role(self):
        context = classify_email("manager@example.com", [], {}, ["manager@example.com"])

        self.assertEqual(context.role, "manager")

    def test_staff_identity_uses_configured_teacher_name(self):
        context = classify_email(
            "teacher@example.com",
            ["teacher@example.com"],
            {},
            teacher_accounts={"teacher@example.com": "Professora Ana"},
        )

        self.assertEqual(context.teacher_name, "Professora Ana")

    def test_unlisted_email_is_denied(self):
        context = classify_email("unknown@example.com", [], {})

        self.assertEqual(context.role, "unauthorized")

    def test_cloud_runtime_cannot_be_switched_to_development(self):
        with patch("src.access_control.Path.resolve") as resolve:
            resolve.return_value.as_posix.return_value = "/mount/src/conviva/src/access_control.py"
            with patch.dict("os.environ", {"APP_ENV": "development"}):
                self.assertTrue(_is_production())

    def test_empty_parent_mapping_is_denied(self):
        context = classify_email("parent@example.com", [], {"parent@example.com": "  "})

        self.assertEqual(context.role, "unauthorized")

    def test_staff_can_delete_only_own_tutoring_rows(self):
        own_row = can_delete("staff", "tutoria", ["professora", "ra"], ["Professora Ana", "001"], "Professora Ana")
        other_row = can_delete("staff", "tutoria", ["professora", "ra"], ["Professor Beto", "002"], "Professora Ana")

        self.assertTrue(own_row)
        self.assertFalse(other_row)

    def test_staff_cannot_delete_administrative_rows(self):
        allowed = can_delete("staff", "alunos", ["ra"], ["001"], "Professora Ana")

        self.assertFalse(allowed)

    def test_manager_can_delete_administrative_rows(self):
        allowed = can_delete("manager", "alunos", ["ra"], ["001"])

        self.assertTrue(allowed)

    def test_sync_exception_is_limited_to_structured_tutoring_tables(self):
        allowed_sync = can_delete("staff", "tutoria_individual", [], [], allow_sync=True)
        disallowed_sync = can_delete("staff", "alunos", [], [], allow_sync=True)

        self.assertTrue(allowed_sync)
        self.assertFalse(disallowed_sync)


if __name__ == "__main__":
    unittest.main()