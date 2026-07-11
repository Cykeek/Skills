# Remote Development

Run workspaces on remote hosts or local containers via SSH or Docker.

## SSH Connection
Configure:
| Field | Description |
|---|---|
| **Host** | Remote server address |
| **Port** | SSH port (default 22) |
| **Username** | SSH login user |
| **Authentication** | Password or private key |
| **Download method** | How to transfer ZCode to the remote host |

## Docker Connection
- Select a running container from the list.
- Or input a container name/id manually.
- Uses `docker exec` and `docker cp` for access.

## Use Cases
- Projects requiring remote servers or GPUs.
- Development inside isolated containers.
- File editing, terminal, Git, and Agent tasks all execute remotely.

## Prerequisites
- SSH access to the remote host or local Docker daemon.
- Remote hosts need `curl`, `tar`, and `sha256sum` installed.

## FAQ
- **SSH alias not showing?** Config may be malformed — check SSH config file syntax.
- **"Download on remote server" fails?** Remote host needs internet access.
- **Can Mobile Remote Control create new SSH/Docker connections?** No — must be created from the desktop app.
