# Crivo Thalam CLI

Command-line interface for device authentication and management with Crivo Thalam.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install CLI globally
pip install -e .
```

## Usage

### Setup Device

Register your device and generate authorization link:

```bash
crivo-thalam setup
```

This will:
1. Collect device information (hostname, platform, etc.)
2. Register device with Crivo Thalam backend
3. Generate a unique authorization link
4. Save device configuration locally

### Check Status

Check if your device is authorized:

```bash
crivo-thalam status
```

### View Configuration

Show current device configuration:

```bash
crivo-thalam info
```

### Reset Configuration

Reset device configuration:

```bash
crivo-thalam reset
```

## Configuration

The CLI stores device configuration in `~/.crivo_thalam/device.json`

Set API URL (optional):
```bash
export CRIVO_API_URL=http://localhost:8000
```

## Device Authorization Flow

1. **Install CLI** on your device
2. **Run setup**: `crivo-thalam setup`
3. **Get authorization link** from CLI output
4. **Open link in browser** and sign in to your Crivo Thalam account
5. **Authorize device** in the web interface
6. **Check status**: `crivo-thalam status` to confirm authorization

## Commands

- `crivo-thalam setup` - Setup and register device
- `crivo-thalam status` - Check authorization status
- `crivo-thalam info` - Show device configuration
- `crivo-thalam reset` - Reset device configuration
- `crivo-thalam --help` - Show help message

## Requirements

- Python 3.7+
- Active internet connection
- Crivo Thalam backend running

## Example

```bash
$ crivo-thalam setup
╭─────────────────────────────────────────╮
│ Crivo Thalam Device Setup               │
│ This will register your device and      │
│ generate an authorization link.         │
╰─────────────────────────────────────────╯

Collecting device information...

✓ Device registered successfully!

╭─────────────────────────────────────────╮
│ Authorization Required                   │
│                                         │
│ Please visit this link to authorize:   │
│ http://localhost:3000/authorize/abc123  │
╰─────────────────────────────────────────╯

$ crivo-thalam status
Device Status: ⚠ Pending Authorization
```

## Troubleshooting

**Connection Error:**
- Make sure the backend is running at the configured API URL
- Check your internet connection

**Device Not Found:**
- Run `crivo-thalam setup` to register the device

**Already Configured:**
- Run `crivo-thalam reset` to start fresh