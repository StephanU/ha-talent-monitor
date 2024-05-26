# Home Assistant Talent Monitor Integration

TALENT Monitoring and Management Portal (TSUN) integration for HomeAssistant using the [PyTalentMonitor](https://github.com/LenzGr/pytalent-monitor) library.

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]

[![hacs][hacsbadge]][hacs]
[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**This component will set up the following platforms.**

| Platform       | Description                                                        |
| -------------- | ------------------------------------------------------------------ |
| `sensor`       | Sensors for the PV metrics                                         |

![Dashboard Screenshot][dashboard-screenshot]

## Installation

### Via HACS

1. Install [HACS](https://hacs.xyz/docs/setup/prerequisites/)
2. Add 'https://github.com/StephanU/ha-talent-monitor' as a [Custom Repository](https://hacs.xyz/docs/faq/custom_repositories)
3. Restart Home Assistant
4. In the HA UI, go to "Settings" -> "Automations & scenes". Click "+ Add Integration" and search for "TalentMonitor"
5. Enter the username and password that you used to register your solar plant in the Talent Monitoring App

### Manually

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `talent-monitor`.
4. Download _all_ the files from the `custom_components/talent-monitor/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI, go to "Settings" -> "Automations & scenes". Click "+ Add Integration" and search for "TalentMonitor"
8. Enter the username and password that you used to register your solar plant in the Talent Monitoring App

## Configuration

Configuration is done in the UI.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/stephanu/ha-talent-monitor.svg?style=for-the-badge
[commits]: https://github.com/stephanu/ha-talent-monitor/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[dashboard-screenshot]: DashboardScreenshot.png
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/stephanu/ha-talent-monitor.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40stephanu-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/stephanu/ha-talent-monitor.svg?style=for-the-badge
[releases]: https://github.com/stephanu/ha-talent-monitor/releases
[user_profile]: https://github.com/stephanu
