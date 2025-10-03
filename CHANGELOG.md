# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0](https://github.com/tiffany-co/backend/releases/tag/v1.5.0) - 2025-10-03
### Added
- some unit tests
### Fixed
- account ledger create

## [1.4.0](https://github.com/tiffany-co/backend/releases/tag/v1.4.0) - 2025-10-01
### Added
- investment system
### Fixed
- delete transaction

## [1.3.0](https://github.com/tiffany-co/backend/releases/tag/v1.3.0) - 2025-09-30
### Added
- backup system

## [1.2.0](https://github.com/tiffany-co/backend/releases/tag/v1.2.0) - 2025-09-29
### Added
- refresh token

## [1.1.0](https://github.com/tiffany-co/backend/releases/tag/v1.1.0) - 2025-09-29
### Added
- seeding demo data for new enities
- a temporary make command for faster testing
- new items in inventory and items
- timestamp range search feature for payment
### Changed
- current user udpate schema
- total price format in transaction items
### Fixed
- payment system work cycle

## [1.0.0](https://github.com/tiffany-co/backend/releases/tag/v1.0.0) - 2025-09-27
### Added
- payment system
- account ledger entity
### Changed
- inventory update system
- approval status shared between transaction and payment

## [0.5.0](https://github.com/tiffany-co/backend/releases/tag/v0.5.0) - 2025-09-24
### Added
- transaction system
### Fixed
- inventory service

## [0.4.0](https://github.com/tiffany-co/backend/releases/tag/v0.4.0) - 2025-09-19
### Added
- central audit log system

## [0.3.0](https://github.com/tiffany-co/backend/releases/tag/v0.3.0) - 2025-09-18
### Added
- inventory entity

## [0.2.0](https://github.com/tiffany-co/backend/releases/tag/v0.2.0) - 2025-09-16
### Added
- item entity
- item financial profile entity
- Shared item and inventory file for easier matching
- Creating a mechanism to make Persian information display more professional
- truncate database
- seed database with demo informations
### Changed
- permission entity
- get all users endpoint permission shape

## [0.1.0](https://github.com/tiffany-co/backend/releases/tag/v0.1.0) - 2025-09-10
### Added
- structure of fastapi project including model, schema, service, repository, controller
- user entity
- contact entity
- saved bank account entity
- permissioning system + admin/user role
- extra scripts like `create admin` and ...
