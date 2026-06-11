## ADDED Requirements

### Requirement: Remote repository input is validated
The GitHub installer MUST accept only a valid `owner/repo` identifier and a non-empty ref before constructing a download URL.

#### Scenario: Malformed repository argument
- **WHEN** a user passes an absolute URL, path traversal sequence, or malformed repository identifier
- **THEN** the installer exits without making a network request

### Requirement: Archive extraction is confined
The installer MUST reject ZIP entries that are absolute, contain parent traversal, or resolve outside the temporary extraction root.

#### Scenario: Malicious archive member
- **WHEN** an archive contains `../outside` or an absolute member path
- **THEN** extraction fails and no file is written outside the temporary directory

### Requirement: Downloads have bounded failure behavior
The installer SHALL use a finite network timeout and return a concise actionable error for HTTP, timeout, and invalid archive failures.

#### Scenario: Download timeout
- **WHEN** the GitHub archive request exceeds the configured timeout
- **THEN** installation exits non-zero without changing existing installed skills

### Requirement: Destination replacement is failure-safe
The installer SHALL validate all selected sources before replacing destinations and MUST restore an existing destination if replacement fails.

#### Scenario: Forced upgrade succeeds
- **WHEN** `--force` installs a valid skill over an existing destination
- **THEN** the destination contains the complete new skill and no staging or backup directory remains

#### Scenario: Replacement copy fails
- **WHEN** a failure occurs after the existing destination is moved aside
- **THEN** the previous destination is restored
