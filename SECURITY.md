# Security Policy

## Scope and safe use

WSProbe is an educational tool. Its scanner is intentionally limited to loopback targets (`localhost`, `127.0.0.1`, and `::1`). Run it only against the included practice server or a local service you own or have explicit permission to test.

Do not use this project to probe public hosts, third-party services, or systems without authorization. Do not remove the loopback safety check to expand scanning scope.

## Reporting a vulnerability

If you discover a security issue in this project, please do not publish exploit details before maintainers have had a reasonable opportunity to investigate. Open a private security advisory through GitHub if the repository has that feature enabled, or contact the repository owner privately. Include the affected file, reproduction steps, and potential impact.

## Limitations

A `PASS` result means only that the included lab exhibited the expected behavior for that test. It is not a certification, penetration-test report, or guarantee that another WebSocket application is secure.
