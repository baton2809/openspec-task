# openspec-task-explain

> VibeCoding Challenge #4 — SDD: "One-shot"
> Уровень: **Advanced**
> Деливерабл: **скилл для GigaCode CLI**, дополняющий пайплайн OpenSpec Skills (Сбер).

## Идея

В существующем пайплайне OpenSpec Skills есть разрыв между шагами `design` и `implement`: разработчик, открывший задачу `[ ] 2.1 Реализовать X` в `tasks.md`, не имеет фокусированного контекста по этой задаче и вынужден читать `change.md` + `design.md` + `tasks.md` целиком. Скилл `openspec-task-explain` закрывает этот разрыв: для одной выбранной задачи он собирает structured briefing — что делать, где, какие контракты и edge cases применимы, какие тесты нужны.

**Дифференциатор от существующего `openspec-implement`:** наш скилл не пишет код. Он готовит человека к написанию кода, цитируя релевантные фрагменты спеки. Это закрывает зону, где обычно теряется контекст между планом и реализацией.

## Структура репозитория

```
openspec-task-explain/
├── SPEC.md                ← главная спецификация (передавалась в GigaCode)
├── PROMPT.md              ← один промпт, который был дан GigaCode CLI
├── REVIEW.md              ← честный разбор: что сработало / додумал / провалилось
├── README.md              ← этот файл
├── skills/
│   └── openspec-task-explain/
│       ├── SKILL.md       ← результат one-shot генерации GigaCode
│       └── templates/
│           └── briefing.md
└── examples/
    ├── input/             ← Python-проект с подготовленными change.md, design.md, tasks.md
    └── expected-output/   ← эталонный briefing, который должен был получиться
```

## Как это собрано (one-shot)

1. Написана `SPEC.md` — спецификация скилла в формате максимально близком к существующим OpenSpec Skills.
2. Подготовлен `examples/input/` — мини Python-проект с openspec-структурой и заполненными change.md/design.md/tasks.md (этот шаг сделан **до** запуска GigaCode и не входит в one-shot).
3. В GigaCode CLI скормлен `PROMPT.md` — единственный промпт.
4. GigaCode сгенерировал `skills/openspec-task-explain/SKILL.md` и `templates/briefing.md`.
5. **Никаких правок и итераций после запуска.**
6. Запущен сгенерированный скилл на `examples/input/`. Результат сравнён с `examples/expected-output/`.
7. Написан `REVIEW.md`.

## Применимость

- В Сбере: устанавливается через `gigacode extensions install` рядом с другими `openspec-*` скиллами.
- В open-source: формат скилла совместим с Claude Code, Qwen Code, OpenCode (по образцу установки OpenSpec Skills).
- Для команды разработки: даёт каждому разработчику возможность за 1 команду получить агрегированный контекст по задаче, не теряя минут на чтение всех артефактов.

## Что предлагается сделать дальше (вне рамок челленджа)

- `openspec-verify` — скилл проверки соответствия кода спецификации после реализации
- `openspec-task-tdd` — вариант скилла с автоматической генерацией теста перед реализацией
- Интеграция с `mcp-jira` — обогащение briefing данными из тикета (требует MCP)
