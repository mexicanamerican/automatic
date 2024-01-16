# Security & Privacy Policy

<br>

## Issues

All issues are tracked publicly on GitHub: <https://github.com/vladmandic/automatic/issues>

<br>

## Vulnerabilities

`SD.Next` code base and included dependencies are undergoes automatic scanning for known security vulnerabilities to ensure that it follows best practices for security and privacy

Any code commit is validated before merge

- [Dependencies](https://github.com/vladmandic/automatic/security/dependabot)
- [Scanning Alerts](https://github.com/vladmandic/automatic/security/code-scanning)

<br>

## Privacy

`SD.Next` app:

- Is fully self-contained and does not send or share data of any kind with external targets
- Does not store any user or system data tracking, user-provided inputs (such as images, video), or detection results to ensure user privacy
- Does not utilize any analytic services (such as Google Analytics) to maintain the privacy of user data

`SD.Next` library can establish external connections *only* for following purposes and *only* when explicitly configured by user:

- Download extensions and themes indexes from automatically updated indexes  
- Download required packages and repositories from GitHub during installation/upgrade
- Download installed/enabled extensions
- Download models from CivitAI and/or Huggingface when instructed by user
- Submit benchmark info upon user interaction  
