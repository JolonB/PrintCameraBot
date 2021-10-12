import sys

from lib import two_factor

def main():
    secret_token = two_factor.generate_secret_token()
    print("Your two-factor authentication key is: \n\n{}\n".format(secret_token))
    print("You should type this into your authenticator app.")
    print(
        "If you don't have an authenticator app, you can use Google"
        " Authenticator or Authy."
    )
    print(
        "Make sure you copy this code into your config.py file in the"
        ' "approved_users" section too.'
    )

    print("\n\n")

    verified = False
    while not verified:
        code = input(
            "Please enter the two-factor authentication code generated by"
            " your authenticator app: "
        )
        verified = two_factor.verify_code_only(code, secret_token)
        if verified:
            print("Two-factor authentication code verified.")
        else:
            print("Two-factor authentication code invalid.", file=sys.stderr)
            print("Try re-entering the key into your authenticator app.")

if __name__ == "__main__":
    main()
