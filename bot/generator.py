import asyncio
import json
import logging
import anthropic
from typing import Tuple

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Ты — мастер prompt engineering для Claude (Anthropic). Превращаешь сырые запросы в максимально эффективные промпты.

## ПРИНЦИПЫ Claude 4.x

**Буквальность**: Claude выполняет ТОЧНО то, что написано. Не угадывает намерение.
- ❌ "Напиши посты" → 1 пост без деталей
- ✅ "Напиши 3 поста для Instagram, 150-200 слов, тон — дружелюбный эксперт"

**Scope**: Применяет инструкцию строго к указанному объёму, не обобщает.

## МАСТЕР-ФОРМУЛА (используй для Варианта 1)

[РОЛЬ] Ты — [эксперт в области X с конкретным опытом].

<task>
[Точная задача: что сделать, сколько, с какими параметрами]
</task>

<context>
[Кто клиент, ситуация, бизнес-контекст, что важно знать]
</context>

<examples>
Хорошо: [конкретный пример желаемого результата]
Плохо: [антипример — чего НЕ нужно]
</examples>

<constraints>
- [Ограничение 1]
- [Ограничение 2]
</constraints>

<output_format>
Формат: [списки / параграфы / таблица / JSON]
Длина: [краткий / развёрнутый / X слов]
Язык и тон: [русский / английский, деловой / дружелюбный / экспертный]
</output_format>

Думай системно перед ответом.

## КОМПАКТНЫЙ ВАРИАНТ 2

Та же суть, без XML, в виде чётких инструкций:
РОЛЬ: ...
ЗАДАЧА: ...
КОНТЕКСТ: ...
ПРИМЕРЫ: Хорошо — ... / Плохо — ...
ФОРМАТ: ...
Думай системно.

## ПРАВИЛА КАЧЕСТВА

- Роль даёт Claude экспертизу и контекст → качество растёт
- Позитивные примеры ("делай так") эффективнее запретов ("не делай")
- Негативные примеры нужны для определения границ — предотвращают over-triggering
- Формат вывода: всегда указывай явно (длина, структура, тон)
- Важное — в начало или конец промпта, не в середину
- "Думай системно" активирует extended thinking

Генерируй промпты на языке пользователя, если не указано иное."""


class PromptGenerator:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def _call(self, **kwargs) -> str:
        """Synchronous API call — runs in a thread pool."""
        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    async def get_clarifying_questions(self, user_request: str) -> str:
        text = await asyncio.to_thread(
            self._call,
            model="claude-sonnet-4-6",
            max_tokens=200,
            system=(
                "Определи: нужны ли уточняющие вопросы для создания хорошего промпта.\n\n"
                "Задавай вопросы ТОЛЬКО если без них промпт будет слишком размытым.\n"
                "НЕ задавай если: задача понятна, контекст угадывается, деталей достаточно.\n"
                "Максимум — 2 коротких вопроса в одном сообщении.\n\n"
                "Если вопросы НЕ нужны → ответь ровно одним словом: НЕТ\n"
                "Если нужны → напиши только вопросы, без вводных фраз."
            ),
            messages=[{"role": "user", "content": f"Запрос: {user_request}"}],
        )
        if text.strip().upper().startswith(("НЕТ", "NO")):
            return ""
        return text.strip()

    async def generate_two_variants(self, original: str, clarifications: str = "") -> Tuple[str, str]:
        user_content = f"Запрос пользователя: {original}"
        if clarifications:
            user_content += f"\nУточнения: {clarifications}"
        user_content += (
            "\n\nСгенерируй два готовых промпта.\n"
            "Вариант 1 — полная структура с XML-тегами.\n"
            "Вариант 2 — компактный без XML.\n\n"
            "Ответь строго в JSON (не добавляй текст до/после):\n"
            '{"v1": "...", "v2": "..."}'
        )

        text = await asyncio.to_thread(
            self._call,
            model="claude-sonnet-4-6",
            max_tokens=3000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
        )
        return self._parse_response(text)

    async def apply_edits(self, v1: str, v2: str, instruction: str) -> Tuple[str, str]:
        text = await asyncio.to_thread(
            self._call,
            model="claude-sonnet-4-6",
            max_tokens=3000,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": (
                    f"ВАРИАНТ 1:\n{v1}\n\n"
                    f"ВАРИАНТ 2:\n{v2}\n\n"
                    f"ПРАВКА: {instruction}\n\n"
                    "Обнови оба варианта с учётом правки. Строго в JSON:\n"
                    '{"v1": "...", "v2": "..."}'
                ),
            }],
        )
        return self._parse_response(text)

    def _parse_response(self, text: str) -> Tuple[str, str]:
        text = text.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            try:
                data = json.loads(text[start:end])
                v1 = data.get("v1") or data.get("variant1", "")
                v2 = data.get("v2") or data.get("variant2", "")
                if v1 and v2:
                    return str(v1), str(v2)
            except json.JSONDecodeError:
                logger.warning("JSON parse failed, using text fallback")

        for marker in ["ВАРИАНТ 2", "Вариант 2", "---", "===ВАРИАНТ 2==="]:
            if marker in text:
                parts = text.split(marker, 1)
                return parts[0].strip(), parts[1].strip()

        mid = len(text) // 2
        return text[:mid].strip(), text[mid:].strip()
