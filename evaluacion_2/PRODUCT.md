# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Backend: Django 6.1.1, Django REST Framework, PostgreSQL.
Frontend: Vistas HTML base renderizadas por Django (incluyendo el footer obligatorio con datos del alumno).

## Users

- **Estudiante**: Navega por la oferta académica, agrega cursos a su carro de matrícula y realiza el proceso de pago (checkout) para inscribirse.
- **Coordinador Académico**: Administra las áreas de conocimiento, los cursos/bootcamps y gestiona las matrículas (incluyendo la cancelación para liberar cupos).

## Product Purpose

Sistema de matriculación para una academia tecnológica que permite gestionar la oferta de cursos y bootcamps. Su objetivo principal es asegurar la persistencia del carro de compras (matrículas) y controlar de manera transaccional y atómica la disponibilidad de cupos.

## Positioning

Una plataforma EdTech que garantiza que no existan sobreventas mediante validaciones de inventario en tiempo de transacción, manteniendo el progreso de selección del estudiante incluso si cambia de sesión o dispositivo.

## Operating Context

- Autenticación y autorización basada en JSON Web Tokens (JWT) con separación de roles (RBAC).
- APIs documentadas automáticamente mediante Swagger/OpenAPI.
- Entorno educativo y de desarrollo backend evaluativo.

## Capabilities and Constraints

- **Restricciones del Carro**: Persistente, vinculado 1:1 con el usuario. Un mismo curso no puede agregarse dos veces al mismo carro.
- **Gestión de Stock**: El cupo no se descuenta al agregar al carro, sino de forma atómica en el instante en que el estado pasa a PAGADO.
- **Reposición**: Si una orden se cancela, el cupo debe liberarse y reponerse al catálogo automáticamente.
- **Visuales Obligatorias**: Todo endpoint o vista HTML debe tener un *footer* visible con el Nombre, Sección y Año del alumno que desarrolla el proyecto.

## Evidence on Hand

Documento de pauta (PDF) que especifica requerimientos técnicos de la Evaluación 2.
