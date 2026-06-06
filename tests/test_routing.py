import os
import tempfile
import unittest


class HermesGeralRoutingTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        os.environ["HERMES_GERAL_OWNER_PHONES"] = "89994315927,5589994315927"
        os.environ["HERMES_GERAL_DB_PATH"] = os.path.join(self.tmpdir.name, "test.db")
        os.environ["OPENAI_API_KEY"] = ""
        os.environ["TELEGRAM_ALLOWED_CHAT_IDS"] = ""

    def tearDown(self):
        self.tmpdir.cleanup()
        os.environ.pop("HERMES_GERAL_OWNER_PHONES", None)
        os.environ.pop("HERMES_GERAL_DB_PATH", None)
        os.environ.pop("OPENAI_API_KEY", None)
        os.environ.pop("TELEGRAM_ALLOWED_CHAT_IDS", None)

    def test_owner_phone_local_format_is_allowed(self):
        from app.config import is_owner_phone

        self.assertTrue(is_owner_phone("89994315927"))

    def test_owner_phone_international_format_is_allowed(self):
        from app.config import is_owner_phone

        self.assertTrue(is_owner_phone("+55 89 99431-5927"))

    def test_other_phone_is_blocked(self):
        from app.config import is_owner_phone

        self.assertFalse(is_owner_phone("+55 89 99999-0000"))

    def test_telegram_chat_is_allowed_when_allowlist_empty(self):
        from app.config import is_allowed_telegram_chat

        self.assertTrue(is_allowed_telegram_chat("123"))

    def test_telegram_chat_can_be_restricted(self):
        from app.config import is_allowed_telegram_chat

        os.environ["TELEGRAM_ALLOWED_CHAT_IDS"] = "123,456"
        self.assertTrue(is_allowed_telegram_chat("123"))
        self.assertFalse(is_allowed_telegram_chat("789"))

    def test_common_request_uses_common_gemini_model(self):
        from app.llm import selected_gemini_model

        os.environ["HERMES_GERAL_COMMON_MODEL"] = "gemini-2.5-flash"
        self.assertEqual(selected_gemini_model("qual e a pauta de hoje?"), "gemini-2.5-flash")

    def test_development_request_uses_dev_gemini_model(self):
        from app.llm import selected_gemini_model

        os.environ["HERMES_GERAL_DEV_MODEL"] = "gemini-3.5-flash"
        self.assertEqual(selected_gemini_model("/dev revisar arquitetura supabase"), "gemini-3.5-flash")

    def test_knowledge_accepts_query(self):
        from app.knowledge import read_knowledge

        text = read_knowledge("codex hermes")
        self.assertIn("Hermes Geral", text)

    def test_system_prompt_prioritizes_current_project_status(self):
        from app.llm import build_system_prompt

        prompt = build_system_prompt("qual o estagio do hermes pastoral?")
        self.assertIn("estado atual documentado", prompt.lower())
        self.assertIn("Chats antigos do Codex sao historico", prompt)
        self.assertIn("Hermes Pastoral 2.0 MVP concluido", prompt)

    def test_parse_codex_request_for_allowed_project(self):
        from app.local_codex import parse_codex_request

        request = parse_codex_request("/codex hermes-pastoral | rode os testes")
        self.assertEqual(request.project, "hermes-pastoral")
        self.assertIn("HERMES-LOCAL", request.workdir)
        self.assertEqual(request.prompt, "rode os testes")

    def test_parse_codex_request_blocks_unknown_project(self):
        from app.local_codex import parse_codex_request

        with self.assertRaises(ValueError):
            parse_codex_request("/codex sistema-qualquer | rode algo")

    def test_codex_command_resolves_command_name(self):
        from app.local_codex import codex_command

        self.assertTrue(codex_command())


if __name__ == "__main__":
    unittest.main()
