"""
Provides the `cmdeploy` entry point function,
along with command line option and subcommand parsing.
"""

import argparse
import importlib.resources
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
from pathlib import Path

import pyinfra
from chatmaild.config import read_config, write_initial_config
from packaging import version
from termcolor import colored

from . import dns, remote
from .sshexec import SSHExec

#
# cmdeploy sub commands and options
#


def init_cmd_options(parser):
    parser.add_argument(
        "chatmail_domain",
        action="store",
        help="fully qualified DNS domain name for your chatmail instance",
    )


def init_cmd(args, out):
    """Initialize chatmail config file."""
    mail_domain = args.chatmail_domain
    if args.inipath.exists():
        print(f"Path exists, not modifying: {args.inipath}")
        return 1
    else:
        write_initial_config(args.inipath, mail_domain, overrides={})
        out.green(f"created config file for {mail_domain} in {args.inipath}")


def run_cmd_options(parser):
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="don't actually modify the server",
    )
    parser.add_argument(
        "--disable-mail",
        dest="disable_mail",
        action="store_true",
        help="install/upgrade the server, but disable postfix & dovecot for now",
    )
    parser.add_argument(
        "--ssh-host",
        dest="ssh_host",
        help="specify an SSH host to deploy to; uses mail_domain from chatmail.ini by default",
    )


def run_cmd(args, out):
    """Deploy chatmail services on the remote server."""

    sshexec = args.get_sshexec()
    require_iroh = args.config.enable_iroh_relay
    remote_data = dns.get_initial_remote_data(sshexec, args.config.mail_domain)
    if not dns.check_initial_remote_data(remote_data, print=out.red):
        return 1

    env = os.environ.copy()
    env["CHATMAIL_INI"] = args.inipath
    env["CHATMAIL_DISABLE_MAIL"] = "True" if args.disable_mail else ""
    env["CHATMAIL_REQUIRE_IROH"] = "True" if require_iroh else ""
    deploy_path = importlib.resources.files(__package__).joinpath("deploy.py").resolve()
    pyinf = "pyinfra --dry" if args.dry_run else "pyinfra"
    ssh_host = args.config.mail_domain if not args.ssh_host else args.ssh_host
    cmd = f"{pyinf} --ssh-user root {ssh_host} {deploy_path} -y"
    if version.parse(pyinfra.__version__) < version.parse("3"):
        out.red("Please re-run scripts/initenv.sh to update pyinfra to version 3.")
        return 1

    try:
        retcode = out.check_call(cmd, env=env)
        if retcode == 0:
            print("\nYou can try out the relay by talking to this echo bot: ")
            sshexec = SSHExec(args.config.mail_domain, verbose=args.verbose)
            print(
                sshexec(
                    call=remote.rshell.shell,
                    kwargs=dict(command="cat /var/lib/echobot/invite-link.txt"),
                )
            )
            out.green("Deploy completed, call `cmdeploy dns` next.")
        elif not remote_data["acme_account_url"]:
            out.red("Deploy completed but letsencrypt not configured")
            out.red("Run 'cmdeploy run' again")
            retcode = 0
        else:
            out.red("Deploy failed")
    except subprocess.CalledProcessError:
        out.red("Deploy failed")
        retcode = 1
    return retcode


def dns_cmd_options(parser):
    parser.add_argument(
        "--zonefile",
        dest="zonefile",
        type=pathlib.Path,
        default=None,
        help="write out a zonefile",
    )


def dns_cmd(args, out):
    """Check DNS entries and optionally generate dns zone file."""
    sshexec = args.get_sshexec()
    remote_data = dns.get_initial_remote_data(sshexec, args.config.mail_domain)
    if not remote_data:
        return 1

    if not remote_data["acme_account_url"]:
        out.red("could not get letsencrypt account url, please run 'cmdeploy run'")
        return 1

    if not remote_data["dkim_entry"]:
        out.red("could not determine dkim_entry, please run 'cmdeploy run'")
        return 1

    zonefile = dns.get_filled_zone_file(remote_data)

    if args.zonefile:
        args.zonefile.write_text(zonefile)
        out.green(f"DNS records successfully written to: {args.zonefile}")
        return 0

    retcode = dns.check_full_zone(
        sshexec, remote_data=remote_data, zonefile=zonefile, out=out
    )
    return retcode


def status_cmd(args, out):
    """Display status for online chatmail instance."""

    sshexec = args.get_sshexec()

    out.green(f"chatmail domain: {args.config.mail_domain}")
    if args.config.privacy_mail:
        out.green("privacy settings: present")
    else:
        out.red("no privacy settings")

    for line in sshexec(remote.rshell.get_systemd_running):
        print(line)


def test_cmd_options(parser):
    parser.add_argument(
        "--slow",
        dest="slow",
        action="store_true",
        help="also run slow tests",
    )


def test_cmd(args, out):
    """Run local and online tests for chatmail deployment.

    This will automatically pip-install 'deltachat' if it's not available.
    """

    x = importlib.util.find_spec("deltachat")
    if x is None:
        out.check_call(f"{sys.executable} -m pip install deltachat")

    pytest_path = shutil.which("pytest")
    pytest_args = [
        pytest_path,
        "cmdeploy/src/",
        "-n4",
        "-rs",
        "-x",
        "-v",
        "--durations=5",
    ]
    if args.slow:
        pytest_args.append("--slow")
    ret = out.run_ret(pytest_args)
    return ret


def fmt_cmd_options(parser):
    parser.add_argument(
        "--check",
        "-c",
        action="store_true",
        help="only check but don't fix problems",
    )


def fmt_cmd(args, out):
    """Run formattting fixes on all chatmail source code."""

    sources = [str(importlib.resources.files(x)) for x in ("chatmaild", "cmdeploy")]
    format_args = [shutil.which("ruff"), "format"]
    check_args = [shutil.which("ruff"), "check"]

    if args.check:
        format_args.append("--diff")
    else:
        check_args.append("--fix")

    if not args.verbose:
        check_args.append("--quiet")
        format_args.append("--quiet")

    format_args.extend(sources)
    check_args.extend(sources)

    out.check_call(" ".join(format_args), quiet=not args.verbose)
    out.check_call(" ".join(check_args), quiet=not args.verbose)


def bench_cmd(args, out):
    """Run benchmarks against an online chatmail instance."""
    args = ["pytest", "--pyargs", "cmdeploy.tests.online.benchmark", "-vrx"]
    cmdstring = " ".join(args)
    out.green(f"[$ {cmdstring}]")
    subprocess.check_call(args)


def webdev_cmd(args, out):
    """Run local web development loop for static web pages."""
    from .www import main

    main()


#
# Parsing command line options and starting commands
#


class Out:
    """Convenience output printer providing coloring."""

    def red(self, msg, file=sys.stderr):
        print(colored(msg, "red"), file=file)

    def green(self, msg, file=sys.stderr):
        print(colored(msg, "green"), file=file)

    def __call__(self, msg, red=False, green=False, file=sys.stdout):
        color = "red" if red else ("green" if green else None)
        print(colored(msg, color), file=file)

    def check_call(self, arg, env=None, quiet=False):
        if not quiet:
            self(f"[$ {arg}]", file=sys.stderr)
        return subprocess.check_call(arg, shell=True, env=env)

    def run_ret(self, args, env=None, quiet=False):
        if not quiet:
            cmdstring = " ".join(args)
            self(f"[$ {cmdstring}]", file=sys.stderr)
        proc = subprocess.run(args, env=env, check=False)
        return proc.returncode


def add_config_option(parser):
    parser.add_argument(
        "--config",
        dest="inipath",
        action="store",
        default=Path("chatmail.ini"),
        type=Path,
        help="path to the chatmail.ini file",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        dest="verbose",
        action="store_true",
        default=False,
        help="provide verbose logging",
    )


def add_subcommand(subparsers, func):
    name = func.__name__
    assert name.endswith("_cmd")
    name = name[:-4]
    doc = func.__doc__.strip()
    help = doc.split("\n")[0].strip(".")
    p = subparsers.add_parser(name, description=doc, help=help)
    p.set_defaults(func=func)
    add_config_option(p)
    return p


description = """
Setup your chatmail server configuration and
deploy it via SSH to your remote location.
"""


def get_parser():
    """Return an ArgumentParser for the 'cmdeploy' CLI"""

    parser = argparse.ArgumentParser(description=description.strip())
    subparsers = parser.add_subparsers(title="subcommands")

    # find all subcommands in the module namespace
    glob = globals()
    for name, func in glob.items():
        if name.endswith("_cmd"):
            subparser = add_subcommand(subparsers, func)
            addopts = glob.get(name + "_options")
            if addopts is not None:
                addopts(subparser)

    return parser


def main(args=None):
    """Provide main entry point for 'cmdeploy' CLI invocation."""
    parser = get_parser()
    args = parser.parse_args(args=args)
    if not hasattr(args, "func"):
        return parser.parse_args(["-h"])

    def get_sshexec():
        print(f"[ssh] login to {args.config.mail_domain}")
        return SSHExec(args.config.mail_domain, verbose=args.verbose)

    args.get_sshexec = get_sshexec

    out = Out()
    kwargs = {}
    if args.func.__name__ not in ("init_cmd", "fmt_cmd"):
        if not args.inipath.exists():
            out.red(f"expecting {args.inipath} to exist, run init first?")
            raise SystemExit(1)
        try:
            args.config = read_config(args.inipath)
        except Exception as ex:
            out.red(ex)
            raise SystemExit(1)

    try:
        res = args.func(args, out, **kwargs)
        if res is None:
            res = 0
        return res
    except KeyboardInterrupt:
        out.red("KeyboardInterrupt")
        sys.exit(130)


if __name__ == "__main__":
    main()
