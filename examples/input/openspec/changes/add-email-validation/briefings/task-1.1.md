# Briefing: задача 1.1

**Change:** add-email-validation
**Task:** 1.1 — Создать файл `src/validators.py` с классом `EmailValidator`
**Сгенерировано:** 2026-04-28
**Источник:** openspec-task-explain v1.0

---

## 1. Контекст из design.md

> Цель — изолировать логику валидации в отдельном классе для переиспользования.
> — design.md, раздел "Goals"

> **Новые модули / классы / функции**
> | Имя | Расположение | Назначение | Ключевые операции |
> |---|---|---|
> | `EmailValidator` | `src/validators.py` | Валидация формата email по regex | `validate(email: str) -> bool` |
> — design.md, раздел "Архитектура → Изменения в коде"

> **Regex-паттерн**
> ```
> EMAIL_PATTERN = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
> ```
> Константа определяется в `src/validators.py`. Не конфигурируема извне (см. Non-Goals).
> — design.md, раздел "Детали реализации"

---

## 2. Целевые точки в коде

| Имя | Расположение | Назначение | Статус |
|---|---|---|---|
| `EmailValidator` | `src/validators.py` | Валидация формата email по regex | (существует, требует доработки) |

---

## 3. Контракт

> **`EmailValidator.validate`**
> - **Входные параметры:** `email: str`
> - **Результат:** `True` если email валиден, `False` если формат не соответствует паттерну
> - **Ошибки:** `EmailValidationError` если `email` равен `None` или пустой строке (после strip)
> - **Побочные эффекты:** нет
> — design.md, раздел "Интерфейсы / Контракты"

---

## 4. Применимые edge cases

> | Ситуация | Поведение `EmailValidator.validate` |
> |---|---|
> | Пустая строка `""` | Raise `EmailValidationError("Email cannot be empty")` |
> | Строка с пробелами `" "` | После `strip()` → пустая → raise `EmailValidationError("Email cannot be empty")` |
> | Email с пробелами по краям `" user@example.com "` | После `strip()` → проверить regex → вернуть результат |
> | Email длиннее 254 символов | Вернуть `False` (не raise, формат нарушен) |
> | Email без `@` (`notanemail`) | Вернуть `False` |
> | Email без домена после `@` (`user@`) | Вернуть `False` |
> | `None` | Raise `EmailValidationError("Email cannot be empty")` |
> — design.md, раздел "Обработка edge cases"

---

## 5. Применимые НФТ

Специфичных НФТ для задачи в change.md не указано — применяются общепроектные требования.

---

## 6. Чеклист тестов

### Unit-тесты

> | Что тестируем | Метод | Сценарий |
> |---|---|---|
> | `EmailValidator.validate` | `test_valid_email_returns_true` | `user@example.com` → True |
> | `EmailValidator.validate` | `test_invalid_format_returns_false` | `notanemail` → False |
> | `EmailValidator.validate` | `test_empty_string_raises` | `""` → raise EmailValidationError |
> | `EmailValidator.validate` | `test_email_with_spaces_stripped` | `" user@example.com "` → True |
> | `EmailValidator.validate` | `test_email_too_long_returns_false` | строка 255 символов → False |
> — design.md, раздел "Тестирование → Unit-тесты"

### Integration-тесты

> | Что тестируем | Метод | Сценарий |
> |---|---|---|
> | `register_user` | `test_register_with_invalid_email_raises` | `register_user("notanemail", "Bob")` → raise EmailValidationError |
> — design.md, раздел "Тестирование → Integration-тесты"

### Чеклист верификации (из tasks.md)

> **Альтернативные сценарии**
> - [ ] Регистрация с email с пробелами по краям (` user@example.com `) — пробелы обрезаются, регистрация проходит
>
> **Ошибочные сценарии**
> - [ ] Регистрация с пустым email (`""`) возвращает `EmailValidationError`
> - [ ] Регистрация с email без `@` (`notanemail`) возвращает `EmailValidationError`
> - [ ] Регистрация с `None` вместо email возвращает `EmailValidationError`
> — tasks.md, раздел "Чеклист верификации"

---

## 7. Зависимости от других задач

Явные зависимости в tasks.md не специфицированы.

---

## 8. Риски и подводные камни

> **Risks / Trade-offs**
> Использование упрощённого regex для проверки email: не покрывает все легальные форматы по RFC 5322 (например, `"user name"@example.com`). Trade-off принят сознательно — простота реализации важнее полноты для данного контекста.
> — design.md, раздел "Risks / Trade-offs"

---

## 9. Open Questions

> **Decisions**
> - **Regex вместо сторонней библиотеки** — упрощает зависимости, достаточно для бизнес-задачи. Trade-off: неполная RFC 5322 совместимость.
> - **EmailValidationError наследует Exception** — не RuntimeError и не ValueError, чтобы вызывающий код мог ловить именно ошибки валидации email без риска поймать лишнее.
> - **validate возвращает bool, а не raise** — для случаев невалидного формата. Raise только для None/empty, потому что это программная ошибка (нарушение контракта), а не пользовательский ввод.
> — design.md, раздел "Decisions"

---

## Готовность к реализации

- ✓ Контракт определён
- ✓ Edge cases специфицированы
- ✓ Тесты полностью описаны
- ✗ Целевые точки в коде частично указаны (файл существует, но метод не реализован)

### Рекомендация

Реализация ВОЗМОЖНА после ответа на N открытых вопросов.

### Next Steps

- Прочитай briefing полностью
- Ответь на Open Questions (если есть) и обнови design.md
- Запусти `openspec-implement` или работай руками по briefing
