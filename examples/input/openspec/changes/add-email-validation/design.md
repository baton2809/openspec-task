# Design: add-email-validation

**Change:** add-email-validation
**Автор:** example-author
**Дата:** 2026-04-28

---

## Goals

- Добавить валидацию email в `register_user` без изменения внешнего контракта функции.
- Изолировать логику валидации в отдельном классе для переиспользования.
- Покрыть все edge cases, перечисленные в change.md раздел 10.

## Non-Goals

- Не валидировать email через DNS MX-запрос или внешний сервис.
- Не изменять схему базы данных.
- Не реализовывать полную RFC 5322 — используется упрощённый regex.

---

## Архитектура

### Изменения в коде

#### Новые модули / классы / функции

| Имя | Расположение | Назначение | Ключевые операции |
|---|---|---|---|
| `EmailValidator` | `src/validators.py` | Валидация формата email по regex | `validate(email: str) -> bool` |
| `EmailValidationError` | `src/exceptions.py` | Исключение при невалидном email | — |

#### Изменения в существующих сущностях

| Имя | Расположение | Изменение |
|---|---|---|
| `register_user` | `src/api.py` | Добавить вызов `EmailValidator().validate()` перед сохранением; при `False` — raise `EmailValidationError` |

---

## Интерфейсы / Контракты

### `EmailValidator.validate`

- **Входные параметры:** `email: str`
- **Результат:** `True` если email валиден, `False` если формат не соответствует паттерну
- **Ошибки:** `EmailValidationError` если `email` равен `None` или пустой строке (после strip)
- **Побочные эффекты:** нет

### `register_user` (изменённый контракт)

- **Входные параметры:** `email: str, name: str` (без изменений)
- **Результат:** `dict` с данными пользователя (без изменений)
- **Новые ошибки:** `EmailValidationError` при невалидном email (до любых операций с БД)

---

## Детали реализации

### Обработка edge cases

| Ситуация | Поведение `EmailValidator.validate` |
|---|---|
| Пустая строка `""` | Raise `EmailValidationError("Email cannot be empty")` |
| Строка с пробелами `" "` | После `strip()` → пустая → raise `EmailValidationError("Email cannot be empty")` |
| Email с пробелами по краям `" user@example.com "` | После `strip()` → проверить regex → вернуть результат |
| Email длиннее 254 символов | Вернуть `False` (не raise, формат нарушен) |
| Email без `@` (`notanemail`) | Вернуть `False` |
| Email без домена после `@` (`user@`) | Вернуть `False` |
| `None` | Raise `EmailValidationError("Email cannot be empty")` |

### Regex-паттерн

```
EMAIL_PATTERN = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
```

Константа определяется в `src/validators.py`. Не конфигурируема извне (см. Non-Goals).

---

## Тестирование

### Unit-тесты

| Что тестируем | Метод | Сценарий |
|---|---|---|
| `EmailValidator.validate` | `test_valid_email_returns_true` | `user@example.com` → True |
| `EmailValidator.validate` | `test_invalid_format_returns_false` | `notanemail` → False |
| `EmailValidator.validate` | `test_empty_string_raises` | `""` → raise EmailValidationError |
| `EmailValidator.validate` | `test_email_with_spaces_stripped` | `" user@example.com "` → True |
| `EmailValidator.validate` | `test_email_too_long_returns_false` | строка 255 символов → False |

### Integration-тесты

| Что тестируем | Метод | Сценарий |
|---|---|---|
| `register_user` | `test_register_with_invalid_email_raises` | `register_user("notanemail", "Bob")` → raise EmailValidationError |

---

## Decisions

- **Regex вместо сторонней библиотеки** — упрощает зависимости, достаточно для бизнес-задачи. Trade-off: неполная RFC 5322 совместимость.
- **EmailValidationError наследует Exception** — не RuntimeError и не ValueError, чтобы вызывающий код мог ловить именно ошибки валидации email без риска поймать лишнее.
- **validate возвращает bool, а не raise** — для случаев невалидного формата. Raise только для None/empty, потому что это программная ошибка (нарушение контракта), а не пользовательский ввод.

---

## Risks / Trade-offs

- Использование упрощённого regex для проверки email: не покрывает все легальные форматы по RFC 5322 (например, `"user name"@example.com`). Trade-off принят сознательно — простота реализации важнее полноты для данного контекста.

---

## Open Questions

Нет открытых вопросов. Все решения зафиксированы в Decisions.
