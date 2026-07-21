import time

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse


class FileUploadSizeLimitTests(TestCase):
    """Тесты для view handle_file_upload: проверка ограничения размера файла."""

    def test_small_file_uploads_successfully(self):
        """Файл меньше лимита (5000 байт) должен успешно загрузиться и вернуть 200."""
        small_file = SimpleUploadedFile(
            "small.txt", b"x" * 5000, content_type="text/plain"
        )
        response = self.client.post(
            reverse("requestdataapp:file_upload"), {"myfile": small_file}
        )
        self.assertEqual(response.status_code, 200)

    def test_big_file_is_rejected(self):
        """Файл больше лимита (15000 байт) должен быть отклонён с кодом 400 без сохранения."""
        big_file = SimpleUploadedFile(
            "big.txt", b"x" * 15000, content_type="text/plain"
        )
        response = self.client.post(
            reverse("requestdataapp:file_upload"), {"myfile": big_file}
        )
        self.assertEqual(response.status_code, 400)


class ThrottlingMiddlewareTests(TestCase):
    """Тесты для ThrottlingMiddleware: проверка ограничения частоты запросов по IP."""

    def test_second_immediate_request_is_blocked(self):
        """Второй запрос сразу после первого (быстрее RATE_LIMIT_SECONDS) должен вернуть 429."""
        client = Client()
        first = client.get(reverse("requestdataapp:file_upload"))
        second = client.get(reverse("requestdataapp:file_upload"))

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 429)

    def test_request_after_delay_is_allowed(self):
        """Запрос, отправленный после паузы больше RATE_LIMIT_SECONDS, должен снова вернуть 200."""
        client = Client()
        client.get(reverse("requestdataapp:file_upload"))
        time.sleep(2.1)
        second = client.get(reverse("requestdataapp:file_upload"))

        self.assertEqual(second.status_code, 200)
