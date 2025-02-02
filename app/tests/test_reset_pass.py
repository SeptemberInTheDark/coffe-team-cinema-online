from unittest import mock

import pytest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException

from app.routers.v1.reset_pass import request_password_reset
from app.routers.v1.reset_pass import generate_reset_code, is_valid_email, send_email_reset_code


# Тест для генерации кода сброса пароля
def test_generate_reset_code():
    reset_code = generate_reset_code()
    assert len(reset_code) == 8


# Тест для проверки валидного email
def test_is_valid_email_valid():
    assert is_valid_email("test@example.com") is True


# Тест для проверки невалидного email
def test_is_valid_email_invalid():
    assert is_valid_email("invalid-email") is False


# Мокаем SMTP для отправки email
@patch("smtplib.SMTP_SSL")
def test_send_email_reset_code(mock_smtp):
    mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
    mock_smtp_instance.send_message.return_value = None

    with patch("app.controllers.reset_pass_controller.get_email_template") as mock_get_email:
        # Вызов тестируемой функции
        send_email_reset_code("test@example.com", "123456", "TestUser")


# Тест на обработку ошибки при отправке email
@patch("smtplib.SMTP_SSL")
def test_send_email_reset_code_exception(mock_smtp):
    mock_smtp_instance = mock_smtp.return_value
    mock_smtp_instance.send_message.side_effect = Exception("SMTP error")

    with patch("app.controllers.reset_pass_controller.get_email_template") as mock_get_email:
        mock_get_email.return_value = mock.Mock()
        send_email_reset_code("test@example.com", "123456", "TestUser")


# Тест на случай, когда пользователь не найден
@pytest.mark.asyncio
@patch("app.crud.crud_user.UserCRUD.get_user", new_callable=AsyncMock)
async def test_request_password_reset_user_not_found(mock_get_user):
    mock_get_user.return_value = None  # Эмулируем, что пользователь не найден

    with pytest.raises(HTTPException) as exc_info:
        await request_password_reset(email="test@example.com", db=mock.Mock())

    assert exc_info.value.status_code == 404
    mock_get_user.assert_called_once_with(email="test@example.com")


# Тест на невалидный email при запросе на сброс пароля
@pytest.mark.asyncio
async def test_request_password_reset_invalid_email():
    with pytest.raises(HTTPException) as exc_info:
        await request_password_reset(email="invalid-email", db=mock.Mock())

    assert exc_info.value.status_code == 400
