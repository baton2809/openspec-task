# Briefing: задача 1.1

**Change:** add-email-validation
**Task:** 1.1 — Создать файл `src/validators.py` с классом `EmailValidator`
**Сгенерировано:** 2026-04-28
**Источник:** openspec-task-explain v1.0

---

## 1. Контекст из design.md

Задача 1.1 создаёт центральную сущность изменения — класс `EmailValidator`.

> | `EmailValidator` | `src/validators.py` | Валидация формата email по regex | `validate(email: str) -> bool` |

— design.md, раздел "Архитектура → Новые модули / классы / функции"

Решение по изоляции валидационной логики:

> **Regex вместо сторонней библиотеки** — упрощает зависимости, достаточно для бизнес-задачи. Trade-off: неполная RFC 5322 совместимость.

— design.md, раздел "Decisions"

Goals, в которые попадает задача:

> Изолировать логику валидации в отдельном классе для переиспользования.

— design.md, раздел "Goals"

---

## 2. Целевые точки в коде

| Имя | Расположение | Статус |
|---|---|---|
| `EmailValidator` | `src/validators.py` | (существует, реализация — NotImplementedError) |

Константа regex-паттерна также определяется в этом файле:

> `EMAIL_PATTERN = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'`
> Константа определяется в `src/validators.py`. Не конфигурируема извне.

— design.md, раздел "Детали реализации → Regex-паттерн"

---

## 3. Контракт

### `EmailValidator.validate`

> - **Входные параметры:** `email: str`
> - **Результат:** `True` если email валиден, `False` если формат не соответствует паттерну
> - **Ошибки:** `EmailValidationError` если `email` равен `None` или пустой строке (после strip)
> - **Побочные эффекты:** нет

— design.md, раздел "Интерфейсы / Контракты → EmailValidator.validate"

---

## 4. Применимые edge cases

Все edge cases относятся к методу `validate`, реализуемому в задаче 1.1:

> | Пустая строка `""` | Raise `EmailValidationError("Email cannot be empty")` |
> | Строка с пробелами `" "` | После `strip()` → пустая → raise `EmailValidationError("Email cannot be empty")` |
> | Email с пробелами по краям `" user@example.com "` | После `strip()` → проверить regex → вернуть результат |
> | Email длиннее 254 символов | Вернуть `False` (не raise, формат нарушен) |
> | Email без `@` (`notanemail`) | Вернуть `False` |
> | Email без домена после `@` (`user@`) | Вернуть `False` |
> | `None` | Raise `EmailValidationError("Email cannot be empty")` |

— design.md, раздел "Детали реализации → Обработка edge cases"

Важное решение про raise vs return:

> **validate возвращает bool, а не raise** — для случаев невалидного формата. Raise только для None/empty, потому что это программная ошибка (нарушение контракта), а не пользовательский ввод.

— design.md, раздел "Decisions"

---

## 5. Применимые НФТ

> - Логирование невалидных email происходит с уровнем `INFO`: `"Email validation failed: {reason}"`.

— change.md, раздел "13. Логирование"

Специфичных НФТ по производительности для задачи 1.1 в change.md не указано — применяются общепроектные требования.

---

## 6. Чеклист тестов

Из design.md, раздел "Тестирование → Unit-тесты" (строки, относящиеся к `EmailValidator.validate`):

| Метод | Сценарий |
|---|---|
| `test_valid_email_returns_true` | `user@example.com` → True |
| `test_invalid_format_returns_false` | `notanemail` → False |
| `test_empty_string_raises` | `""` → raise EmailValidationError |
| `test_email_with_spaces_stripped` | `" user@example.com "` → True |
| `test_email_too_long_returns_false` | строка 255 символов → False |

Из tasks.md, раздел "Чеклист верификации" (относящиеся к задаче 1.1):

- [ ] Регистрация с валидным email (`user@example.com`) завершается успешно
- [ ] Регистрация с email с пробелами по краям (`  user@example.com `) — пробелы обрезаются, регистрация проходит

---

## 7. Зависимости от других задач

Задача 1.1 — первая в списке. Явных пререквизитов нет.

Примечание: задача 2.1 (создать `EmailValidationError`) логически является зависимостью для полной реализации `validate` (метод raise-ит это исключение). Однако для создания класса `EmailValidator` с сигнатурой можно начать параллельно — итоговая интеграция через задачи 3.1–3.2.

---

## 8. Риски и подводные камни

> Использование упрощённого regex для проверки email: не покрывает все легальные форматы по RFC 5322 (например, `"user name"@example.com`). Trade-off принят сознательно — простота реализации важнее полноты для данного контекста.

— design.md, раздел "Risks / Trade-offs"

---

## 9. Open Questions

Нет открытых вопросов. Все решения зафиксированы в design.md раздел "Decisions".

---

## Готовность к реализации

| Секция | Статус |
|---|---|
| Контракт | ✓ определён полностью |
| Целевые точки в коде | ✓ src/validators.py (существует, нужна реализация) |
| Edge cases | ✓ специфицированы все 7 |
| НФТ | ⚠ только логирование из change.md; общие НФТ применяются по умолчанию |
| Тесты | ✓ 5 unit-сценариев из design.md |
| Зависимости | ✓ нет пререквизитов для старта |
| Риски | ✓ задокументированы |
| Open Questions | ✓ нет |

**Рекомендация:** Реализация готова к запуску `openspec-implement`.
