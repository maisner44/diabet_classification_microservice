import pyotp
import qrcode

def generate_secret_key():
    return pyotp.random_base32()

def generate_provision_url(username):
    key = generate_secret_key()
    return pyotp.totp.TOTP(key).provisioning_uri(name=username, issuer_name='DiaScreen2FA')

def generate_qrcode(url):
   return qrcode.make(url).save("totp.png")