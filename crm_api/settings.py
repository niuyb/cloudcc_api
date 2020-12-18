import os

mode = os.environ.get("SUPPORT_PROFILE")
print(mode)

if mode == "develop":
    from crm_api.develop import *
elif mode == "beta":
    from crm_api.beta import *
else:
    from crm_api.product import *
