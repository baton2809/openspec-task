# Tasks: add-email-validation

**Change:** add-email-validation
**Design:** openspec/changes/add-email-validation/design.md
**Статус:** В реализации
**Автор:** example-author
**Дата:** 2026-04-28

---

## Задачи

### 1. Создать EmailValidator

- [ ] 1.1 Создать файл `src/validators.py` с классом `EmailValidator`
- [ ] 1.2 Реализовать метод `validate(email: str) -> bool` через regex-паттерн `EMAIL_PATTERN`

### 2. Добавить исключение

- [ ] 2.1 Создать класс `EmailValidationError(Exception)` в `src/exceptions.py`

### 3. Интегрировать валидацию в API

- [ ] 3.1 Импортировать `EmailValidator` и `EmailValidationError` в `src/api.py`
- [ ] 3.2 Добавить вызов `EmailValidator().validate(email)` в `register_user` перед сохранением; при `False` — raise `EmailValidationError`

### 4. Покрыть тестами

- [ ] 4.1 Unit-тесты для `EmailValidator.validate` (5 сценариев из design.md)
- [ ] 4.2 Integration-тест для `register_user` с невалидным email

---

## Чеклист верификации

### Основной сценарий

- [ ] Регистрация с валидным email (`user@example.com`) завершается успешно и возвращает данные пользователя

### Альтернативные сценарии

- [ ] Регистрация с email с пробелами по краям (` user@example.com `) — пробелы обрезаются, регистрация проходит

### Ошибочные сценарии

- [ ] Регистрация с пустым email (`""`) возвращает `EmailValidationError`
- [ ] Регистрация с email без `@` (`notanemail`) возвращает `EmailValidationError`
- [ ] Регистрация с `None` вместо email возвращает `EmailValidationError`

### Нефункциональные требования

- [ ] Метод `validate` выполняется за < 1 мс на типичном email
- [ ] Логирование невалидных email происходит с уровнем `INFO`
