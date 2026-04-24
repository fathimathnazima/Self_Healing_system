import json
import time

from monitor import is_running
from recovery import restart_service
from logger import log

from stats import (
    update_failure,
    get_stats,
    get_risk_level,
    is_unstable,
    update_last_seen
)

from alert import show_alert
from email_alert import send_failure_email

from colorama import Fore, Style, init


init()


# Check every 60 seconds
CHECK_INTERVAL = 60


print("\n=== SELF-HEALING SYSTEM STARTED ===\n")


# Load services config
with open("config.json") as f:
    config = json.load(f)

services = config["services"]

silent = config.get(
    "silent",
    False
)


# Continuous monitoring loop
while True:

    print(
        "\n----- Running Health Check -----\n"
    )


    for service in services:

        name = service["name"]

        command = service["start_command"]



        # -------------------------
        # FAILURE DETECTED
        # -------------------------
        if not is_running(name):

            update_failure(name)

            stats = get_stats(
                name
            )

            failures = stats["failures"]

            risk = get_risk_level(
                failures
            )


            if not silent:

                print(
                    Fore.RED +
                    f"❌ {name} restarted "
                    f"(Failures:{failures}, Risk:{risk})"
                    + Style.RESET_ALL
                )


            log(
                f"{name} stopped -> restarted "
                f"(failures:{failures}, risk:{risk})"
            )


            # unstable detection
            if is_unstable(
                failures
            ):

                if not silent:
                    print(
                        Fore.YELLOW +
                        f"⚠ {name} is UNSTABLE!"
                        + Style.RESET_ALL
                    )

                log(
                    f"{name} marked unstable"
                )


            # popup alert
            show_alert(
                name,
                risk
            )


            # email only severe failures
            if (
                is_unstable(failures)
                or risk=="HIGH"
            ):

                send_failure_email(
                    name,
                    failures,
                    risk
                )


            # self healing
            restart_service(
                command
            )


        # -------------------------
        # HEALTHY
        # -------------------------
        else:

            update_last_seen(
                name
            )

            if not silent:

                print(
                    Fore.GREEN +
                    f"✔ {name} healthy"
                    + Style.RESET_ALL
                )

            log(
                f"{name} healthy"
            )


        # -------------------------
        # Report generation
        # -------------------------
        with open(
            "logs/report.txt",
            "a"
        ) as f:

            f.write(
                f"{name} | "
                f"Failures:{failures if 'failures' in locals() else 0} | "
                f"Risk:{risk if 'risk' in locals() else 'LOW'}\n"
            )



    print(
        f"\nNext health check in "
        f"{CHECK_INTERVAL} seconds..."
    )


    time.sleep(
        CHECK_INTERVAL
    )