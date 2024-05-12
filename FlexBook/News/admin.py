from django.contrib import admin


def admin_register(model_names: list):
    for model_name in model_names:
        model = getattr(__import__('News.models', fromlist=[model_name]), model_name)
        admin.site.register(model)


model_names = ["News"]
admin_register(model_names)
