# Contributing

Contributions that improve clarity, correctness, test coverage, or safe local learning are welcome.

## Before opening a change

1. Keep scanner targets restricted to loopback addresses.
2. Add or update unit tests for behavior changes.
3. Keep examples local and use clearly fictional test data.
4. Update the README or Urdu guide when commands or behavior change.
5. Never commit virtual environments, Python cache files, credentials, or generated personal reports.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

Describe the purpose of the change, the tests you ran, and any limitations in your pull request.
