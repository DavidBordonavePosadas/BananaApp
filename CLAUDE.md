# CLAUDE.md — BananaApp

## Contexto del proyecto

Aplicación web para administrar una empresa productora y comercializadora de
plátano en Veracruz, México. Digitaliza procesos manejados manualmente.
También es proyecto de portafolio profesional del desarrollador.

## Stack (obligatorio, no cambiar)

- Frontend: Next.js 15 + Tailwind CSS + TypeScript strict
- Backend: Python + Django + Django REST Framework
- Base de datos: PostgreSQL
- Auth: djangorestframework-simplejwt
- Deploy: Railway
- IDE: VS Code + Claude Code

## Módulos

1. Control de cosechas (parcelas + cosechas)
2. Control de trabajadores y actividades
3. Historial de precios
4. Clientes y ventas (pago siempre al contado)
5. Insumos (tipos de insumo + compras)
6. Notas internas
7. Dashboard con métricas y gráficas

## Modelo de datos

Ver `docs/BananaApp.mmd` para el diagrama completo.

Entidades: USUARIO, PARCELA, COSECHA, HISTORIAL_PRECIO, TRABAJADOR,
ACTIVIDAD, REGISTRO_TRABAJO, CLIENTE, VENTA, TIPO_INSUMO, COMPRA_INSUMO, NOTA.

Decisiones clave:
- HISTORIAL_PRECIO sin FK (snapshot pattern)
- total y total_estimado son calculados, no almacenados
- VENTA: pago siempre al contado — sin monto_pagado ni estado_pago
- ACTIVIDAD es tabla normalizada, no enum
- parcela_id obligatorio en REGISTRO_TRABAJO
- FKs con PROTECT, excepto parcela_id en REGISTRO_TRABAJO (SET_NULL)
- TIPO_INSUMO precargado con 8 categorías base

## Estructura del monorepo

BananaApp/
├── backend/           # Django
├── frontend/          # Next.js
├── docs/              # ERD y diagramas
├── .github/workflows/ # GitHub Actions
├── CLAUDE.md
├── .gitignore
└── README.md

Estructura por app Django:

apps/<nombre>/
├── models.py
├── serializers.py
├── views.py        # ViewSets DRF
├── services.py     # lógica de negocio
├── urls.py
├── admin.py
└── tests/

## Decisiones de arquitectura

- Next.js desacoplado consumiendo API REST de Django
- JWT: access token en memoria, refresh en cookie httpOnly
- Settings divididos: base.py, dev.py, prod.py
- Custom user model: AbstractUser + campo rol (ADMIN/OPERADOR)
- Commits: Conventional Commits (feat:, fix:, docs:, chore:, refactor:)

## Estilo de código

- Python: ruff + black, type hints, pytest
- TypeScript: strict mode, eslint + prettier
- Commits atómicos, nunca commitear .env

## Estado del proyecto

Fase 0 (diseño) ✅ completada
Fase 1 (scaffolding) ✅ completada

### Fases
1. ✅ Diseño y arquitectura
2. ✅ Scaffolding inicial
3. Módulo Precios
4. Módulo Cosechas + Parcelas
5. Módulo Clientes + Ventas
6. Módulo Trabajadores
7. Dashboard + reportes
8. Deploy en Railway

## Notas

- Portafolio: README profesional, commits limpios, docs/ completo
- No cambiar el stack sin razón técnica sólida