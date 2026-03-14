import inspect

from utils import data_manager


def test_post_new_job_signature_is_compatible_with_page_usage():
    signature = inspect.signature(data_manager.post_new_job)
    assert list(signature.parameters.keys()) == ["job_data", "company_id"]


def test_get_applications_for_company_signature_uses_company_id():
    signature = inspect.signature(data_manager.get_applications_for_company)
    assert list(signature.parameters.keys()) == ["company_id"]


def test_send_email_to_applicant_contract():
    signature = inspect.signature(data_manager.send_email_to_applicant)
    assert list(signature.parameters.keys()) == ["application_id", "email_data"]
