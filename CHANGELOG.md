# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--template
## *major.minor.patch* - *ISO-8601 date*
### Added
### Fixed
### Changed
### Removed
-->

## 1.1.0 - 2026-06-06

### Added

- Added reaction to messages for keywords 普通（ふつう） and あたりまえ
  (from [栞 / MyGO!!!!!][], the ending song of anime *BanG Dream It's MyGO!!!!!*),
  similar to existing one to 一生 that [1.0.0](#100---2025-11-24) adds.

## 1.0.1 - 2025-11-25

### Fixed

- Fixed an issue running on Linux machine via container due to interaction between symbolic links and bind mounts.

## 1.0.0 - 2025-11-24

### Added

- Added channel registering cog for registering/unregistering/testing the channel to send reactions this bot does.
- Added reaction to messages for keyword 一生（いっしょう） and its variant by forwarding matching message to registered channel.
- Added version cog for checking this bot's version.

[栞 / MyGO!!!!!]: https://www.youtube.com/watch?v=wuUZjdiUCj0
